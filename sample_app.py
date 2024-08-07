from flask import Flask
from flask import request
from flask import render_template

sample = Flask(__name__)

DBHOST = 'NOT SET'
def getdb(targethost = ''):
    import MySQLdb
    if targethost == '':
        global DBHOST
        targethost = DBHOST
    return MySQLdb.connect(host=targethost,
                     user="devnetstudent",
                     passwd="pass",
                     db="products")

@sample.route("/")
def main():
    return render_template("index.html")

@sample.route("/test")
def test():
    return "You are calling me from "+request.remote_addr

@sample.route("/config")
def config():
    return render_template("config.html")

@sample.route("/get_config")
def get_config():
    global DBHOST
    return DBHOST

@sample.route("/config_action", methods=['GET', 'POST'])
def config_action():
    global DBHOST 
    DBHOST = request.args.get('dbhost')
    return "Saved database host as "+DBHOST

@sample.route("/products")
def products():
    db = getdb()

    cur = db.cursor()
    cur.execute("select * from products")

    output = ""
    for row in cur.fetchall():
        output = output +  str(row[0]) + " -- " + str(row[1]) + "<br />"

    db.close()
    return output


if __name__ == "__main__":
    sample.run(host="0.0.0.0", port=80)
