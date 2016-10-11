
import os
from atlas.config import ConfigManager

from fabric.api import puts, local
from fabric.colors import yellow

def pingcheck():
    metadata = ConfigManager(os.environ["CONFIGFILE"])

    domain = metadata.config["domain"]
    for server in sorted(metadata.servers):
        server_ip = metadata.servers[server]["ip"]
        puts(yellow("pinging %s.%s (%s)" % (server, domain, server_ip)))
        local("ping -c1 -W3 %s" % server_ip)

