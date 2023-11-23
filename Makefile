DEST := /Volumes/NO\ NAME

STEPS := 20
MIN := 0.1
MAX := 2.0
SECS := 10 60 300 900
FILES := $(foreach step, $(STEPS), $(foreach sec, $(SECS), vibrate-$(step)-$(sec)s-$(MIN)-$(MAX)mm.gcode))

all: $(FILES)

clean:
	rm -f vibrate-*-*-*-*.gcode

card-clean:
	rm -f $(DEST)/vibrate-*.gcode

copy: card-clean all
	cp *.gcode $(DEST) && diskutil eject $(DEST)

test:
	python3 -m unittest discover -p 'test_*.py' -v

# vibrate-50-60s-0.1-2.0mm.gcode
vibrate-%.gcode: generate.py
	$(eval temp := $(subst -, ,$*))
	$(eval steps := $(word 1, $(temp)))
	$(eval secs := $(subst s,,$(word 2, $(temp))))
	$(eval min := $(word 3, $(temp)))
	$(eval max := $(subst mm,,$(word 4, $(temp))))
	python3 generate.py -t $(steps) -n $(min) -x $(max) -s $(secs) -o $@

.PHONY: test clean card-clean copy
