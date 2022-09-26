install: venv
	. venv/bin/activate; pip3 install -Ur requirements.txt

setupUbuntu:
	sudo systemctl start mongod

setupMac:
	brew services start mongodb-community@6.0
	
venv:
	test -d venv || python3 -m venv venv
	
clean:
	rm -rf venv
	find -iname "*.pyc" -delete