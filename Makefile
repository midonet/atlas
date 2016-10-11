
#
# ゼウス
#

include include/defines.mk

all: $(ALL)

include include/targets.mk
include include/fabfiles.mk

ci: clean all

fabtargets:
	bin/mkfabtargets.sh > include/fabfiles.mk

preload: fabtargets
	make $(SSHCONFIG)

cleanssh:
	for IP in $(shell seq 1 254); do ssh-keygen -f "/home/agabert/.ssh/known_hosts" -R 192.168.1.$$IP 2>/dev/null 1>/dev/null; done
	for IP in $(shell seq 1 254); do ssh-keygen -f "/home/agabert/.ssh/known_hosts" -R 192.168.124.$$IP 2>/dev/null 1>/dev/null; done

#
# this is for developers only
#
REXEC = ssh suse@os001 -t -- make $(@)

antispoof:
	$(REXEC)

instances:
	$(REXEC)

wipe:
	$(REXEC)

