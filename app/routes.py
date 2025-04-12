from app import app

@app.route('/')
@app.route('/index')
@app.route('/index1')
def index():
    return "Hello, World!"
