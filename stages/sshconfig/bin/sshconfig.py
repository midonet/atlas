#!/usr/bin/env python

import sys

from atlas.config import ConfigManager

metadata = ConfigManager(sys.argv[1])

if __name__ == "__main__":
    with open(sys.argv[2], 'w') as sshconfig:
        for server in metadata.servers:
            for entry in [server, "%s.%s" % (server, metadata.config['domain'])]:
                sshconfig.write("""Host %s
    User root
    ServerAliveInterval 2
    KeepAlive yes
    ConnectTimeout 30
    TCPKeepAlive yes
    Hostname %s

""" % (entry, metadata.servers[server]["ip"]))

    sys.exit(0)

