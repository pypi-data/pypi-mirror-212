import logging
import subprocess
import shutil
import time
import tempfile
from pathlib import Path

import PIL.Image

import metaindex.configuration
import metaindex.shared
from metaindex import Cache
from metaindex import proto
from metaindex.client import Client

from filecabinet import utils
from filecabinet.cabinet import Cabinet, Document


METAINDEXCONFIG = '''[General]
cache = {cache}
socket = {socket}
index-unknown = no
preferred-sidecar-format = .yaml
recursive-extra-metadata = no
implicit-tags = issuer, creator, title, tag, subject
ocr = no

[Indexer:rule-based]
{rules}

[Synonyms]
fulltext = pdf.fulltext, extra.fulltext
issuer = extra.issuer
creator = extra.creator
subject = extra.subject
tag = extra.tag, extra.tags, rules.tag, rules.tags
language = extra.language, rules.language
date = extra.date, rules.date

[Server]
loglevel = warning
logfile = {logfile}
index-new-tags = yes
'''


class FilecabinetCache(Cache):
    """A cache with different 'reduce' rules"""
    def __init__(self, manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager

    def reduce(self, entry):
        for key in set(entry.metadata.keys()):
            values = entry.metadata[key]
            skey = None

            if key in self.config.synonymized and any(len(str(v.raw_value)) > 0 for v in values):
                skey = 'extra.' + self.config.synonymized[key]
            elif key.startswith('extra.'):
                skey = key.lower()
            elif key.startswith('rules.') and len(key.strip()) > 6:
                skey = 'extra.' + key.strip()[6:]

            if skey is not None:
                if skey not in entry.metadata:
                    entry.metadata[skey] = []
                entry.metadata[skey] = list(set(entry.metadata[skey] + [v for v in values if len(str(v.raw_value)) > 0]))

            if key != skey:
                del entry.metadata[key]

        return entry

    def find(self, *args, **kwargs):
        results = [Document.wrap(self.manager.path_cabinet.get(Path(*entry.path.parts[:-4])), entry)
                   for entry in super().find(*args, **kwargs)]
        return results

    def get(self, *args, **kwargs):
        results = [Document.wrap(self.manager.path_cabinet.get(Path(*entry.path.parts[:-4])), entry)
                   for entry in super().get(*args, **kwargs)]
        return results

    def shutdown(self):
        self.client.send(proto.Shutdown())


class Manager:
    def __init__(self, configuration):
        self.config = configuration

        self.ocr = None

        # check whether there is any OCR, if needed
        if self.config.bool('OCR', 'enabled'):
            self.ocr = shutil.which('tesseract')

        # create the metaindex configuration, overwrite existing ones
        cachepath = self.config.path('General', 'database')
        rules = []
        if 'Rules' in self.config:
            rules = [f"{k} = {self.config.get('Rules', k)}" for k in self.config['Rules']]
        self.miconfig = cachepath / 'metaindex.conf'
        if not self.miconfig.is_file() or (self.config.filepath is not None
           and self.config.filepath.is_file() and
           metaindex.shared.get_last_modified(self.config.filepath) > metaindex.shared.get_last_modified(self.miconfig)):
            cachepath.mkdir(parents=True, exist_ok=True)
            self.miconfig.parent.mkdir(parents=True, exist_ok=True)
            socketpath = self.miconfig.parent / 'metaindex.sock'
            logfile = self.miconfig.parent / 'metaindex.log'
            self.miconfig.write_text(METAINDEXCONFIG.format(cache=str(cachepath),
                                                            socket=str(socketpath),
                                                            logfile=str(logfile),
                                                            rules="\n".join(rules)))
        self.client_config = metaindex.configuration.load(self.miconfig)
        self.cache = None  # lazily created when a new session is created

        self.cabinets = []
        self.path_cabinet = {}  # mapping cabinet.basedir -> cabinet
        for cabinetname in configuration.cabinets():
            try:
                cabinet = Cabinet(cabinetname, self)
                self.cabinets.append(cabinet)
                self.path_cabinet[cabinet.basedir] = cabinet
            except RuntimeError as exc:
                logging.error(exc)
                continue

    def launch_server(self):
        """Launch the corresponding metaindexserver"""
        client = Client(self.client_config)
        if not client.connection_ok():
            subprocess.run(['metaindexserver', '-c', str(self.miconfig), '-d'])
            time.sleep(1)
        assert client.connection_ok()

    def find_cabinet(self, name):
        for cabinet in self.cabinets:
            if cabinet.name == name:
                return cabinet
        return None

    def new_session(self):
        if self.cache is None:
            self.cache = FilecabinetCache(self, self.client_config)
        return Session(self)

    def process_image(self, fn, default_lang=None):
        """Run Tesseract OCR on the given file and create a OCR'ed PDF

        Returns the ``Path`` to the created PDF file or ``None`` upon error.
        """
        if self.ocr is None:
            return None

        dpi = PIL.Image.open(fn).info.get('dpi', [0])[0]

        with tempfile.NamedTemporaryFile(suffix='.pdf', dir=fn.parent, delete=True) as tmpfd:
            pdffile = Path(tmpfd.name)
            outputbase = str(pdffile.parent / pdffile.stem)

        lang = utils.get_language_from_filename(fn)
        if lang is None:
            lang = default_lang or self.config.get('OCR', 'default-language', 'eng')

        result = subprocess.run([self.ocr,
                                 str(fn),
                                 outputbase,
                                 '-c', 'tessedit_create_pdf=1',
                                 '-c', f'user_defined_dpi={dpi}',
                                 '-l', lang],
                                stdout=subprocess.DEVNULL,
                                stdin=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL,
                                check=False)
        if result.returncode == 0:
            return pdffile
        return None


class Session:
    def __init__(self, manager):
        self.manager = manager
        self.cache = manager.cache

    def pickup(self, cabinet=None):
        if cabinet is None:
            for that in self.manager.cabinets:
                self.pickup(that)
        else:
            cabinet.pickup(self)

    def reindex(self, cabinet=None):
        if cabinet is None:
            for that in self.manager.cabinets:
                self.reindex(that)
        else:
            cabinet.reindex(self)

    def find(self, query):
        """Return a list of all documents that match this query"""
        return list(self.cache.find(query))

    def update(self, doc):
        """Update the stored metadata of 'doc'"""
        cabinet = self.manager.path_cabinet.get(doc.path.parent.parent.parent.parent)
        if cabinet is None:
            logging.error(f"Document {doc.path} does not appear to be part of any cabinet.")
            return

        cabinet.update(self, [doc])

    def add(self, cabinet, sources, samedoc=False, allowduplicates=False, metadata={}):
        """Add the source files to the cabinet

        :arg cabinet The target cabinet to add the files to
        :arg sources A list of files
        :arg samedoc If True, add all files to the same document as pages, otherwise create new documents per file
        :arg allowduplicates If False, reject any duplicate documents/pages. If True, accept.
        :arg metadata Metadata to apply to all added documents
        """
