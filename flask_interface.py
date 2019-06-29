from flask import Flask
from flask import request
from flask import render_template
from factorial import factorial
from compute_pi import compute_pi
from compute_e import compute_e
app = Flask(__name__)

@app.route("/", methods=["POST","GET"])
def implementation():
    if request.method == 'POST':
        func_name = request.form["func_name"]
        if func_name == "factorial":
            inp_val = int(request.form['inp'])
            factorial_val = str(factorial(inp_val))
            n_digits = int(request.form['n_digits'])
            if len(factorial_val) > n_digits:
                factorial_val = factorial_val[:n_digits+1] + "e+" +str(len(factorial_val)-n_digits)
            idx = 70
            while idx < len(factorial_val):
                factorial_val = factorial_val[:idx] + '\n ...' + factorial_val[idx:]
                idx += 70
            return render_template('webpage.html',inp=inp_val, func_name="factorial", out_val=factorial_val)
        elif func_name == "pi":
            time_limit = int(request.form['inp'])
            n_digits = int(request.form['n_digits'])
            pi_val, accuracy = compute_pi(time_limit,n_digits+2)
            pi_val = str(pi_val)
            idx = 70
            while idx < len(pi_val):
                pi_val = pi_val[:idx] + '\n ...' + pi_val[idx:]
                idx += 70
            return render_template('webpage.html', inp=time_limit, func_name="pi", out_val=pi_val, acc=str(accuracy-1))
        elif func_name == "e":
            time_limit = int(request.form['inp'])
            n_digits = int(request.form['n_digits'])
            e_val = str(compute_e(time_limit, n_digits + 2))
            idx = 70
            while idx < len(e_val):
                e_val = e_val[:idx] + '\n ...' + e_val[idx:]
                idx += 70
            # we keep n_digits + 1 place for floating point + 1 for 2
            return render_template('webpage.html', inp=time_limit, func_name="e", out_val=e_val)
        return render_template('webpage.html',inp=None, func_name=None, out_val=None)
    else:
        return render_template('webpage.html', inp=None, func_name=None, out_val=None)



if __name__ == '__main__':
    #execfile('modbusreginfo.py')
    app.run(host='localhost', port=5000, debug=True)#, threaded=True)
    #app.run()