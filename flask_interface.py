import pandas as pd
from flask_table import Table, Col
from flask import Flask
from flask import request
from flask import render_template
from factorial import factorial
from compute_pi import compute_pi
from compute_e import compute_e


app = Flask(__name__)


# Declare your table
class ItemTable(Table):
    Id = Col('ID')
    func_name = Col('Function name')
    inp = Col('Argument')
    n_digits = Col('Number of digits of interest')
    view = Col('Completed?')


# Get some objects
class Item:
    def __init__(self, info):
        self.Id = info[0]
        self.func_name = info[1]
        self.inp = info[2]
        self.n_digits = info[3]
        self.view = info[4]


registry = {'factorial':factorial, 'pi':compute_pi, 'e':compute_e}
computed = pd.DataFrame(columns=["ID", "func_name", "inp", "n_digits", "computed?", "out_val", "accuracy"])
tables = ItemTable([Item(row) for row in computed.values.tolist()])
ID = 0


@app.route("/", methods=["POST","GET"])
def implementation():
    global ID, computed, tables
    if request.method == 'POST':
        func_name = request.form["func_name"]
        inp_val = int(request.form['inp'])
        n_digits = int(request.form['n_digits'])

        computed.loc[computed.shape[0]] = [ID, func_name, inp_val, n_digits, "In progress", "", ""]
        print(computed)
        if computed.shape[0] > 10:
            computed = computed.iloc[1 :: ].reset_index(drop=True)
        ID += 1
        tables = ItemTable([Item(row) for row in computed.values.tolist()])

        [out_val, accuracy] = registry[func_name](inp_val, n_digits)
        out_val = str(out_val)
        computed.loc[computed.shape[0]-1, "computed?"] = "yes"

        #crop number if needed
        if len(out_val) > n_digits:
            if "." not in out_val[:n_digits]:
                out_val = out_val[:n_digits+1] + "E+" + str(len(out_val)-n_digits)
            else:
                out_val = out_val[:n_digits + 2]

        idx = 70
        while idx < len(out_val):
            out_val = out_val[:idx] + '\n ...' + out_val[idx:]
            idx += 70

        computed.iloc[-1, 5] = out_val
        computed.iloc[-1, 6] = accuracy
        tables = ItemTable([Item(row) for row in computed.values.tolist()])


        return render_template('webpage.html', tables=tables,
                               inp=inp_val, func_name=func_name, out_val=out_val, acc=accuracy)
    else:
        return render_template('webpage.html', tables=tables,
                               inp=None, func_name=None, out_val=None, acc=None)



if __name__ == '__main__':
    #execfile('modbusreginfo.py')
    app.run(host='localhost', port=5000, debug=True)#, threaded=True)
    #app.run()