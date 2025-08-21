<h1 style='font-size: 50px;'>SHORT ME</h1>

<img src='static/logo.svg' height='150px'>

## This is a python based program which helps to host own short links. i.e. It is a `link shortner`


## Config

### If you want to use Docker see [Docker config](#docker-config)

### If you want to setup Manually see [Manual config](#manual-config)

### To see General Configaration click [General config](#general-config)

# Docker config

<ul style='font-size:20px'>

* Run `docker build -t name_of_image .`

* To run the container `docker run -d -p host_port:5000 --name name_of container name_of_image`

* <b>NOTE</B>:if you want to keep a backup of your database add `-v "$PWD"/main.db:/root/main.db` to the above command.

</ul>

# Manual config

<ul style='font-size:20px'>

* Open `config.json`

    In place of yoursecret in `"sign" : "yoursecret"` replace with your secret key

    `"host": "host-ip"` host ip to your host ip address

    `"port": "host-port"` host port to the port of your host in which service runs


* To install required packages run `pip install -r requirements.txt`

    It may show `error: externally-managed-environment` then follow the instrection to create a virtual environment.

    * create a folder and `cd` into it.

    * `python3 -m venv name`

    * To activate it run `source bin/activate`

    - To deactivate it run `deactivate`

* Run `init.py`

* Finally run the `main.py` to start the server

</ul>

# General Config

<ul style='font-size:20px'>

* To change the configaration in `config.json` you can use `config.py`

* Type `python3 config.py`

* If you use nginx or cloudflare or something like that which comes before the main program, set the value of `ext-req` to `true` in config.json and set the value of `ext-hed` to the header which contains the ip addr of the client i.e. `X-Real-IP` in nginx. You can also do this using config.py

</ul>