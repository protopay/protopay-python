upload:
	python setup.py sdist upload

install:
	python setup.py install

test:
	@python setup.py install && clear
	. venv/bin/activate; nosetests --rednose --with-cov --cov-config=.coveragerc --cov-report=html

venv:
	virtualenv venv
	. venv/bin/activate; pip install -r requirements.txt -r tests/requirements.txt
	echo 'alias pay="python -m protopay --auth=test_firstdata_xxxxxxxxxxxx --url https://protopay-staging.herokuapp.com/v1 "' >> venv/bin/activate
