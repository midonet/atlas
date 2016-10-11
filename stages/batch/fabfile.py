
import os

from atlas.config import ConfigManager
from atlas.common import FabricManager
from atlas.suse import RepoManager
from atlas.crowbar import Network

from fabric.api import parallel, roles, run, env, puts
from fabric.colors import green, yellow, red

metadata = ConfigManager(os.environ["CONFIGFILE"])

FabricManager.setup(metadata.roles)

@roles('crowbar')
def batch():
    controller = run("crowbar machines list | sort -n | grep -v soc6admin | head -n1")

    computes = []

    for compute in str(run("""
for COMPUTE in $(crowbar machines list | sort -n | grep -v soc6admin | tail -n+2); do
    echo "${COMPUTE}"
done
""")).split('\n'):
        computes.append(compute.replace('\n', '').replace('\r', ''))

    puts(yellow("controller: %s" % controller))

    for compute in computes:
        puts(green("compute: %s" % compute))

    run("""
cat>/root/atlas.yaml<<EOF
---
proposals:
- barclamp: database
  attributes:
  deployment:
    elements:
      database-server:
      - dfa-16-3e-12-25-6c.soc6.benningen.midokura.de
- barclamp: rabbitmq
  attributes:
    password: YywmU6i5HNFm
    trove:
      password: 1E8N3tjNMmLh
  deployment:
    elements:
      rabbitmq-server:
      - dfa-16-3e-12-25-6c.soc6.benningen.midokura.de
- barclamp: keystone
  attributes:
    database_instance: default
    rabbitmq_instance: default
    db:
      password: VCd3XSIl0ZjL
    service:
      token: 4ouMRclrRT97
  deployment:
    elements:
      keystone-server:
      - dfa-16-3e-12-25-6c.soc6.benningen.midokura.de
- barclamp: glance
  attributes:
    service_password: T8u9E69cCWNk
    db:
      password: RF7VcEcB0Yuk
    keystone_instance: default
    database_instance: default
    rabbitmq_instance: default
  deployment:
    elements:
      glance-server:
      - dfa-16-3e-12-25-6c.soc6.benningen.midokura.de
- barclamp: cinder
  attributes:
    rabbitmq_instance: default
    keystone_instance: default
    glance_instance: default
    database_instance: default
    service_password: nrNd4arOvbod
    volumes:
    - backend_driver: local
      backend_name: local
      local:
        volume_name: cinder-volumes
        file_name: "/var/lib/cinder/volume.raw"
        file_size: 2000
    db:
      password: lU1tezWEzYHZ
  deployment:
    elements:
      cinder-controller:
      - dfa-16-3e-12-25-6c.soc6.benningen.midokura.de
      cinder-volume:
      - dfa-16-3e-12-25-6c.soc6.benningen.midokura.de
- barclamp: neutron
  attributes:
    service_password: x7SVhyavIOSo
    rabbitmq_instance: default
    keystone_instance: default
    ml2_mechanism_drivers:
    - linuxbridge
    ml2_type_drivers:
    - vlan
    ml2_type_drivers_default_provider_network: vlan
    ml2_type_drivers_default_tenant_network: vlan
    database_instance: default
    db:
      password: 6eNv0X1PAmGn
  deployment:
    elements:
      neutron-server:
      - dfa-16-3e-12-25-6c.soc6.benningen.midokura.de
      neutron-network:
      - dfa-16-3e-12-25-6c.soc6.benningen.midokura.de
- barclamp: nova
  attributes:
    service_password: JEql6g8dySsQ
    neutron_metadata_proxy_shared_secret: dC3gPgPp8Nu7
    database_instance: default
    rabbitmq_instance: default
    keystone_instance: default
    glance_instance: default
    cinder_instance: default
    neutron_instance: default
    itxt_instance: ''
    db:
      password: OVNzaFYbAa0j
  deployment:
    elements:
      nova-controller:
      - dfa-16-3e-12-25-6c.soc6.benningen.midokura.de
      nova-compute-hyperv: []
      nova-compute-kvm: []
      nova-compute-qemu:
      - dfa-16-3e-23-bc-fd.soc6.benningen.midokura.de
      - dfa-16-3e-84-10-20.soc6.benningen.midokura.de
      - dfa-16-3e-8a-54-98.soc6.benningen.midokura.de
      - dfa-16-3e-e1-66-b5.soc6.benningen.midokura.de
      - dfa-16-3e-fa-9e-80.soc6.benningen.midokura.de
      nova-compute-xen: []
- barclamp: horizon
  attributes:
    nova_instance: default
    keystone_instance: default
    database_instance: default
    db:
      password: IdHg6y4biBe7
  deployment:
    elements:
      horizon-server:
      - dfa-16-3e-12-25-6c.soc6.benningen.midokura.de
- barclamp: heat
  attributes:
    rabbitmq_instance: default
    database_instance: default
    stack_domain_admin_password: xPfRvxHJzKEr
    keystone_instance: default
    service_password: IrGQ9wV9c6M6
    auth_encryption_key: mr8Phg3I8NNAA8SEETiiqTAqzPnsrYV1z5lj
    db:
      password: Gp6xhLJHqlN9
  deployment:
    elements:
      heat-server:
      - dfa-16-3e-12-25-6c.soc6.benningen.midokura.de
EOF
""")

    run("""

sed -i 's,dfa-16-3e-12-25-6c.soc6.benningen.midokura.de,%s,g;' /root/atlas.yaml

sed -i 's,dfa-16-3e-23-bc-fd.soc6.benningen.midokura.de,%s,g;' /root/atlas.yaml
sed -i 's,dfa-16-3e-84-10-20.soc6.benningen.midokura.de,%s,g;' /root/atlas.yaml
sed -i 's,dfa-16-3e-8a-54-98.soc6.benningen.midokura.de,%s,g;' /root/atlas.yaml
sed -i 's,dfa-16-3e-e1-66-b5.soc6.benningen.midokura.de,%s,g;' /root/atlas.yaml
sed -i 's,dfa-16-3e-fa-9e-80.soc6.benningen.midokura.de,%s,g;' /root/atlas.yaml

""" % (
        controller,
        computes[0],
        computes[1],
        computes[2],
        computes[3],
        computes[4]))

    run("crowbar batch build </root/atlas.yaml")
