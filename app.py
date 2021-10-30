from flask import Flask, render_template, request
import searchEngine
import autoComplete
import re

app = Flask(__name__)


def fliterList(Lists):
    # tuple list to list
    lists = [item for items in Lists for item in items]
    return lists


@app.route('/', methods=['POST', 'GET'])
def homePage():  # put application's code here
    if request.method == 'POST':
        query = request.form.get('inputWords')
        if not query:
            return render_template('index.html')
        else:
            rel = searchEngine.querySearch(query)
            if not rel:
                return '<h1>No Result<h1>'
            else:
                return render_template('Result.html', query=rel)
    elif request.method == 'GET':
        auto = autoComplete.autoComplete()
        auto = fliterList(auto)
        return render_template('index.html', languages=auto)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run()
