
import os

from atlas.config import ConfigManager
from atlas.common import FabricManager
from atlas.suse import RepoManager
from atlas.crowbar import Network

from fabric.api import parallel, roles, run, puts, env
from fabric.colors import yellow

metadata = ConfigManager(os.environ["CONFIGFILE"])

FabricManager.setup(metadata.roles)

@parallel
@roles('nodes')
def nodes():

    run("""
cat >/etc/zypp/repos.d/SLES12.repo<<EOF
[SLES12]
enabled=1
autorefresh=0
baseurl=http://192.168.124.10:8091/suse-12.1/x86_64/install/
type=NONE
EOF

cat >/etc/zypp/repos.d/server_monitoring.repo<<EOF
[server_monitoring]
name=Server Monitoring Software (SLE_12_SP1)
enabled=1
autorefresh=0
baseurl=http://download.opensuse.org/repositories/server:/monitoring/SLE_12_SP1/
type=rpm-md
gpgcheck=0
gpgkey=http://download.opensuse.org/repositories/server:/monitoring/SLE_12_SP1//repodata/repomd.xml.key
EOF

zypper update --no-confirm

zypper install --auto-agree-with-licenses -y screen htop

curl http://192.168.124.10:8091/suse-12.1/x86_64/crowbar_register > /root/crowbar_register

chmod 0755 /root/crowbar_register
""")

    Network.rescue(metadata.servers[env.host_string]['ip'])

    run("""
screen -- /root/crowbar_register -v -f --gpg-auto-import-keys --no-gpg-checks || \
    screen -- /root/crowbar_register -v -f --gpg-auto-import-keys --no-gpg-checks || \
        screen -- /root/crowbar_register -v -f --gpg-auto-import-keys --no-gpg-checks || exit 0
""")

