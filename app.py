from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def HomePage():  # put application's code here
    return render_template('Index.html')


if __name__ == '__main__':
    app.run()
