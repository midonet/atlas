
import os

from atlas.config import ConfigManager
from atlas.common import FabricManager

from fabric.api import parallel, roles, run, env

FabricManager.setup(ConfigManager(os.environ["CONFIGFILE"]).roles)

@parallel
@roles('all_servers')
def connectcheck():
    run("""
/sbin/SuSEfirewall2 off

grep 'SUSE Linux Enterprise Server 12' /etc/SuSE-release
""")

    if "OS_MIDOKURA_ROOT_PASSWORD" in os.environ:
        run("""
echo 'root:%s' | chpasswd

useradd -u0 -g0 -m -o midokura; echo

echo 'midokura:%s' | chpasswd
""" % (
            os.environ["OS_MIDOKURA_ROOT_PASSWORD"],
            os.environ["OS_MIDOKURA_ROOT_PASSWORD"]))

