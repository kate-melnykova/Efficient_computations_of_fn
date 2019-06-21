from flask import Flask
from flask import request
import factorial, compute_pi, compute_e
app = Flask(__name__)

@app.route("/")
def hello():
    print("Welcome to scientific computation")
@app.route("/compute", methods=['GET','POST'])
def implementation():
    print("Welcome to scientific computation")
    if request.method == 'POST':
        return get_the_input()
    else:
        return print_output()

def get_the_input():
    print("Input")
def print_output():
    print("Output")