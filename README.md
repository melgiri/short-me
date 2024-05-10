# Short Me

<img src="static/logo.png" alt="short Me logo" width="100" height="100">

### Url Shortner

It is a python program which helps you to create and host short links

## Table of Contents

- [Installation](#installation)
- [Config](#config)
- [Usage](#usage)

## Installation

To install requirement run

`sh install.sh`

## Config

To begin go to `config.json` to edit basic config.

    {
        "signup": "true",
        "key" : "your key",
        "host-short" : "127.0.0.1",
        "port-short" : "5000",
        "db-host" : "your db-host",
        "db-user" : "your db-user",
        "db-pass" : "your db-pass",
        "db-name" : "your db-name"
    }

- Replce the `true` in front of signup to false when you are done adding accounts

- Replace `your key` with the key you want. It will be the encryption key.

- You can choose the host i.e. the ip and the port where it will run.

- Replace `your db-X` with your credentials

### Database config

- Sql commands to setup data base are found in db.sql

### Run

- Run the program --> Go to site --> /signup

- After this login

## Usage

- In main page `ID` refers to shorted link.
- If you want to delete a link type the id which you want to delete in section delete.
