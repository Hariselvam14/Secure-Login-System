from flask import Flask, request, redirect, session
import bcrypt

app = Flask(__name__)
app.secret_key = "mysecretkey"

# Temporary database
users = {}

# Home page
@app.route('/')
def home():
    if 'user' in session:
        return f"Welcome {session['user']}! <br><a href='/logout'>Logout</a>"
    return """
    <h2>Secure Login System</h2>
    <a href='/register'>Register</a><br>
    <a href='/login'>Login</a>
    """

# Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check existing user
        if username in users:
            return "User already exists!"

        # Hash password
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        users[username] = hashed_password

        return "Registration Successful! <a href='/login'>Login</a>"

    return '''
    <h3>Register</h3>
    <form method="post">
        Username: <input type="text" name="username"><br><br>
        Password: <input type="password" name="password"><br><br>
        <input type="submit" value="Register">
    </form>
    '''

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and bcrypt.checkpw(password.encode(), users[username]):
            session['user'] = username
            return redirect('/')

        return "Invalid Username or Password"

    return '''
    <h3>Login</h3>
    <form method="post">
        Username: <input type="text" name="username"><br><br>
        Password: <input type="password" name="password"><br><br>
        <input type="submit" value="Login">
    </form>
    '''

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

# Run app
if __name__ == "__main__":
    app.run(debug=True)
