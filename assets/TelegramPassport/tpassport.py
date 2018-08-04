from flask import Flask, render_template, request, make_response, redirect
import tpassport_padding

app = Flask(__name__)


@app.route('/')
def index():
    return 'ok'


@app.route('/encrypt', methods=['POST'])
def enc():
    name = request.form['msg']
    name, padd = tpassport_padding.encrypt(name)
    if name is None:
        return "Padding Error"
    else:
        return name


@app.route('/decrypt', methods=['POST'])
def dec():
    name = request.form['msg']
    name = tpassport_padding.decrypt(name)
    if name is None:
        return "Padding Error"
    else:
        return name


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9999)
