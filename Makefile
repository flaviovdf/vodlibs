# Simple makefile

PYTHON ?= python
NOSETESTS ?= nosetests

all: test

clean:
	find . -name "*.pyc" | xargs rm -f

test: clean
	$(NOSETESTS)

trailing-spaces: 
	find -name "*.py" | xargs sed 's/^M$$//'
