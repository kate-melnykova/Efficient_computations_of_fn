import pandas as pd
from flask_table import Table, Col
from flask import Flask
from flask import request
from flask import render_template
from factorial import factorial
from compute_pi import compute_pi
from compute_e import compute_e



app = Flask(__name__)

registry = {'factorial':factorial, 'pi':compute_pi, 'e':compute_e}
computed = pd.DataFrame(columns=['ID', 'func_name','inp','accuracy','completed?'])
ID = 0

@app.route("/", methods=["POST","GET"])
def implementation():
    global ID, computed
    if request.method == 'POST':
        func_name = request.form["func_name"]
        inp_val = int(request.form['inp'])
        n_digits = int(request.form['n_digits'])

        computed.loc[computed.shape[0], :] = [ID, func_name, inp_val, n_digits, "In progress"]
        if computed.shape[0] > 10:
            computed = computed.iloc[1:,:].reset_index(drop=True)
        ID += 1

        [out_val, accuracy] = registry[func_name](inp_val, n_digits)
        out_val = str(out_val)
        computed.iloc[-1,4]="yes"
        #crop number if needed
        if len(out_val) > n_digits:
            if "." not in out_val[:n_digits]:
                out_val = out_val[:n_digits+1] + "e+" +str(len(out_val)-n_digits)
            else:
                out_val = out_val[:n_digits + 2]

        idx = 70
        while idx < len(out_val):
            out_val = out_val[:idx] + '\n ...' + out_val[idx:]
            idx += 70
        return render_template('webpage.html',tables=[computed.to_html(classes='data', header="true")],
                               inp=inp_val, func_name=func_name, out_val=out_val, accuracy=accuracy)
    else:
        return render_template('webpage.html',tables=[computed.to_html(classes='data', header="true")],
                               inp=None, func_name=None, out_val=None, accuracy=None)



if __name__ == '__main__':
    #execfile('modbusreginfo.py')
    app.run(host='localhost', port=5000, debug=True)#, threaded=True)
    #app.run()