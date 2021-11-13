from flask import Flask, render_template, request
import searchEngine
import autoComplete
import re
import itertools

app = Flask(__name__)


def fliterList(Lists):
    # tuple list to list
    lists = [item for items in Lists for item in items]
    newlist = []
    for list in lists:
        list = re.sub(r'\\', '', list)
        newlist.append(list)

    return newlist


@app.route('/', methods=['POST', 'GET'])
def homePage():  # put application's code here
    if request.method == 'POST':
        query = request.form.get(r'inputWords')
        if not query:
            return render_template('Index.html')
        else:
            rel = searchEngine.querySearch(query)
            if not rel:
                return '<h1>No Result<h1>'
            else:
                groups = []
                for i in range(0, len(rel)):
                    flag = 0
                    for j in range(0, len(groups)):
                        if(rel[i][1] in groups[j][0]):
                            groups[j].append(rel[i])
                            flag = 1
                    if(not flag):
                        groups.append([rel[i]])
                return render_template('Result.html', query=groups)
    elif request.method == 'GET':
        auto = autoComplete.autoComplete()
        auto = fliterList(auto)
        return render_template('Index.html', languages=auto)
    else:
        return render_template('Index.html')


if __name__ == '__main__':
    app.run()
