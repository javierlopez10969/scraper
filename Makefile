run:
	uvicorn app.main:app --reload
virtual:
	virtualenv -p python3.9 env
	source ./env/bin/activate
install:
	pip install -r requirements.txt
kill:
	kill -9 $(lsof -ti:8000)
verify:
	pycodestyle app
test:
	python3 manage.py test