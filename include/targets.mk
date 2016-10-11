
$(TMPDIR):
	mkdir -pv $(TMPDIR)

$(SSHDIR):
	mkdir -pv $(SSHDIR)

.PHONY: $(SSHCONFIG)
$(SSHCONFIG): $(SSHDIR)
	$(PP) stages/sshconfig/bin/sshconfig.py "$(CONFIGFILE)" "$(@)"

preflight:
	@which fab 1>/dev/null 2>/dev/null

start: $(TMPDIR)
	@date > $(TMPDIR)/.START

finish: $(TMPDIR)
	@date > $(TMPDIR)/.FINISH

clean:
	rm -rfv $(TMPDIR)

