# filecabinet

filecabinet is a minimal document management system for your computer. It has
metadata per document and supports fulltext search in various document types.


# Installing

The easiest way to install is to use `pip`:

```bash
    pip install filecabinet
```

Alternatively you can get the source code at
[codeberg](https://codeberg.org/vonshednob/filecabinet):

```bash
    git clone https://codeberg.org/vonshednob/filecabinet
    pip install filecabinet
```


## Requirements

`filecabinet` **requires** the [xapian python bindings](https://xapian.org/docs/bindings/python/)
which can not be installed through `pip`!

Other automatically installed required dependencies are:

 * [metaindex](https://codeberg.org/vonshednob/metaindex)
 * [Pillow](https://pypi.org/project/Pillow/)
 * [PyPDF](https://pypi.org/project/pypdf/)
 * [PyYAML](https://pypi.org/project/PyYAML/)

Even though optional, I strongly recommend installing [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
to enable fulltext search in scanned documents.


# Quick start

To initialize your file cabinet, run `filecabinet init` and provide a new
path where you would like to store your documents:

```bash
    filecabinet init ~/Documents/cabinet
```

Now you can start either copying files into `~/Documents/cabinet/inbox` and
run

```bash
    filecabinet pickup
```

to process them, or add files manually via

```bash
    filecabinet add ~/some_scanned_document.jpg
```

To get a basic overview of documents, you can use the Shell.


# Shell

There’s a basic shell that allows you to inspect indexed documents, edit
their metadata (by means of an external text editor), or view the
documents.

To open the shell, run

```bash
    filecabinet shell
```

Try `help` inside the shell to see what your options are.

If you want to use a specific text editor to modify metadata, consider
updating your configuration file’s `Shell` section and add a
`document_editor`, like this:

```ini
    [Shell]
    editor = subl -w
```

In this example we set up SublimeText as the external editor. Note that the
`-w` option is necessary to make filecabinet wait until you’re done editing
the file before returning into the shell.  
Visual Studio Code uses the `-W` or `--wait` flag to accomplish the same
behaviour.


# Searching

Searching for **tags** is done case-insensitive and is done using `tag:`.
For example if you're looking for a document that's tagged with *banana*, you
can search for it by `tag:banana`.

Searching **new** documents is accomplished by searching for `tag:new`.
If you only want to find documents that are not new, you can also
search for `-tag:new`. Unless specified, a search will ignore whether or not a
document is new.

You can search for any **metadata** value, like *title*, *author*, or *language*,
by searching with the metadata name and a colon like `title:gravity`.

Everything else that does not match the special search terms will be used in
the **fulltext** search.

If you want to search for terms with whitespaces, you can use quotes:
`title:"brain surgery"`.

**Example:**

The title contains "brain", is from author "Gumby" and it was set to some time
before August 2005: `title:brain author:gumby date:2015-08-01`

Looking for a newly added document with the title "The Larch": `title:larch tag:new`


# OCR

filecabinet can use Tesseract OCR to do character recognition on pictures and
scanned PDFs, so you can search the text of images.

In order for that to work, you have to install Tesseract and some language
packages, depending on the languages of the documents you wish to scan.

If you don't have Tesseract OCR installed, filecabinet will still work, but
be much less useful.


# Rule based tagging

By using metaindex, filecabinet inherits the powerful rule based
tagging. This allows you to automatically add metadata tags to documents
based on their text (which might have come from OCR).

Rules are defined in text files and you have to point filecabinet to the
rule files that you want it to use. To do that, add a section `[Rules]` to
your configuration file (usually at
`~/.config/filecabinet/filecabinet.conf`) and list your rule files like
this:

```ini
    [Rules]
    base = ~/.config/filecabinet/basic_rules.txt
    companies = ~/Document/company_rules.txt
```

The names (before the `=`) are somewhat free-form descriptors.

To understand how to write these rule files, please have a look at the
[metaindex documentation](https://codeberg.org/vonshednob/metaindex/src/branch/main/doc/source/indexers.rst#rule-based-indexer).

To test your rules on documents, you can use the `filecabinet test-rules`
command. It will run all indexers on a file and show you what tags have
been found by your rules.

When using `test-rules` the tested document will not be added to your
cabinet.


# Cabinet Directory Structure

Assuming a cabinet is set up at `~/cabinet`, the directory structure is:

```
    ~/cabinet
     │
     ├── inbox
     │
     ├── metaindex.conf
     │
     ├── metaindex.log
     │
     └── documents
          │
          └── <partial document id>
               │
               └── <full document id>
                    │
                    ├── <document id>.yaml
                    │
                    ├── <document id>.<suffix>
                    │
                    └── <document id>.txt
```

 * `inbox` will be processed (and emptied) when `filecabinet pickup` is being run
 * `documents` contains the documents
 * `<document id>.yaml` contains the metadata
 * `<document id>.<suffix>` is the original document (usually a PDF)
 * `<document id>.txt` is the extracted full text, if it could be extracted
 * `metaindex.conf`, the configuration file for filecabinet's metaindexserver
 * `metaindex.log`, the log file of file cabinet's metaindexserver


# Usage from Python

To use `filecabinet` from Python, you can use this boilerplate:

```python
from filecabinet import Manager


manager = Manager()
manager.launch_server()

session = manager.new_session()
```

`session` will be an instance of `Session` which, together with `manager`,
allows manipulation of metadata and querying of documents.

