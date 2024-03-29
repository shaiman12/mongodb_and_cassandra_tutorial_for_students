install: venv
	. venv/bin/activate; pip3 install -Ur requirements.txt

setupUbuntu:
	sudo service mongod start
	sudo systemctl enable cassandra.service
	sudo service cassandra start
	sudo cp cassandra.yaml /etc/cassandra/

setupMac:
	brew services start mongodb-community@6.0
	brew services start cassandra
	
venv:
	test -d venv || python3 -m venv venv

tearDown_ubuntu:
	sudo service cassandra stop
	sudo service mongod stop

tearDown_mac:
	brew services stop mongod
	brew services stop cassandra

run:
	@python3 src/wrapper.py

clean:
	rm -rf venv
	find -iname "*.pyc" -delete