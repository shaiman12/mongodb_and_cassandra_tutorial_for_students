install: venv
	. venv/bin/activate; pip3 install -Ur requirements.txt

setupUbuntu:
	sudo systemctl start mongod
	sudo systemctl start cassandra

setupMac:
	brew services start mongodb-community@6.0
	brew services start cassandra
	
venv:
	test -d venv || python3 -m venv venv

tearDown_ubuntu:
	sudo systemctl stop mongod
	sudo systemctl stop cassandra

tearDown_mac:
	brew services stop mongod
	brew services stop cassandra

clean:
	rm -rf venv
	find -iname "*.pyc" -delete