import configparser
import os
import logging
import pathlib

from . import utils


HERE = pathlib.Path(__file__).parent

HOME = pathlib.Path().home()
PROGRAMNAME = 'filecabinet'
CONFFILENAME = PROGRAMNAME + os.path.extsep + 'conf'
CONFIGFILE = HOME / ".config" / PROGRAMNAME / CONFFILENAME
INDEXPATH = HOME / ".cache" / PROGRAMNAME


try:
    from xdg import BaseDirectory
    CONFIGFILE = pathlib.Path(BaseDirectory.load_first_config(CONFFILENAME) or CONFIGFILE)
    INDEXPATH = pathlib.Path(BaseDirectory.save_cache_path(PROGRAMNAME) or INDEXPATH)
except ImportError:
    BaseDirectory = None


CONF_DEFAULTS = {'General': {'loglevel': 'warning',
                             'database': INDEXPATH,
                            },
                 'Shell': {'document_opener': 'xdg-open',
                          },
                 'OCR': {'enabled': 'yes',
                         'default-language': 'eng',
                        },
                 }


class Configuration:
    def __init__(self, conf):
        self.conf = conf
        self.filepath = None
        """Path to the configuration file"""
        self._userfile = None

    def cabinets(self):
        for group in self.conf:
            if group not in CONF_DEFAULTS.keys() and self.conf[group].get('path', None) is not None:
                yield group

    def __contains__(self, group):
        return group in self.conf

    def __getitem__(self, group):
        return self.conf[group]

    def get(self, group, item, default=None):
        return self.conf[group].get(item, default)

    def bool(self, group, item, default='n'):
        return self.get(group, item, default).lower() in ['y', 'yes', '1', 'true', 'on']

    def number(self, group, item, default='0'):
        value = self.get(group, item, default)
        if value.isnumeric():
            return int(value)
        return None

    def size(self, group, item, default='0'):
        return utils.parse_size(self.get(group, item, default))

    def duration(self, group, item, default=''):
        return utils.parse_duration(self.get(group, item, default))

    def path(self, group, item, default=None):
        return pathlib.Path(self.get(group, item, default)).expanduser()

    def list(self, group, item, default='', separator=',', strip=True, skipempty=True):
        result = []
        for v in self.get(group, item, default).split(separator):
            if strip:
                v = v.strip()
            if skipempty and len(v) == 0:
                continue
            result.append(v)
        return result


def get_configuration(conffile=None):
    conf = configparser.ConfigParser(interpolation=None)
    conf.read_dict(CONF_DEFAULTS)

    if conffile is not None and not os.path.exists(os.path.abspath(conffile)):
        logging.warning(f"Configuration file {conffile} not found. "
                        "Using defaults.")
        conffile = None
    if conffile is None and CONFIGFILE.is_file():
        conffile = CONFIGFILE

    if conffile is not None:
        logging.info(f"Loading configuration from {conffile}.")
        conf.read([conffile])

    finalconfig = Configuration(conf)
    finalconfig.filepath = pathlib.Path(conffile or CONFIGFILE)
    return finalconfig
