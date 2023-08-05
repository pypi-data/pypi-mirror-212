"""Package for Cabinet and related classes"""
import logging
import shutil
import subprocess
import mimetypes
import tempfile
from pathlib import Path

from pypdf import PdfWriter

import metaindex.shared
from metaindex import yaml
from metaindex import indexers
from metaindex import indexer
from metaindex import CacheEntry

from filecabinet import utils


MIMETYPE_PDF = 'application/pdf'


class LanguageFromFilenameIndexer(metaindex.indexer.IndexerBase):
    """An indexer that extracts the language of the file from its name"""
    NAME = 'filecabinet_filenamelanguage'
    ACCEPTS = '*'
    PREFIX = 'extra.'
    ORDER = metaindex.indexer.Order.EARLY

    def run(self, path, metadata, _):
        language = utils.get_language_from_filename(path)
        if language is not None:
            metadata.add(self.PREFIX + 'language', language)
            other = utils.LANGUAGES.get(language, language)
            if other != language:
                metadata.add(self.PREFIX + 'language', other)


class Document(CacheEntry):
    """Representing a document in a filecabinet"""
    def __init__(self, *args, cabinet=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.cabinet = cabinet

    @classmethod
    def wrap(cls, cabinet, entry):
        """Create a new Document based on ``entry``
        """
        if isinstance(entry, Document):
            entry.cabinet = cabinet
            return entry

        that = cls(entry.path, cabinet=cabinet)
        that.metadata = entry.metadata
        that.last_modified = entry.last_modified
        that.mimetype = entry.mimetype
        that.rel_path = entry.rel_path
        that.storage_label = entry.storage_label
        return that

    def copy(self):
        that = super().copy()
        that.cabinet = self.cabinet
        return that

    def is_new(self):
        return any(v == 'new' for v in self.get('extra.tag'))


class Cabinet:
    """Represents a filecabinet as a container of documents"""
    def __init__(self, name, manager):
        self.manager = manager
        self.config = manager.config
        self.name = name
        self.description = self.config[name].get('description', name)
        self.basedir = self.config.path(name, 'path')
        self.inbox = self.basedir / self.config[name].get('inbox', 'inbox')
        self.documents = self.basedir / self.config[name].get('documents', 'documents')

        self.documents.mkdir(exist_ok=True, parents=True)
        self.inbox.mkdir(exist_ok=True, parents=True)

    def next_doc_id(self):
        while True:
            fullid = utils.random_id()
            prefix = fullid[:4]

            if (self.documents / prefix / fullid).is_dir():
                continue

            return (prefix, fullid)

    def pickup(self, session):
        files = list(self.inbox.iterdir())

        for fn in files[:]:
            if not fn.is_dir():
                continue
            files.remove(fn)
            merged = self.merge_files(fn)
            if merged is not None:
                files.append(merged)

        if self.manager.ocr is not None:
            # convert picture files to OCR'd PDFs
            ## find picture files first
            images = []
            for fn in files[:]:
                mimetype, _ = mimetypes.guess_type(fn, strict=False)
                if mimetype is None:
                    continue
                if not mimetype.startswith('image/'):
                    continue
                images.append(fn)
                files.remove(fn)

            ## process each image file
            for fn in images:
                newfn = self.manager.process_image(fn)
                if newfn is not None:
                    files.append(newfn)
                    try:
                        fn.unlink()
                    except OSError as exc:
                        logging.error(f"Could not clean up '{fn}': {exc}")

        self.index_new_files(session, files)

    def index_new_files(self, session, files):
        """Index the given files and move them to this cabinet's 'document' folder"""
        generator = indexer.index_files(files, self.manager.client_config, 1, None, True, {}, {})

        for result in generator:
            if not result.success:
                logging.warning(f"Unknown file: {result.filename}")
                continue

            result.info.last_modified = metaindex.shared.get_last_modified(result.filename)
            info = result.info

            # new document ID
            prefix, docid = self.next_doc_id()
            docdir = self.documents / prefix / docid
            docdir.mkdir(parents=True)
            docpath = docdir / (docid + info.path.suffix)

            # move to new location
            shutil.move(result.filename, docpath)
            info.path = docpath

            # mark as 'new'
            info.add('extra.tag', 'new')

            # index metadata in cache
            session.cache.reduce(info)
            session.cache.insert(info)

            # split off fulltext
            fulltext = ("\n".join([str(v) for v in info.get('extra.fulltext')])).strip()

            # create the sidecar file
            self.save_metadata(info)

            # write out full text, if there was any
            if len(fulltext) > 0:
                text = docdir / (docid + ".txt")
                text.write_text(fulltext, encoding='utf-8')

    def save_metadata(self, document):
        """Save the metadata of 'document' to its respective sidecar file"""
        docdir = document.path.parent
        docid = document.path.stem
        assert docdir.stem == docid

        to_save = document.copy()
        to_save.delete('extra.fulltext')

        # create sidecar file
        sidecar = docdir / (docid + ".yaml")
        yaml.store(to_save, sidecar)

    def merge_files(self, dirpath):
        """Try and merge all files in ``dirpath`` into one PDF at ``dirpath/../dirpath.pdf``

        Returns the full path to the merged file on success, otherwise ``None``
        """
        assert dirpath.is_relative_to(self.inbox)
        lang = utils.get_language_from_filename(dirpath)

        parts = list(dirpath.iterdir())
        parts.sort()
        mimes = {}
        # if there's anything that's neither image nor PDF in these files, we're out
        for part in parts:
            mimetype, _ = mimetypes.guess_type(part, strict=False)
            mimes[part] = mimetype
            if mimetype is None:
                return None
            if mimetype == MIMETYPE_PDF:
                # PDFs can be merged
                continue
            if not mimetype.startswith('image/'):
                # some file, not an image, not a PDF
                logging.error(f"Can only merge images and PDFs ({dirpath})")
                return None

        # convert all images to PDF and OCR them
        converted = []
        for part in parts:
            mimetype = mimes[part]
            if mimetype == MIMETYPE_PDF:
                converted.append(part)
                continue

            if self.manager.ocr is None:
                logging.error("Tesseract OCR is disabled or not available. "
                              f"Can not merge files in '{dirpath}' meaningfully.")
                return None

            pdffile = self.manager.process_image(part, lang)
            if pdffile is None:
                logging.error(f"Could not convert {part} to PDF")
                return None
            try:
                part.unlink()
            except OSError as exc:
                logging.error(f"Could not clean up converted file '{part}': {exc}")
            converted.append(pdffile)

        # time to merge all pages in `converted`
        with tempfile.NamedTemporaryFile(suffix='.pdf',
                                         dir=dirpath.parent,
                                         delete=False) as tmpfd:
            targetfile = Path(tmpfd.name)

        writer = PdfWriter()
        for part in converted:
            writer.append(part)
        writer.write(targetfile)
        writer.close()

        try:
            shutil.rmtree(dirpath)
        except OSError as exc:
            logging.error(f"Could not delete {dirpath}: {exc}")
        return targetfile

    def files(self):
        """Iterate over all document files in this cabinet"""
        paths = sum([list(d.iterdir())
                     for d in self.documents.iterdir()], start=[])

        for path in paths:
            candidates = [fn for fn in path.iterdir() if fn.suffix != '.yaml']
            if len(candidates) == 0:
                logging.info(f"Abandoned folder {path}")
                continue
            if len(candidates) == 1:
                yield candidates[0]
                continue
            candidates = [c for c in candidates if c.suffix != '.txt']
            assert len(candidates) > 0
            yield candidates[0]

    def reindex(self, session, files=None):
        """Re-index the given files

        If no files were selected, re-index the entire cabinet
        """
        if files is None:
            files = list(self.files())

        if not isinstance(files, (list, tuple, set)):
            files = [files]

        files = [fn for fn in files
                 if fn.is_relative_to(self.documents)]

        for filepath in files:
            sidecar = filepath.parent / (filepath.stem + '.yaml')
            fulltext = filepath.parent / (filepath.stem + '.txt')

            entry = yaml.get(sidecar)
            entry.path = filepath

            if fulltext.is_file():
                entry.add('extra.fulltext', fulltext.read_text(encoding='utf-8'))

            session.cache.insert(entry)

    def update(self, session, documents):
        """Update the metadata information of these documents"""
        for document in documents:
            if not document.path.is_relative_to(self.documents):
                continue
            self.save_metadata(document)
            session.cache.insert(document)
