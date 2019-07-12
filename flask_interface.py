import pandas as pd

from flask import Flask
from flask import request
from flask import render_template
from factorial import factorial
from compute_pi import compute_pi
from compute_e import compute_e


app = Flask(__name__)

registry = {'factorial': factorial, 'pi': compute_pi, 'e': compute_e}
tables = []
ID = 0


@app.route("/", methods=["POST", "GET"])
def implementation():
    global ID, tables
    if request.method == 'POST':
        func_name = request.form["func_name"]
        inp_val = int(request.form['inp'])
        n_digits = int(request.form['n_digits'])

        tables.append([ID, func_name, inp_val, n_digits, "Computing...", "", ""])
        if len(tables) > 10:
            del tables[0]
        id_loc = ID
        ID += 1

        [out_val, accuracy] = registry[func_name](inp_val, n_digits)
        out_val = str(out_val)
        tables[-1][4] = "yes"

        # crop number if needed
        if len(out_val) > n_digits:
            if "." not in out_val[:n_digits]:
                out_val = out_val[:n_digits+1] + "E+" + str(len(out_val)-n_digits)
            else:
                out_val = out_val[:n_digits + 2]

        idx = 70
        while idx < len(out_val):
            out_val = out_val[:idx] + '\n ...' + out_val[idx:]
            idx += 70

        #find row with ID = id_loc
        for i in range(len(tables)):
            found = tables[i][0] == id_loc
            if found:
                break
        if found:
            tables[i][5] = out_val
            tables[i][6] = accuracy

        return render_template('webpage.html', tables=tables,
                               inp=inp_val, func_name=func_name, out_val=out_val, acc=accuracy)
    else:
        return render_template('webpage.html', tables=tables,
                               inp=None, func_name=None, out_val=None, acc=None)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)