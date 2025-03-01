from flask import Flask, render_template

#initialize app
app = Flask(__name__)

#route to home page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

#starting website
if __name__ == '__main__':
    app.run(debug=True)