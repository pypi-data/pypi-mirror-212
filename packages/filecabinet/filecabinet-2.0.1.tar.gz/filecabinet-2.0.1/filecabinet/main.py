import argparse
import logging
import sys
import re
import mimetypes
from pathlib import Path

from metaindex import indexers
from metaindex import indexer

from filecabinet.configuration import get_configuration, CONFIGFILE
from filecabinet.manager import Manager
from filecabinet.shell import Shell


CABINET_ID_RE = re.compile(r'^[\w][^\t\n\r\f\v]*$')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config',
                        default=None,
                        type=str,
                        help=f'The config file you wish to use. Defaults to {CONFIGFILE}')
    parser.add_argument('-l', '--log-level',
                        choices=['debug', 'info', 'warning', 'error', 'fatal'],
                        default=None,
                        help='The loglevel.')
    
    subparsers = parser.add_subparsers(dest='command')

    serviceparser = subparsers.add_parser('service', help='Maintenance tasks')
    serviceparser.add_argument('action',
                               choices=['stop', 'compact', 'start'],
                               help="What task to perform. Options are: 'stop' "
                                    "to stop the backend server, 'start' to "
                                    "start the backend server, 'compact' to "
                                    "compact the backend database.")

    subparsers.add_parser('shell', help='Start the filecabinet shell')

    listparser = subparsers.add_parser('list', help='List various things')
    listparser.add_argument('what',
                            choices=['cabinets', 'documents', 'new'],
                            help="What to list. Options are: %(choices)s.")

    findparser = subparsers.add_parser('find', help="Find documents")
    findparser.add_argument('query',
                            nargs='*',
                            type=str,
                            help="The search query to run")

    rulesparser = subparsers.add_parser('test-rules', help="Test your rules on a file")
    rulesparser.add_argument('-t', '--text',
                             action="store_true",
                             default=False,
                             help="Print the full text that was found.")
    rulesparser.add_argument('file',
                             type=str,
                             help="The file to run the rules on")

    initparser = subparsers.add_parser('init', help="Initialize a new file cabinet")
    initparser.add_argument('-d', '--description',
                            default='',
                            type=str,
                            help="Optional single line description.")
    initparser.add_argument('-n', '--name',
                            default='cabinet',
                            type=str,
                            help="Unique name for this file cabinet. Defaults to %(default)s.")
    initparser.add_argument('path',
                            type=str,
                            help="Path where the documents should be stored.")

    subparsers.add_parser('pickup', help='Pick up files from incoming')

    reindexparser = subparsers.add_parser('reindex', help='Rebuild index')
    reindexparser.add_argument('-c', '--cabinet',
                               default=None,
                               type=str,
                               help="The cabinet to reindex. If there is only "
                                    "one cabinet, this can be left empty.")

    args = parser.parse_args(sys.argv[1:])
    if args.command not in ['service', 'pickup', 'list', 'find', 'test-rules', 'reindex', 'init', 'shell']:
        parser.print_help()

    return args


def error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def run():
    logging.basicConfig(level=logging.WARNING)
    args = parse_args()

    conf = get_configuration(args.config)

    level = args.log_level if args.log_level is not None else conf['General']['loglevel'].upper()
    logging.getLogger().setLevel(level.upper())

    manager = Manager(conf)

    if args.command == 'init':
        sys.exit(create_new_cabinet(manager, args))

    elif args.command == 'test-rules':
        sys.exit(test_rules(manager, args))

    elif len(manager.cabinets) == 0:
        logging.warning(f"There are no cabinets configured.")
        sys.exit(-1)

    manager.launch_server()

    if args.command == 'service':
        session = manager.new_session()

        if args.action == 'stop':
            session.cache.shutdown()

        if args.action == 'compact':
            session.cache.compact()

        if args.action == 'start':
            pass  # already done

    elif args.command == 'pickup':
        session = manager.new_session()
        session.pickup()

    elif args.command == 'find':
        query = " ".join(args.query)
        session = manager.new_session()
        for result in session.find(query):
            print(result)

    elif args.command == 'reindex':
        session = manager.new_session()
        session.reindex()

    elif args.command == 'list':
        if args.what == 'cabinets':
            for cabinet in manager.cabinets:
                print(f"{cabinet.name}\t{cabinet.basedir}")

        if args.what == 'new':
            session = manager.new_session()
            for doc in session.find('tag:new'):
                print(doc.path)

        if args.what == 'documents':
            raise NotImplementedError("Not gonna do that just now")

    elif args.command == 'shell':
        Shell(manager.new_session()).run()

    sys.exit(0)


def create_new_cabinet(manager, args):
    # 1. check if the path to the config file exists
    confpath = manager.config.filepath
    if confpath is None:
        confpath = CONFIGFILE
    try:
        confpath.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        error(f"Could not create path to configuration file '{confpath.parent}': {exc}")
        return -2

    # 2. check that the path to the new cabinet does not exist
    cabinetpath = Path(args.path).expanduser().absolute()
    if cabinetpath.exists() and any(cabinetpath.iterdir()):
        error(f"Path for new file cabinet '{cabinetpath}' exists and is not empty!")
        cabinet = manager.path_cabinet.get(cabinetpath)
        if cabinet is not None:
            error(f"Cabinet {cabinet.name} is defined at that location.")
        return -3

    # 3. touch config file (to test we can write)
    try:
        confpath.touch()
    except OSError as exc:
        error(f"Cannot write to '{confpath}': {exc}")
        return -4

    # 4. determine a good cabinet id
    cabinetcounter = ''
    cabinetbasename = args.name
    if not CABINET_ID_RE.match(cabinetbasename):
        error(f"'{args.name}' is not a valid name for a file cabinet. "
              "Please do not use new-line or control characters.")
        return -6

    while True:
        cabinetid = f'{cabinetbasename}{cabinetcounter}'
        if cabinetid in manager.config:
            if cabinetcounter == '':
                cabinetcounter = 1
            else:
                cabinetcounter += 1
            continue
        break

    # 5. create the cabinet path
    inboxname = 'inbox'  # TODO allow configuration
    documentsname = 'documents'  # TODO allow configuration
    try:
        cabinetpath.mkdir(parents=True, exist_ok=True)
        (cabinetpath / inboxname).mkdir()
        (cabinetpath / documentsname).mkdir()
    except OSError as exc:
        error(f"Could not create paths for new file cabinet: {exc}")
        return -5


    # 6. add the cabinet to the config
    name = ''
    if len(args.name.strip()) > 0:
        name = f'name = {args.name.strip()}'
    text = ''
    if confpath.exists():
        text = confpath.read_text(encoding='utf-8')
        text += "\n\n"
    text += f"""[{cabinetid}]
path = {cabinetpath}
inbox = {inboxname}
documents = {documentsname}
{name}
"""
    confpath.write_text(text, encoding='utf-8')

    return 0


def test_rules(manager, args):
    # 1. Check that rule file are defined and exist
    if 'Rules' not in manager.config or len(manager.config['Rules']) == 0:
        error("No rule files defined in your configuration file {manage.config.filepath}.")
        return -1

    indexer.logger.setup(logging.WARNING)

    missing_rule_files = [manager.config.path('Rules', name)
                          for name in manager.config['Rules']
                          if not manager.config.path('Rules', name).is_file()]
    if len(missing_rule_files) > 0:
        logging.warning("These rule files are defined but don't actually exist: %s" ,
                        ", ".join(str(p) for p in missing_rule_files))
    if len(missing_rule_files) == len(manager.config['Rules']):
        error("No rule files exist on disk.")
        return -2

    # 2. extract fulltext from file, OCR if required
    sourcefile = Path(args.file).expanduser()
    to_index = [sourcefile]
    delete_me = None
    mime, _ = mimetypes.guess_type(sourcefile, strict=False)
    if mime is not None and mime.startswith('image/'):
        delete_me = manager.process_image(sourcefile)
        to_index = [delete_me]

    results = list(indexer.index_files(to_index, manager.client_config, 1, None, True, {}, {}))
    for result in results:
        if args.text:
            fulltext = "\n".join(value.raw_value
                                 for tag, value in result.info
                                 if tag.endswith('.fulltext'))
            print(fulltext)
        for tag, value in result.info:
            if not tag.startswith('rules.'):
                continue
            print(f"{tag}: {value}")

    if delete_me is not None:
        try:
            delete_me.unlink()
        except OSError as exc:
            error(f"Could not delete temporary file '{delete_me}': {exc}")

    return 0
