
from fabric.api import run

class Network(object):
    def __init__(self):
        return

    @classmethod
    def rescue(cls, ipaddress):
        run("""

IPADDRESS="192.168.1.%s"

cat >/root/ipaddress.sh<<EOF
#!/bin/bash
while(true); do
    ifconfig eth1 ${IPADDRESS}/24
    route add -net 192.168.9.0/24 gw 192.168.1.1
done
EOF

chmod 0755 /root/ipaddress.sh

screen -d -m /root/ipaddress.sh

for i in $(seq 1 10); do echo -n '.'; done

sync

""" % ipaddress.split('.')[3])

    @classmethod
    def json(cls):
        return("""{
  "attributes": {
    "network": {
      "conduit_map": [
        {
          "conduit_list": {
            "intf0": {
              "if_list": [
                "1g1",
                "1g2"
              ]
            },
            "intf1": {
              "if_list": [
                "1g1",
                "1g2"
              ]
            },
            "intf2": {
              "if_list": [
                "1g1",
                "1g2"
              ]
            }
          },
          "pattern": "team/.*/.*"
        },
        {
          "conduit_list": {
            "intf0": {
              "if_list": [
                "?1g1"
              ]
            },
            "intf1": {
              "if_list": [
                "?1g2"
              ]
            },
            "intf2": {
              "if_list": [
                "?1g1"
              ]
            }
          },
          "pattern": "dual/.*/.*"
        },
        {
          "conduit_list": {
            "intf0": {
              "if_list": [
                "?1g1"
              ]
            },
            "intf1": {
              "if_list": [
                "?1g1"
              ]
            },
            "intf2": {
              "if_list": [
                "?1g1"
              ]
            }
          },
          "pattern": "single/.*/.*"
        },
        {
          "conduit_list": {
            "intf0": {
              "if_list": [
                "?1g1"
              ]
            },
            "intf1": {
              "if_list": [
                "1g1"
              ]
            },
            "intf2": {
              "if_list": [
                "1g1"
              ]
            }
          },
          "pattern": ".*/.*/.*"
        },
        {
          "conduit_list": {
            "intf0": {
              "if_list": [
                "1g1"
              ]
            },
            "intf1": {
              "if_list": [
                "?1g1"
              ]
            },
            "intf2": {
              "if_list": [
                "?1g1"
              ]
            }
          },
          "pattern": "mode/1g_adpt_count/role"
        }
      ],
      "enable_rx_offloading": false,
      "enable_tx_offloading": false,
      "interface_map": [
        {
          "bus_order": [
            "0000:00/0000:00:01",
            "0000:00/0000:00:03"
          ],
          "pattern": "PowerEdge R610"
        },
        {
          "bus_order": [
            "0000:00/0000:00:01.1/0000:01:00.0",
            "0000:00/0000:00:01.1/0000.01:00.1",
            "0000:00/0000:00:01.0/0000:02:00.0",
            "0000:00/0000:00:01.0/0000:02:00.1"
          ],
          "pattern": "PowerEdge R620"
        },
        {
          "bus_order": [
            "0000:00/0000:00:01",
            "0000:00/0000:00:03"
          ],
          "pattern": "PowerEdge R710"
        },
        {
          "bus_order": [
            "0000:00/0000:00:04",
            "0000:00/0000:00:02"
          ],
          "pattern": "PowerEdge C6145"
        },
        {
          "bus_order": [
            "0000:00/0000:00:1c",
            "0000:00/0000:00:07",
            "0000:00/0000:00:09",
            "0000:00/0000:00:01"
          ],
          "pattern": "PowerEdge C2100"
        },
        {
          "bus_order": [
            "0000:00/0000:00:01",
            "0000:00/0000:00:03",
            "0000:00/0000:00:07"
          ],
          "pattern": "C6100"
        },
        {
          "bus_order": [
            "0000:00/0000:00:01",
            "0000:00/0000:00:02"
          ],
          "pattern": "product"
        }
      ],
      "mode": "single",
      "networks": {
        "admin": {
          "add_bridge": false,
          "broadcast": "192.168.124.255",
          "conduit": "intf0",
          "mtu": 1500,
          "netmask": "255.255.255.0",
          "ranges": {
            "admin": {
              "end": "192.168.124.11",
              "start": "192.168.124.10"
            },
            "dhcp": {
              "end": "192.168.124.80",
              "start": "192.168.124.21"
            },
            "host": {
              "end": "192.168.124.160",
              "start": "192.168.124.101"
            },
            "switch": {
              "end": "192.168.124.250",
              "start": "192.168.124.241"
            }
          },
          "router": "192.168.124.1",
          "router_pref": 10,
          "subnet": "192.168.124.0",
          "use_vlan": false,
          "vlan": 100
        },
        "bmc": {
          "add_bridge": false,
          "broadcast": "192.168.124.255",
          "conduit": "bmc",
          "netmask": "255.255.255.0",
          "ranges": {
            "host": {
              "end": "192.168.124.240",
              "start": "192.168.124.162"
            }
          },
          "subnet": "192.168.124.0",
          "use_vlan": false,
          "vlan": 100
        },
        "bmc_vlan": {
          "add_bridge": false,
          "broadcast": "192.168.124.255",
          "conduit": "intf2",
          "netmask": "255.255.255.0",
          "ranges": {
            "host": {
              "end": "192.168.124.161",
              "start": "192.168.124.161"
            }
          },
          "subnet": "192.168.124.0",
          "use_vlan": false,
          "vlan": 100
        },
        "nova_fixed": {
          "add_bridge": false,
          "add_ovs_bridge": false,
          "bridge_name": "br-fixed",
          "broadcast": "192.168.123.255",
          "conduit": "intf1",
          "netmask": "255.255.255.0",
          "ranges": {
            "dhcp": {
              "end": "192.168.123.254",
              "start": "192.168.123.1"
            }
          },
          "router": "192.168.123.1",
          "router_pref": 20,
          "subnet": "192.168.123.0",
          "use_vlan": false,
          "vlan": 500
        },
        "nova_floating": {
          "add_bridge": false,
          "add_ovs_bridge": false,
          "bridge_name": "br-public",
          "broadcast": "192.168.126.255",
          "conduit": "intf1",
          "netmask": "255.255.255.128",
          "ranges": {
            "host": {
              "end": "192.168.126.254",
              "start": "192.168.126.129"
            }
          },
          "subnet": "192.168.126.128",
          "use_vlan": false,
          "vlan": 300
        },
        "os_sdn": {
          "add_bridge": false,
          "broadcast": "192.168.130.255",
          "conduit": "intf1",
          "netmask": "255.255.255.0",
          "ranges": {
            "host": {
              "end": "192.168.130.254",
              "start": "192.168.130.10"
            }
          },
          "subnet": "192.168.130.0",
          "use_vlan": false,
          "vlan": 400
        },
        "public": {
          "add_bridge": false,
          "broadcast": "192.168.126.255",
          "conduit": "intf1",
          "netmask": "255.255.255.0",
          "ranges": {
            "host": {
              "end": "192.168.126.127",
              "start": "192.168.126.2"
            }
          },
          "router": "192.168.126.1",
          "router_pref": 5,
          "subnet": "192.168.126.0",
          "use_vlan": false,
          "vlan": 300
        },
        "storage": {
          "add_bridge": false,
          "broadcast": "192.168.125.255",
          "conduit": "intf1",
          "mtu": 1500,
          "netmask": "255.255.255.0",
          "ranges": {
            "host": {
              "end": "192.168.125.239",
              "start": "192.168.125.10"
            }
          },
          "subnet": "192.168.125.0",
          "use_vlan": false,
          "vlan": 200
        }
      },
      "start_up_delay": 30,
      "teaming": {
        "mode": 1
      }
    }
  }
}""")

