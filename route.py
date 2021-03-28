import bmr
import json

def hello_world():
    return json.dumps(bmr.i_index)


def name(name):
    return "Hello, "+name


def findWord(word):
    try:
        return set(bmr.i_index[word])
    except:
        print('"%s" is not a key in the dictionary' % word)
        return set()

# TODO remove stopwords from query
def SimpleQuery(query):
    query = bmr.removePunctuation(query.lower()).split()
    query = [bmr.ps.stem(word) for word in query]
    print(query)
    result = set()
    # for queries containing only OR operator also run for one word queries
    if ('and' not in query) and ('not' not in query):
        print("or query run")
        query = [x for x in query if x != 'or']
        for word in query:
            s1 = findWord(word)
            if s1:
                result = result.union(s1)

    elif ('or' not in query) and ('not' not in query):   # for queries containing only AND operator
        print("and query run")
        query = [x for x in query if x != 'and']
        for i, word in enumerate(query):
            if i == 0:
                result = findWord(word)
                continue
            s1 = findWord(word)
            result = result.intersection(s1)

    elif ('or' not in query) and ('and' not in query) and ('not' == query[0]):
        print("not query run")
        s1 = findWord(query[1])
        if s1:
            result = set(bmr.docid) - s1
        else:
            result = bmr.docid

    if result:
        return json.dumps(sorted(list(result), key=int), indent=4)
    else:
        return ("No document found!")