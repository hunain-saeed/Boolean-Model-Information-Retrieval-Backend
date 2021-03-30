import json
import os
import nltk
from nltk.stem import PorterStemmer


swl = []
dic = {}
docid = []
i_index = {}
p_index = {}

ps = PorterStemmer()

# Read stop word from file and split them
# and store each word in swl list
def readStopWord():
    try:
        global swl
        swl = open('Stopword-List.txt', 'r').read().split()
    except Exception as e:
        print(e)


# Find the all file name in the directory, extract docid and store it on docid variable
def AllFileInDir():
    global docid
    # list of file name in the ShortStories dir
    file_names = os.listdir("ShortStories/")
    # split the name of file to get docid
    docid = [int(fn.split('.')[0]) for fn in file_names]

    try:
        docid.sort()     # sort the docids
    except Exception as e:
        print(e)


# Remove punctuation from stories
def removePunctuation(words):
    words = words.replace("n’t", " not").replace("’ll", " will").replace("’m", " am").replace(
        "’ve", " have").replace("’re", " are").replace("’d", " had").replace("it’s", "it is").replace(
        "he’s", "he is").replace("she’s", "she is").replace("that’s", "that is").replace("who’s", "who is").replace(
        "to-morrow", "tomorrow").replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace(
        "’", "").replace("—", " ").replace("“", "").replace("”", "").replace("‘", "").replace(
        "'", "").replace(",", "").replace("!", "").replace(".", "").replace(":", "").replace(
        ";", "").replace("?", "").replace("-", " ").replace("*", "")

    # .replace("¯", "").replace(
    # "ã", "a").replace("ª", "a").replace("©", "c").replace("§", "s").replace("¨", "")
    return words


# Reads all stories from files one by one and stemm the tokens
def readFilesAndStemm():
    for x in docid:
        f = open("ShortStories/"+str(x)+".txt", 'r',
                encoding='utf8').read()     # read file one by one
        # casefolding and removing punctuations and tokenize (words list)
        f = removePunctuation(f.lower()).split()
        # Stemming words and storing list of words in a dictionary agains their doc id

        dic[x] = [ps.stem(word) if word not in swl else word for word in f]

        # making inverted index and positional index
        creatInvertedandPositionalIndex()
        # print(dic)


# take word and docid and add them in Inverted Index
def InvertedIndex(word, docid):
    if word not in i_index:  # if word is not in the inverted index then add it
        i_index[word] = []
        i_index[word].append(docid)
    else:   # if doc id is not in the list then append it againt the given word/key
        if docid not in i_index[word]:
            i_index[word].append(docid)


# take word, docid and their position in document and add them in Inverted Index
def positionIndex(word, docid, position):
    if word not in p_index:  # if word is not in the positional index then add it also add its doc id
        p_index[word] = {}
        p_index[word][docid] = []
    else:  # if doc id is not in the list then append it againt the given word/key
        if docid not in p_index[word]:
            p_index[word][docid] = []
    if position not in p_index[word][docid]:
        p_index[word][docid].append(position)


# Inverted index and Positional index creation
def creatInvertedandPositionalIndex():
    for docid in dic.keys():
        for position, word in enumerate(dic[docid]):
            if word in swl:
                continue
            InvertedIndex(word, docid)
            positionIndex(word, docid, position)


# Write Both indexes to seperatre files
def WriteIndexesToFile():
    json_ii = json.dumps(i_index)
    json_pi = json.dumps(p_index)

    iiFile = open('InvertedIndex.json', 'w', encoding='utf8')
    piFile = open('PositionalIndex.json', 'w', encoding='utf8')

    iiFile.write(json_ii)
    piFile.write(json_pi)

    iiFile.close()
    piFile.close()


# Reading indexes from their respective file and saving them in global dictionaries
def ReadIndexesFromFile():
    global i_index
    global p_index

    try:
        iiFile = open('InvertedIndex.json', 'r', encoding='utf8')
        piFile = open('PositionalIndex.json', 'r', encoding='utf8')

        i_index = json.loads(iiFile.read())
        p_index = json.loads(piFile.read())
        
        iiFile.close()
        piFile.close()

        if (not i_index) or (not p_index):
            readFilesAndStemm()
            WriteIndexesToFile()

    except Exception as e:
        print(e)
        readFilesAndStemm()
        WriteIndexesToFile()



def main():
    readStopWord()
    AllFileInDir()
    ReadIndexesFromFile()