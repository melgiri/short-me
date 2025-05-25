import MySQLdb as mysql
import os
import json

if os.environ.get("DOCKER") == "true":
    host = "0.0.0.0"
    port = 5000
    db_host = os.environ.get("db-host")
    db_user = "root"
    db_passd = os.environ.get("db-pass")
    db_name = os.environ.get("db-name")
else:
    f = open("config.json", "r")
    data = json.load(f)
    host = data["host"]
    port = data["port"]
    db_host = data["db-host"]
    db_user = data["db-user"]
    db_passd = data["db-pass"]
    db_name = data["db-name"]
    f.close()


cnx = mysql.connect(
    host=db_host,
    user=db_user,
    password=db_passd,
    database=db_name
)

cursor = cnx.cursor()
