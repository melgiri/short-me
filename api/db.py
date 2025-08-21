# import MySQLdb as mysql
import sqlite3
import os
import json

if os.environ.get("DOCKER") == "true":
    host = "0.0.0.0"
    port = 5000
else:
    f = open("config.json", "r")
    data = json.load(f)
    host = data["host"]
    port = data["port"]
    f.close()


pwd = os.popen("pwd").read().strip()

cnx = sqlite3.connect(
    database=os.path.join(pwd, "main.db"),
    check_same_thread=False
)

cursor = cnx.cursor()
