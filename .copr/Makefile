.PHONY: all srpm
TARGET := $(notdir $(CURDIR))

all: srpm

srpm: $(TARGET).spec /usr/bin/spectool
	spectool -g $<
	rpmbuild -bs $< --define "_sourcedir $(PWD)" --define "_srcrpmdir $(outdir)"

# mock -r epel-9-x86_64 *.src.rpm

/usr/bin/spectool:
	dnf install -y rpmdevtools
