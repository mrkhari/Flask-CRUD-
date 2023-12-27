from flask import Flask, render_template, url_for, redirect, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "12345"
app.config["MYSQL_DB"] = "flask"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

@app.route("/")
def home():
    con = mysql.connection.cursor()
    sql = "SELECT * FROM datas"
    con.execute(sql)
    res = con.fetchall()
    con.close()
    return render_template("home.html", datas=res)




# Insert
@app.route("/addusers", methods=['GET', 'POST'])
def addusers():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        city = request.form['city']
        con = mysql.connection.cursor()
        sql = "INSERT INTO datas(Name, Age, City) VALUES (%s, %s, %s)"
        con.execute(sql, [name, age, city])
        mysql.connection.commit()
        con.close()
        return redirect(url_for('home'))
    else:
    
        return render_template("addusers.html")

# Edit

@app.route("/edituser/<string:id>", methods=['GET', 'POST'])
def edituser(id):
    con = mysql.connection.cursor()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        city = request.form['city']
        sql = "UPDATE datas SET Name=%s, Age=%s, City=%s WHERE ID=%s"
        con.execute(sql, [name, age, city, id])
        mysql.connection.commit()
        con.close()
        return redirect(url_for("home"))

    sql = "SELECT * FROM datas WHERE ID=%s"
    con.execute(sql, [id])
    res = con.fetchone()
    con.close()
    return render_template("edituser.html", datas=res)

# Delete User

@app.route("/deleteuser/<string:id>", methods=['GET', 'POST'])
def deleteuser(id):
    con = mysql.connection.cursor()
    sql = "DELETE FROM datas WHERE ID=%s"
    con.execute(sql, [id])
    mysql.connection.commit()
    con.close()
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)