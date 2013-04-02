empty:

install:
	python setup.py install > install.log

clean:
	rm -r *.egg-info dist/ build/
