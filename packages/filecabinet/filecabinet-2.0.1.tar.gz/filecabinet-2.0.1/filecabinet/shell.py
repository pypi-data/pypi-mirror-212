"""An interactive commandline shell to work with filecabinet"""
import subprocess
import shutil
import shlex
import os
import tempfile

try:
    import readline
except ImportError:
    readline = None

import yaml


class Shell:
    def __init__(self, session):
        self.session = session
        self.manager = session.manager

        self.quit = False
        self.listed_docs = []

        self.opener = shutil.which(self.manager.config.get('Shell', 'document_opener', 'xdg-open'))
        if self.opener is not None:
            self.opener = shlex.split(self.opener)

        editor = self.manager.config.get('Shell', 'editor', None)
        if editor is None:
            for name in ['VISUAL', 'EDITOR']:
                value = os.getenv(name)
                if value is None:
                    continue
                editor = shutil.which(value)
                if editor is not None:
                    break
        self.editor = editor
        if self.editor is not None:
            self.editor = shlex.split(self.editor)

        self.commands = {'quit': self.do_quit,
                         'help': self.help,
                         'info': self.do_info,
                         'open': self.do_open,
                         'edit': self.do_edit,
                         'pickup': self.do_pickup,
                         'seen': self.do_seen,
                         'new': self.do_new,
                         'kill': self.do_stop,
                         'compact': self.do_compact,
                         'find': self.do_find,
                         'list': self.do_find,
                         }

    def do_quit(self, _):
        """Exit the shell"""
        self.quit = True

    def help(self, _):
        """Show this help"""
        for cmd in sorted(self.commands.keys()):
            fnc = self.commands[cmd]
            print(f"{cmd}\t{fnc.__doc__}")

    def do_find(self, args):
        """Find documents or list the most recently found documents"""
        if len(args) > 0:
            query = " ".join(args)
            self.listed_docs = list(self.session.find(query))
        self.print_doc_list()

    def print_doc_list(self):
        idxwidth = len(str(len(self.listed_docs)))
        for idx, doc in enumerate(self.listed_docs):
            number = f"({idx+1: >{idxwidth}})"
            is_new = "*" if doc.is_new() else " "
            title = doc.path.stem
            for tag, value in doc:
                if not tag.endswith('.title'):
                    continue
                title = value
                break

            tags = ' '.join([f'#{value}'
                             for tag, value in doc
                             if tag.endswith('.tag') and value != 'new'])

            print(f"{number} {is_new} {title} {tags}")

    def do_open(self, args):
        """Open the document in an external program"""
        if self.opener is None:
            print("No opener defined")
            return

        doc = self.doc_from_list(args)
        if doc is None:
            print("Usage: open document-number")
            return

        subprocess.Popen(self.opener + [str(doc.path)],
                         shell=False,
                         stdout=subprocess.DEVNULL,
                         stdin=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)

    def do_edit(self, args):
        """Edit the metadata in an external editor"""
        if not isinstance(self.editor, list):
            print("No editor defined.")
            return

        doc = self.doc_from_list(args)
        if doc is None:
            print("Usage: edit document-number")
            return

        sidecar = doc.path.parent / (doc.path.stem + '.yaml')

        with tempfile.NamedTemporaryFile('w+t', encoding='utf-8', suffix='.yaml') as tmpfh:
            tmpfh.write(sidecar.read_text(encoding='utf-8'))
            tmpfh.flush()

            subprocess.run(self.editor + [tmpfh.name], check=False)
            tmpfh.flush()
            tmpfh.seek(0)

            try:
                other = yaml.safe_load(tmpfh.read())
            except yaml.YAMLError as exc:
                print(f"Failed to load metadata file: {exc}")
                return

            doc.metadata = {}
            for key, values in other.items():
                if not isinstance(values, list):
                    values = [values]
                for value in values:
                    doc.add('extra.' + key, value)

            self.session.update(doc)

    def do_info(self, args):
        """Show the metadata of the selected document"""
        doc = self.doc_from_list(args)
        if doc is None:
            print("Usage: info document-number")
            return

        skip = {'extra.fulltext',}
        tagwidth = max(len(tag) for tag, _ in doc if tag not in skip)

        for tag, value in doc:
            if tag in skip:
                continue
            print(f"{tag: <{tagwidth}}    {value}")

    def doc_from_list(self, args):
        if len(args) < 1:
            return None
        if not args[0].isnumeric():
            return None
        nr = int(args[0])-1
        if nr >= len(self.listed_docs) or nr < 0:
            return None
        return self.listed_docs[nr]

    def do_pickup(self, _):
        """Process all files in all cabinets inboxes"""
        self.session.pickup()
        self.do_find(['tag:new'])

    def do_stop(self, _):
        """Quit the shell and also stop the background server"""
        self.quit = True
        self.manager.cache.shutdown()

    def do_compact(self, _):
        """Compact the backend database"""
        self.manager.cache.compact()

    def do_seen(self, args):
        """Mark the document as seen (remove 'new' tag)"""
        doc = self.doc_from_list(args)
        if doc is None:
            print("Usage: seen document-number")
            return

        if not doc.is_new():
            return

        doc.delete(('extra.tag', 'new'))
        self.session.update(doc)

    def do_new(self, args):
        """Mark that document as new"""
        doc = self.doc_from_list(args)
        if doc is None:
            print("Usage: new document-number")
            return

        if doc.is_new():
            return

        doc.add('extra.tag', 'new')
        self.session.update(doc)

    def run(self):
        if self.opener is None:
            print("[Warning] There is no document opener defined or the "
                  "defined document opener could not be found.\nThe 'open' "
                  "command will not work.\nPlease "
                  "check your configuration file to fix this.")
        if self.editor is None:
            print("[Warning] There is no metadata editor defined or the "
                  "defined editor could not be found.\nThe 'edit' "
                  "command will not work.\nPlease "
                  "check your configuration file to fix this.")
        while not self.quit:
            try:
                rawcmd = input('> ')
            except (KeyboardInterrupt, EOFError):
                self.quit = True
                continue

            cmds = tokenize(rawcmd)
            matches = []
            if len(cmds) > 0:
                for name in sorted(self.commands.keys()):
                    if name.startswith(cmds[0]):
                        matches.append(name)
            if len(matches) == 1:
                self.commands[matches[0]](cmds[1:])
            elif len(matches) > 1:
                print("Not quite sure what of these commands you meant:\n {}".format("\n ".join(matches)))
            elif len(rawcmd.strip()) > 0:
                print("I don't know what you mean. Try 'help' to see all available commands.")


def tokenize(text):
    words = []

    word = ''
    quote = None
    escaped = False

    for letter in text:
        if escaped:
            word += letter
            escaped = False
        else:
            if letter == '\\':
                escaped = True
            elif quote is not None and letter == quote:
                quote = None
                words.append(word)
                word = ''
            elif quote is None and letter in " \t":
                words.append(word.strip())
                word = ''
            elif quote is None and letter in '"\'' and len(word.strip()) == 0:
                word = ''
                quote = letter
            else:
                word += letter

    if len(word.strip()) > 0:
        words.append(word.strip())

    return [word for word in words if len(word) > 0]
