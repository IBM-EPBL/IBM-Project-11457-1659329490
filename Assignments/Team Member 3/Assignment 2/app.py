from flask import Flask,redirect,url_for,render_template,request
import sqlite3 as sql

app=Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')
@app.route("/about")
def about():
    return render_template('about.html')
@app.route("/signin",methods=['POST','GET'])
def sign_in():
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
                    return render_template('index.html')
                else:
                    error.append("enter the correct name and email")
                    return render_template('sign in.html',error=error) 
        except sql.Error as error:
            print(error)
            con.rollback()
        finally:
            con.close()

    return render_template('sign in.html')
@app.route("/signup",methods=['POST','GET'])
def sign_up():
    if request.method=='POST':
        
        try:
            name=request.form['name']
            email=request.form['email']
            password=request.form['password']
            with sql.connect("database.db") as con:
                cur=con.cursor()
                cur.execute("INSERT INTO register(name,email,password) values(?,?,?)",(name,email,password))
                print("successfully")
                con.commit()
            return render_template("sign in.html")
        except sql.Error as error:
            print(error)
            con.rollback()
        finally:
            con.close()
    return render_template('sign up.html')
if __name__=='__main__':
    app.run(debug=True)