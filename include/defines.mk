
ALL = start \
			preflight $(SSHCONFIG) \
			instances antispoof \
			jumper \
			pingcheck connectcheck \
			hostname newrelic \
			crowbar \
			nodes \
			finish

PP = PYTHONPATH=$(PWD)/lib

STAGES = stages

TMPDIR = $(PWD)/tmp

BINDIR = $(PWD)/bin

PWCDIR = $(TMPDIR)/etc

SSHDIR = $(TMPDIR)/.ssh

SSHCONFIG = $(SSHDIR)/config

ifeq "$(CONFIGFILE)" ""
CONFIGFILE = $(PWD)/conf/atlas.yaml
endif

CC = CONFIGFILE="$(CONFIGFILE)"
TT = TMPDIR="$(TMPDIR)"
FS = --ssh-config-path=$(SSHCONFIG) --disable-known-hosts --user=root
FF = --fabfile $(STAGES)/$(@)/fabfile.py

FABRIC = $(CC) $(TT) $(PP) fab $(FS) $(FF) $(@)

