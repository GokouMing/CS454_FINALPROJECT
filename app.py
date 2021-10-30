from flask import Flask, render_template, request
import Database
import SearchEngine

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def homePage():  # put application's code here
    if request.method == 'POST':
        query = request.form.get('inputWords')
        if not query:
            return 'ERROR 404'
        elif query is None:
            return '<h1>No Result<h1>'
        else:
            rel = Database.dataBaseSearch(query)
            return render_template('Result.html', query=rel)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run()
