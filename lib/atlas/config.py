
import yaml

class ConfigParser(object):
    def __enter__(self):
        return True

    def __exit__(self, type, value, traceback):
        return True

    def __init__(self):
        return

    def __slurp(self, yamlfile, section_name):
        with open(yamlfile, 'r') as yaml_file:
            yamldata = yaml.load(yaml_file.read())

        if yamldata and section_name in yamldata:
            return yamldata[section_name]
        else:
            return {}

    def parse(self, yamlfile, section_name):
        return self.__slurp(yamlfile, section_name)

class ConfigManager(object):
    def __enter__(self):
        return True

    def __exit__(self, type, value, traceback):
        return True

    def __init__(self, configfile):
        self.__setup(configfile)

    def __setup(self, configfile):
        self.__setup_config(configfile)
        self.__setup_servers(configfile)
        self.__setup_roles(configfile)
        self.__setup_aux_roles()

    def __setup_config(self, configfile):
        self._config = ConfigParser().parse(configfile, 'config')

    def __setup_servers(self, configfile):
        self._servers = ConfigParser().parse(configfile, 'servers')

    def __setup_roles(self, configfile):
        self._roles = ConfigParser().parse(configfile, 'roles')

    def __setup_aux_roles(self):
        if 'all_servers' not in self._roles:
            self._roles['all_servers'] = []
            for server in sorted(self._servers):
                if server not in self._roles['all_servers']:
                    if server not in self._roles['jumper']:
                        self._roles['all_servers'].append(server)

    @property
    def config(self):
        return self._config

    @property
    def servers(self):
        return self._servers

    @property
    def roles(self):
        return self._roles

