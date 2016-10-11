#!/bin/bash

for CHAIN in $(midonet-cli -e 'chain list' | grep -- "_ANTI_SPOOF" | awk '{print $2;}'); do
  midonet-cli -e "delete chain ${CHAIN}"
done

