#!/bin/bash

if ( !(apt list --installed 2>/dev/null | grep -q mongodb >/dev/null) ) ; then
    echo -e "\e[1;36mInstalling MongoDB\e[0m"
    sudo apt-get -y install gnupg
    wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
    sudo apt-get update
    sudo apt-get install -y mongodb-org
fi

if ( !(apt list --installed 2>/dev/null | grep -q cassandra >/dev/null) ) ; then
    echo -e "\e[1;36mInstalling Cassandra\e[0m"
    sudo apt install -y apt-transport-https
    sudo sh -c 'echo "deb http://www.apache.org/dist/cassandra/debian 40x main" > /etc/apt/sources.list.d/cassandra.list'
    wget -q -O - https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add -
    sudo apt update
    sudo apt -y install cassandra
fi

if ( !(systemctl list-units | grep -q mongod >/dev/null) ) ; then
    echo -e "\e[1;36mStarting Mongod service\e[0m"
    sudo service mongod start
fi

if ( !(systemctl list-units | grep -q cassandra >/dev/null) ) ; then
    echo -e "\e[1;36mEnabling Cassandra service\n"
    sudo systemctl enable cassandra.service
    sudo service cassandra start
    sudo chmod 777 /etc/cassandra/cassandra.yaml
    sudo cp cassandra.yaml /etc/cassandra/
    echo -ne "Booting up Cassandra Server"
    sleep 2
    echo -ne "."
    sleep 2
    echo -ne "."
    sleep 2
    echo -ne ".\e[0m\n"
    sleep 2
fi

echo -e "\e[1;36mSetup complete\n"
echo -ne "Starting tutorial"
sleep 1
echo -ne "."
sleep 1
echo -ne "."
sleep 1
echo -ne ".\e[0m\n\n"
sleep 1
make
make run