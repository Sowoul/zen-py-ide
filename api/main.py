from flask import Flask, request, render_template, jsonify
import os

app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def index():
    temp = request.args.get("ans")
    print(temp)
    txt = ""
    try:
        with open('api/temp.py', 'r') as file:
            for i in file.readlines()[1:]:
                txt += f"{i[4:]}"
    except FileNotFoundError:
        txt = "File not found. Please ensure 'temp.py' exists."
    
    if not temp:
        return render_template('index.html', cringe="", prev=txt)
    return render_template('index.html', cringe=temp, prev=txt)

@app.route('/geta', methods=["POST", "GET"])
def get():
    data = request.form["data"]
    if not data:
        return jsonify({"status": "failure"})
    new_file = "api/temp"
    try:
        with open(f"{new_file}.py", 'w') as file:
            file.write('def main():\n')
            for i in data.split('\n'):
                file.writelines(f'    {i}\n')
    except IOError as e:
        return jsonify({"status": "failure", "message": str(e)})
    
    # Ensure to reload the module correctly
    import importlib
    import temp
    importlib.reload(temp)
    store = temp.main()
    return jsonify({'status': 'success', 'data': store})

if __name__ == "__main__":
    app.run()
