from flask import Flask, render_template, request, redirect, url_for
import searchEngine
import autoComplete
import re
from flask_paginate import Pagination, get_page_args

app = Flask(__name__)



def fliterList(Lists):
    # tuple list to list
    lists = [item for items in Lists for item in items]
    newlist = []
    for list in lists:
        list = re.sub(r'\\', '', list)
        newlist.append(list)
    return newlist


def newList(list, offset=0, per_page=10):
    return list[offset: offset + per_page]


@app.route('/', methods=['POST', 'GET'])
def homePage():  # put application's code here
    if request.method == 'POST':
        query = request.form.get(r'inputWords')
        ad1 = request.form.get(r'class')
        if ad1:
            query = query + " " + ad1
        else:
            query = query + " " + 'None'
        ad2 = request.form.get(r'quality')
        if ad2:
            query = query + " " + ad2
        else:
            query = query + " " + 'None'
        ad3 = request.form.get(r'grade')
        if ad3:
            query = query + " " + ad3
        else:
            query = query + " " + 'None'
        print(query)
        return redirect(url_for("dataPage", query=query))

    elif request.method == 'GET':
        auto = autoComplete.autoComplete()
        auto = fliterList(auto)
        return render_template('Index.html', languages=auto)
    else:
        return render_template('Index.html')


@app.route('/dataPage/<query>')
def dataPage(query):
    list = query.split()
    print(list[:-1])
    print(list[:-2])
    print(list[:-3])

    print(len(list))
    searchE = 5
    if 'bm25' or 'tfidf' or 'view' or 'rel' in list:
        if "bm25" in list:
            searchE = 0
        elif "tfidf" in list:
            searchE = 1
        elif "view" in list:
            searchE = 2
        else:
            searchE = 5

    if len(list) <= 3:
        query = " ".join(list[:-1])
        ad1 = 'None'
        ad2 = 'None'
        ad3 = 'None'
        print(query)
    else:
        query = " ".join(list[:-3])
        ad3 = list[-1]
        ad2 = list[-2]
        ad1 = list[-3]

    adFlag = 0
    if ad1 != 'None':
        if len(ad1) > 0:
            adFlag = 1
    if ad2 != 'None':
        if len(ad2) > 0:
            adFlag += 2
    if ad3 != 'None':
        if len(ad3) > 0:
            adFlag += 4
    print(adFlag)
    if not query:
        return render_template('Index.html')
    else:
        if searchE == 0:
            print(f'bm25 Search:   {query}')
            rel, costtime = searchEngine.queryBM25Search(query)
        elif searchE == 1:
            print(f'wiki Search:   {query}')
            rel, costtime = searchEngine.queryWikiIdSearch(query)
        elif searchE == 2:
            print(f'Frequency Search:   {query}')
            rel, costtime = searchEngine.queryFrqsearch(query)
        else:
            print(f'Search:   {query}')
            rel, costtime = searchEngine.querySearch(query)
        if not rel:
            return '<h1>No Result<h1>'
        else:
            groups = []
            for i in range(0, len(rel)):
                flag = 0
                for j in range(0, len(groups)):
                    if (rel[i][0] in groups[j][0][0]):
                        groups[j].append(rel[i])
                        flag = 1
                # Only ran if the item is not in a group already
                if not flag:
                    if adFlag == 0:
                        groups.append([rel[i]])
                    # Class
                    elif adFlag == 1:
                        if ad1 in rel[i][5]:
                            groups.append([rel[i]])
                    # Quality
                    elif adFlag == 2:
                        if ad2 in rel[i][2]:
                            groups.append([rel[i]])
                    # Quality & Class
                    elif adFlag == 3:
                        if ad1 in rel[i][5]:
                            if ad2 in rel[i][2]:
                                groups.append([rel[i]])
                    # Grade
                    elif adFlag == 4:
                        if rel[i][3] != None:
                            if ad3 in rel[i][3]:
                                groups.append([rel[i]])
                    # Class & Grade
                    elif adFlag == 5:
                        if rel[i][3] != None:
                            if ad1 in rel[i][5]:
                                if ad3 in rel[i][3]:
                                    groups.append([rel[i]])
                    # Quality & Grade
                    elif adFlag == 6:
                        if rel[i][3] != None:
                            if ad2 in rel[i][2]:
                                if ad3 in rel[i][3]:
                                    groups.append([rel[i]])
                    # Class & Quality & Grade
                    elif adFlag == 7:
                        if rel[i][3] != None:
                            if ad1 in rel[i][5]:
                                if ad2 in rel[i][2]:
                                    if ad3 in rel[i][3]:
                                        groups.append([rel[i]])

            page, per_page, offset = get_page_args(page_parameter='page',
                                                   per_page_parameter='per_page')
            total = len(groups)
            groups = newList(groups, offset=offset, per_page=per_page)
            pagination = Pagination(page=page,
                                    per_page=per_page,
                                    offset=offset,
                                    total=total,
                                    css_framework='foundation',
                                    record_name='groups')

            return render_template('Result.html', results=groups, searchquery=query, costTime=round(costtime, 5),
                                   number=total, similar_query1=query, similar_query2=query,
                                   pagination=pagination, page=page, per_page=per_page)


@app.route('/results')
def resultPage():  # put application's code here
    query = request.args.get('query')
    sortby = request.args.get('order')

    if not sortby:
        query = query + " " + "rel"
    else:
        query = query + " " + sortby

    return redirect(url_for("dataPage", query=query))


if __name__ == '__main__':
    app.run()
