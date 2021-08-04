from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
	
@app.route('/login')
def login():
	return render_template('login.html')
	#return('Login Page Here')
@app.route('/register')
def register():
	return render_template('register.html')
	#return('Register Page here')
    
@app.route('/adduser', methods= ['POST', 'GET'])
def adduser():
    if request.method == 'POST':
        try:
            uname = request.form['uname']
            psw = request.form['psw']
            
            with sql.connect("database.db") as c:
                cur = c.cursor()
                cur.execute("INSERT INTO users (username, password) VALUES (?,?)", (uname, psw) )
                c.commit();
                msg = "You have been succesfully registered!"
        except:
            c.rollback()
            msg = "Error in inserting user"
            
        finally:
            return render_template("result.html", msg=msg)
            c.close()
            
@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from users")
   
   rows = cur.fetchall();
   return render_template("list.html",rows = rows)


@app.route('/analytics')
def analyze():
	return render_template('analytics.html')
	#return('Analytics will be here')
    

@app.route('/userauth')
def userauth():
    return render_template('userauth.html')

if __name__ == '__main__':
    app.run(debug=True)
