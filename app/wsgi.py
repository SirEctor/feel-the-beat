from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
	
@app.route('/login')
def login():
	#return render_template('login.html')
	return('Login Page Here')
@app.route('/register')
def register():
	#return render_template('register.html')
	return('Register Page here')
@app.route('/analytics')
def analyze():
	#return render_template('analytics.html')
	return('Analytics will be here')
if __name__ == '__main__':
    app.run(debug=True)
