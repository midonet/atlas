
import os

from atlas.config import ConfigManager
from atlas.common import FabricManager
from atlas.suse import RepoManager
from atlas.crowbar import Network

from fabric.api import parallel, roles, run, local

metadata = ConfigManager(os.environ["CONFIGFILE"])

FabricManager.setup(metadata.roles)

@roles('jumper')
def jumper():
    run("""
test -f /root/.ssh/id_rsa || ssh-keygen -t rsa -N "" -f /root/.ssh/id_rsa
""")

    pubkey = run("cat /root/.ssh/id_rsa.pub")

    soc6hosts = []

    for xtuple in [10,81,82,83,84,85,86]:
        soc6hosts.append("192.168.124.%s" % xtuple)

    for ip in sorted(soc6hosts):
        local("""
ssh-keygen -f "/root/.ssh/known_hosts" -R 192.168.1.1

ssh -o StrictHostKeyChecking=no -o ForwardAgent=yes -F tmp/.ssh/config -t jumper -- ssh -o StrictHostKeyChecking=no root@%s 'tee -a /root/.ssh/authorized_keys' <<EOF
%s
EOF
""" % (ip, pubkey))

        run("""
IP="%s"

ssh-keygen -f "/root/.ssh/known_hosts" -R ${IP}

ssh -o StrictHostKeyChecking=no ${IP} -t 'tee /etc/sysconfig/network/ifcfg-eth1' <<EOF
BOOTPROTO='static'
ONBOOT='yes'
BROADCAST='192.168.1.255'
ETHTOOL_OPTIONS=''
IPADDR='192.168.1.%s'
MTU='1450'
NETMASK='255.255.255.0'
NETWORK='192.168.1.0'
REMOTE_IPADDR=''
STARTMODE='auto'
USERCONTROL='no'
EOF

ssh -o StrictHostKeyChecking=no ${IP} -t 'ifup eth1; ip a; route add -net 192.168.9.0/24 gw 192.168.1.1; route -n'

""" % (ip, ip.split('.')[3]))
