#
# Makefile - build wrapper for pyp on CentPOS 7
#
#	git clone RHEL 7 SRPM building tools from
#	https://github.com/nkadel/[package] into designated
#	PYPPKGS below
#
#	Set up local 

# Rely on local nginx service poingint to file://$(PWD)/repo
#REPOBASE = http://localhost
REPOBASE = file://$(PWD)

# Buildable with only EPEL
EPELPKGS+=python-mock-srpm
EPELPKGS+=python-scripttest-srpm
EPELPKGS+=python-virtualenv-api-srpm/

PYPPKGS+=vex-srpm

# Requires vex
PYPPKGS+=pyp2rpm-srpm

REPOS+=pyp2rpmrepo/el/8
REPOS+=pyp2rpmrepo/el/9

REPODIRS := $(patsubst %,%/x86_64/repodata,$(REPOS)) $(patsubst %,%/SRPMS/repodata,$(REPOS))

# No local dependencies at build time
CFGS+=pyp2rpmrepo-8-x86_64.cfg
CFGS+=pyp2rpmrepo-9-x86_64.cfg

# Link from /etc/mock
MOCKCFGS+=centos-stream+epel-8-x86_64.cfg
MOCKCFGS+=centos-stream+epel-9-x86_64.cfg

all:: install
install:: $(CFGS) $(MOCKCFGS)
install:: $(REPODIRS)
install:: $(EPELPKGS)
install:: $(PYPPKGS)

build install clean getsrc build:: FORCE
	@for name in $(EPELPKGS) $(PYPPKGS); do \
	     (cd $$name; $(MAKE) $(MFLAGS) $@); \
	done  

# It is sometimes useful to build up all the more independent EPEL packages first
epel:: $(EPELPKGS)

# Actually build in directories
$(EPELPKGS):: FORCE
	(cd $@; $(MAKE) $(MLAGS) install)

$(PYPPKGS):: FORCE
	(cd $@; $(MAKE) $(MLAGS) install)

repos: $(REPOS) $(REPODIRS)
$(REPOS):
	install -d -m 755 $@

.PHONY: $(REPODIRS)
$(REPODIRS): $(REPOS)
	@install -d -m 755 `dirname $@`
	/usr/bin/createrepo_c `dirname $@`

.PHONY: cfg cfgs
cfg cfgs:: $(CFGS) $(MOCKCFGS)

$(MOCKCFGS)::
	@echo Generating $@ from /etc/mock/$@
	@echo "include('/etc/mock/$@')" | tee $@
	@echo "config_opts['dnf_vars'] = { 'best': 'False' }" | tee -a $@
	@echo | tee -a $@

pyp2rpmrepo-8-x86_64.cfg: /etc/mock/centos-stream+epel-8-x86_64.cfg
	@echo Generating $@ from $?
	@echo "include('$?')" > $@
	@echo "config_opts['dnf_vars'] = { 'best': 'False' }" | tee -a $@
	@echo | tee -a $@
	@echo "config_opts['root'] = 'pyp2rpmrepo-{{ releasever }}-{{ target_arch }}'" | tee -a $@
	@echo "config_opts['dnf.conf'] += \"\"\"" | tee -a $@
	@echo '[repo]' | tee -a $@
	@echo 'name=repo' | tee -a $@
	@echo 'enabled=1' | tee -a $@
	@echo 'baseurl=$(REPOBASE)/pyp2rpmrepo/el/8/x86_64/' | tee -a $@
	@echo 'failovermethod=priority' | tee -a $@
	@echo 'skip_if_unavailable=False' | tee -a $@
	@echo 'metadata_expire=1' | tee -a $@
	@echo 'gpgcheck=0' | tee -a $@
	@echo '#cost=2000' | tee -a $@
	@echo '"""' | tee -a $@

pyp2rpmrepo-9-x86_64.cfg: /etc/mock/centos-stream+epel-9-x86_64.cfg
	@echo Generating $@ from $?
	@echo "include('$?')" > $@
	@echo "config_opts['dnf_vars'] = { 'best': 'False' }" | tee -a $@
	@echo | tee -a $@
	@echo "config_opts['root'] = 'pyp2rpmrepo-{{ releasever }}-{{ target_arch }}'" | tee -a $@
	@echo "config_opts['dnf.conf'] += \"\"\"" | tee -a $@
	@echo '[repo]' | tee -a $@
	@echo 'name=repo' | tee -a $@
	@echo 'enabled=1' | tee -a $@
	@echo 'baseurl=$(REPOBASE)/pyp2rpmrepo/el/9/x86_64/' | tee -a $@
	@echo 'failovermethod=priority' | tee -a $@
	@echo 'skip_if_unavailable=False' | tee -a $@
	@echo 'metadata_expire=1' | tee -a $@
	@echo 'gpgcheck=0' | tee -a $@
	@echo '#cost=2000' | tee -a $@
	@echo '"""' | tee -a $@

pyp2rpmrepo: pyp2rpmrepo.repo
pyp2rpmrepo.repo:: Makefile pyp2rpmrepo.repo.in
	if [ -s /etc/fedora-release ]; then \
		cat $@.in | \
			sed "s|@REPOBASEDIR@/|$(PWD)/|g" | \
			sed "s|/@RELEASEDIR@/|/fedora/|g" > $@; \
	elif [ -s /etc/redhat-release ]; then \
		cat $@.in | \
			sed "s|@REPOBASEDIR@/|$(PWD)/|g" | \
			sed "s|/@RELEASEDIR@/|/el/|g" > $@; \
	else \
		echo Error: unknown release, check /etc/*-release; \
		exit 1; \
	fi

pyp2rpmrepo.repo:: FORCE
	cmp -s /etc/yum.repos.d/$@ $@       

clean::
	find . -name \*~ -exec rm -f {} \;
	rm -f *.cfg
	rm -f *.out
	rm -f nginx/default.d/*.conf
	@for name in $(PYPPKGS); do \
	    $(MAKE) -C $$name clean; \
	done

distclean:
	rm -rf $(REPOS)

maintainer-clean:
	rm -rf $(PYPPKGS)

FORCE::
