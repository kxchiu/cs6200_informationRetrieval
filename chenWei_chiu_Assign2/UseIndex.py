import json

def find_termID_by_term(term):
    file = open('TermIDMap.txt', 'rb')
    data = eval(file.read())
    file.close()
    return data[term]

def find_iList_by_termID(termID):
    file = open('InvertedIndex.txt', 'rb')
    data = json.load(file)
    file.close()
    return data[str(termID)]

def find_docID_by_term(term):
    termID = find_termID_by_term(term)
    iList = find_iList_by_termID(termID)
    docIDs =[]
    for doc in iList:
        docIDs.append(doc[0])
    return docIDs

# The crawled document names should correspond to the document ID, as given in requirements from assignment 1!
def find_docName_by_docID(docID):
    file = open('DocumentIDFile.txt', 'rb')
    data = eval(file.read())
    file.close()
    docData = data[docID]
    docName = docData[0]
    return docName


print('Enter the term to look up all the document names with the term:')
term = input()
print()
docIDs = find_docID_by_term(term)
docString = []
print('The term appears in the following document(s):')
for docID in docIDs:
    docName = find_docName_by_docID(docID)
    docString.append(docName)
print(docString)
