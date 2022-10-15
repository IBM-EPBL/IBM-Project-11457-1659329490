from flask import Flask,redirect,url_for,render_template,request,session
import sqlite3 as sql

from requests import session

app=Flask(__name__)

@app.route('/home')
def home1():
    return render_template('home.html')

@app.route("/")
def home():
    return render_template('index.html')
@app.route("/about")
def about():
    return render_template('About.html')
@app.route("/login",methods=['POST','GET'])
def logIn():
    error=[]
    if request.method=='POST':
        try:
            name=request.form['name']
            password=request.form['password']
            with sql.connect("database.db") as con:
                cur=con.cursor()
                print(cur.execute("SELECT * from register").fetchall())
                p=cur.execute("SELECT * from register where name=? and password=?",(name,password)).fetchall()
                if len(p)!=0:
                    print("login success")
                    return render_template('Home.html')
                else:
                    error.append("enter the correct name and email")
                    return render_template('login.html',error=error) 
        except sql.Error as error:
            print(error)
            con.rollback()
        finally:
            con.close()

    return render_template('login.html')
@app.route("/signup",methods=['POST','GET'])
def SignUp():
    if request.method=='POST':
        
        try:
            name=request.form['name']
            email=request.form['email']
            password=request.form['password']
            with sql.connect("database.db") as con:
                cur=con.cursor()
                cur.execute("INSERT INTO register(name,email,password) values(?,?,?)",(name,email,password))
                print("successfully registered")
                con.commit()
            return render_template("login.html")
        except sql.Error as error:
            print(error)
            con.rollback()
        finally:
            con.close()
    return render_template('signup.html')
if __name__=='__main__':
    app.run(debug=True)