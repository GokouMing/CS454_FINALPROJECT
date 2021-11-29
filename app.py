from flask import Flask, render_template, request
import searchEngine
import autoComplete
import re

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
        ad1 = request.form.get(r'class')
        ad2 = request.form.get(r'quality')
        ad3 = request.form.get(r'grade')
        # This flag uses binary to know which advanced search options were used ex. ad1 + ad2 = 3, ad3 + ad2 = 6
        adFlag = 0
        if(ad1 != None):
            if(len(ad1) > 0):
                adFlag = 1
        if(ad2 != None):
            if(len(ad2) > 0):
                adFlag += 2
        if(ad3 != None):
            if(len(ad3) > 0):
                adFlag += 4              
        print(ad1, ad2, ad3)
        print(adFlag)
        if not query:
            return render_template('Index.html')
        else:
            rel, costtime = searchEngine.querySearch(query)
            if not rel:
                return '<h1>No Result<h1>'
            else:
                groups = []
                for i in range(0, len(rel)):
                    flag = 0
                    for j in range(0, len(groups)):
                        if(rel[i][0] in groups[j][0][0]):
                            groups[j].append(rel[i])
                            flag = 1
                    # Only ran if the item is not in a group already
                    if(not flag):
                            if(adFlag == 0):
                                groups.append([rel[i]])
                            # Class
                            elif(adFlag == 1):
                                #print(ad1)
                                #print(rel[i])
                                if(ad1 in rel[i][5]):
                                    groups.append([rel[i]])
                            # Quality
                            elif(adFlag == 2):
                                #print(ad2)
                                #print(rel[i])
                                if(ad2 in rel[i][2]):
                                    groups.append([rel[i]])
                            # Quality & Class
                            elif(adFlag == 3):
                                #print(ad1)
                                #print(rel[i][2])
                                if(ad1 in rel[i][5]):
                                    if(ad2 in rel[i][2]):
                                        groups.append([rel[i]])
                            # Grade
                            elif(adFlag == 4):
                                #print(ad1)
                                #print(rel[i])
                                if(rel[i][3] != None):
                                    if(ad3 in rel[i][3]):
                                        groups.append([rel[i]])
                            # Class & Grade
                            elif(adFlag == 5):
                                #print(ad1)
                                #print(rel[i])
                                if(rel[i][3] != None):
                                    if(ad1 in rel[i][5]):
                                        if(ad3 in rel[i][3]):
                                            groups.append([rel[i]])
                            # Quality & Grade
                            elif(adFlag == 6):
                                print(ad1)
                                print(rel[i])
                                if(rel[i][3] != None):
                                    if(ad2 in rel[i][2]):
                                        if(ad3 in rel[i][3]):
                                            groups.append([rel[i]])
                            # Class & Quality & Grade
                            elif(adFlag == 7):
                                print(ad1)
                                print(rel[i])
                                if(rel[i][3] != None):
                                    if(ad1 in rel[i][5]):
                                        if(ad2 in rel[i][2]):
                                            if(ad3 in rel[i][3]):
                                                groups.append([rel[i]])
                return render_template('Result.html', results=groups, searchquery=query, costTime=round(costtime, 5),
                                   number=len(groups), similar_query1=query, similar_query2=query)
    elif request.method == 'GET':
        auto = autoComplete.autoComplete()
        auto = fliterList(auto)
        return render_template('Index.html', languages=auto)
    else:
        return render_template('Index.html')


@app.route('/result', methods=['POST', 'GET'])
def resultPage():  # put application's code here
    if request.method == 'POST':
        query = request.form.get(r'inputWords')
        if not query:
            return render_template('index.html')
        else:
            rel, costtime = searchEngine.querySearch(query)
            return render_template('temresult.html', results=rel, searchquery=query, costTime=round(costtime, 5),
                                   number=len(rel))
    elif request.method == 'GET':
        auto = autoComplete.autoComplete()
        auto = fliterList(auto)
        return render_template('index.html', languages=auto)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run()
