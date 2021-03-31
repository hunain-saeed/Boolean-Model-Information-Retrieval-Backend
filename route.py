import bmr
import json
from operator import eq

precedence = {'or': 1, 'and': 2, 'not': 3 }

def hello_world():
    return json.dumps(bmr.i_index)

def findWord(word):
    try:
        return set(bmr.i_index[word])
    except:
        print('"%s" is not a key in the dictionary' % word)
        return set()


def oneWord(query, result):
    print("normal case", query)
    output = findWord(query[0])
    if output:
        # print(sorted(list(output)))
        result["result"] = sorted(list(output))
        return result
        # return json.dumps({"result": list(output), "error": ""})
    else:
        print("No document found!")
        result["error"] = "No document found!"
        return result
        # return json.dumps({"result": [], "error": "No document found!"})


def BooleanQuery(query, result):
    query = removePuncQuery(query.lower()).split()
    query = [bmr.ps.stem(word) for word in query]

    if len(query) == 1:
        return oneWord(query, result)

    post = infixToPostfix(query)
    output = []
    print("complex case", query)
    for p in post:
        if p not in precedence.keys():
            output.append(findWord(p))
        elif precedence[p] == 3:
            output.append(set(bmr.docid) - output.pop())
        elif precedence[p] == 2:    # and case
            a = output.pop()
            output.append(a.intersection(output.pop()))
        elif precedence[p] == 1:
            a = output.pop()
            output.append(a.union(output.pop()))

    if output[0]:
        # print(sorted(list(output)))
        result["result"] = sorted(list(output[0]))
        return result
        # return json.dumps({"result": list(output[0]), "error": ""})
    else:
        result["error"] = "No document found!"
        return result
        # return json.dumps({"result": [], "error": "No document found!"})

# 0 = term, 1=or, 2=and, 3=not
def isValidBQuery(test):
    try:
        position = [(1,2), (2,1), (3,1), (3,2), (0, 3)]
        if test[0] == 3 and (test[1] in precedence.values()):
            return False
        # adjecent values should not be euqal or same eg1. "term term" not allowed eg2. "and and" not allowed
        if any(map(eq, test, test[1:])):
            return False
        # query shouldn't start with these two word "and" "or" and shouldn't end with operator
        elif (test[0] == 1 or test[0] == 2) or (test[-1] == 1 or test[-1] == 2 or test[-1] == 3):
            return False
        # and or shouldn't be adjecent in any order 2nd "and, or" shouldn't come after "not"
        # 3rd "not" shouldn't come after term
        elif any(item in position for item in zip(test, test[1:])):
            return False
        else:
            return True
    except Exception as e:
        print(e)


def checkPrecedence(stack, q):
    try:
        if precedence[q] <= precedence[stack[-1]]:
            return True
        else:
            return False
    except KeyError: 
        return False


def infixToPostfix(query):
    op = []
    post = []
    # convert infix to post fix
    for q in query:
        if q not in precedence.keys():   # not operator then appent term
            post.append(q)
        else:
            while op and checkPrecedence(op, q):
                post.append(op.pop())
            op.append(q)
    while op:
        post.append(op.pop())
    
    return post


def findPWord(word):
    try:
        return bmr.p_index[word]
    except:
        return {}


def isInDoc(l1, l2, pval):
    for p1 in l1:
        for p2 in l2:
            if (abs(p1-p2)-1) == pval:
                return True
    return False


def ProximityQuery(w1, w2, pval, result):
    w1 = findPWord(w1)
    w2 = findPWord(w2)
    common = set(w1.keys()).intersection(set(w2.keys()))
    output = []
    if common:
        for docid in common:
            if isInDoc(w1[docid], w2[docid], pval):
                output.append(int(docid))
    if output:
        result["result"] = sorted(output)
        return result
    else:
        result["error"] = "No document found!"
        return result

def isValidPQuery(test):
    if test[-2] != '/':
        return False
    elif int(test[-1]) < 0:
        return False
    elif len(test) > 4:
        return False
    else:
        return True

def isInDoc3(words, docid, pval):
    for p1 in words[0][docid]:
        for p2 in words[1][docid]:
            for p3 in words[2][docid]:
                if (abs(p1-p2)-1) == pval and (abs(p2-p3)-1) == pval:
                    return True
    return False

def PhrasalQuery(query, result):
    if len(query) == 2:
        result = ProximityQuery(query[0], query[1], 0, result)
        return result
    if len(query) == 3:
        words = []
        for i in query:
            words.append(findPWord(i))
            
        common = set(words[0].keys()).intersection(set(words[1].keys()).intersection(set(words[2].keys())))
        output = []
        if common:
            for docid in common:
                if isInDoc3(words, docid, 0):
                    output.append(int(docid))
        if output:
            result["result"] = sorted(output)
            return result
    result["error"] = "No document found!"
    return result



# TODO return doc title also
def queryType(query):
    result = {"result": [], "error": ""}
    t = query.split()
    # For Proximity Queries
    if '&' in query:
        query = query.replace("&", " / ")
        query = removePuncQuery(query).split()
        query = [bmr.ps.stem(word) for word in query]
        if isValidPQuery(query):
            pval = int(query[-1])
            result = ProximityQuery(query[0], query[1], pval, result)
            return json.dumps(result)
        else:
            return json.dumps({"result": [], "error": "Invalid Query"})

    # For Phrasal Queries
    elif len(t) > 1 and ('not' not in query) and ('and' not in query) and ('or' not in query):
        query = removePuncQuery(query).split()
        query = [bmr.ps.stem(word) for word in query]
        result = PhrasalQuery(query, result)
        print("phrasel query")
        return json.dumps(result)

    # For Boolean Queries
    else:
        query = query.replace("-", " and ").replace("—", " and ")
        test = [precedence.get(x, 0) for x in query.split()]
        if isValidBQuery(test):
            result = BooleanQuery(query, result)
            return json.dumps(result)
        else:
            return json.dumps({"result": [], "error": "Invalid Query"})

    return json.dumps({"result": [], "error": "OLNY SUPPORTS BOOLEAN AND PROXIMITY QUERIES"})


def removePuncQuery(query):
    return query.replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace(
        "’", "").replace("—", "").replace("“", "").replace("”", "").replace("‘", "").replace(
        "'", "").replace(",", "").replace("!", "").replace(".", "").replace(":", "").replace(
        ";", "").replace("?", "").replace("-", "").replace("*", "")