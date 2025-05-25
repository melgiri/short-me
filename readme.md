<h1 style='font-size: 50px;'>SHORT ME</h1>

<img src='short-me-web/static/logo.png' height='150px'>

## This is a python based program which helps to make short links. i.e. It is a `link shortner`

### Download it by

`git clone git@github.com:melgiri/short-me.git`

`cd short-me`

## Config

### If you want to use Docker(recommended) see [Docker config](#docker-config)

### If you want to setup Manually see [Manual config](#manual-config)

# Docker-config

<ul style='font-size:20px'>

* Open `config.json`

    In place of yoursecret in `"sign" : "yoursecret"` replace with your secret key

* Open `docker-compose.yaml` and replace `ROOT_PASS` with the password for root user in database.

* Run `docker-compose up -d` to start the application

</ul>

# Manual-config

<ul style='font-size:20px'>

* Open `config.json`

    In place of yoursecret in `"sign" : "yoursecret"` replace with your secret key

    `"host": "host-ip"` host ip to your host ip address

    `"port": "host-port"` host port to the port of your host in which service runs

    `"db-host" : "db-host"` db-host to data base ip address

    `"db-user" : "db-user"` db-user to user of database (like root)

    `"db-pass" : "db-pass"` db-pass to password of the given user for database

* To install required packages run `pip install short-me-web/requirements.txt`

    It may show `error: externally-managed-environment` then follow then create a virtual environment. 

* Run `setup.py`

* Finally run the `main.py` to start the server

</ul>
