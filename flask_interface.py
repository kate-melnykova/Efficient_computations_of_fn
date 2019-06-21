from flask import Flask
from flask import request
from flask import render_template
import factorial, compute_pi, compute_e
app = Flask(__name__)

@app.route("/")
def hello():
    return "Welcome to scientific computation"

name = "User"
@app.route("/compute", methods=['GET','POST'])
def implementation():
    error = None
    if request.method == 'POST':
        if request.form['factorial']:
            return render_template('webpage.html',factorial=factorial)
        else:
            error = 'Invalid entry'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('webpage.html',factorial=None)#, error=error)


if __name__ == '__main__':
    app.run()