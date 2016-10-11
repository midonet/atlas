
import os
import sys

from atlas.config import ConfigManager
from atlas.common import FabricManager
from atlas.services import ServiceControl

from fabric.api import parallel, roles, run, env

metadata = ConfigManager(os.environ["CONFIGFILE"])

FabricManager.setup(metadata.roles)

@parallel
@roles('all_servers')
def newrelic():
    if "NEWRELIC_LICENSE_KEY" not in os.environ:
        sys.exit(0)

    run("""
SERVER_NAME="%s"
DOMAIN_NAME="%s"
LICENSE_KEY="%s"

if [[ "" == "$(ps axufwwwww | grep -v grep | grep nrsysmond)" ]]; then
    cd /root

    curl http://download.newrelic.com/server_monitor/release/newrelic-sysmond-2.3.0.132-linux.tar.gz >newrelic.tar.gz

    tar xzvpf newrelic.tar.gz

    mkdir -pv /etc/newrelic
    mkdir -pv /var/log/newrelic

    cat>/etc/newrelic/nrsysmond.cfg<<EOF
license_key=${LICENSE_KEY}
loglevel=info
logfile=/var/log/newrelic/nrsysmond.log
hostname=${SERVER_NAME}.${DOMAIN_NAME}
EOF

    cp /root/newrelic-sysmond-2.3.0.132-linux/daemon/nrsysmond.x64 /usr/local/bin/nrsysmond

    /root/newrelic-sysmond-2.3.0.132-linux/scripts/nrsysmond-config --set license_key="${LICENSE_KEY}"
fi

ps axufwwwww | grep -v grep | grep nrsysmond || \
    /usr/local/bin/nrsysmond -s -c /etc/newrelic/nrsysmond.cfg

""" % (
        env.host_string,
        metadata.config["domain"],
        os.environ["NEWRELIC_LICENSE_KEY"]))

