from flask import Flask, request, render_template,jsonify
from uuid import uuid4
import sys
import os
app = Flask(__name__)

@app.route('/', methods=  ["POST", "GET"])
def index():
    temp = request.args.get("ans")
    print(temp)
    txt=""
    with open('temp.py' , 'r') as file:
        for i in file.readlines()[1:]:
            txt+= f"{i[4:]}"
    file.close()
    if not temp:
        return render_template('index.html' , cringe=  "", prev= txt)
    return render_template('index.html' ,cringe = temp , prev=txt)

@app.route('/geta', methods = ["POST", "GET"])
def get():
    data  = request.form["data"]
    if not data:
        return jsonify({"status" : "failure"})
    new_file = "temp"
    with open(f"{new_file}.py" , 'w') as file:
        file.write('def main():\n')
        for i in data.split('\n'):
            file.writelines(f'    {i}\n')
    import temp
    store=temp.main()
    return jsonify({'status' : 'success' , 'data' : store})
if __name__=='__main__":
    app.run(debug=True)
