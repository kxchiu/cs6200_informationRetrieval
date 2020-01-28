import os
import re
import json
import math
import operator
from os import listdir
from os.path import isfile, join
from UseIndex import find_docID_by_term, find_termID_by_term, find_iList_by_termID, find_docName_by_docID

def retrieveResult(query_file, num_result, content_folder_name, index_folder_name, *, output_file='Output.txt'):
    # Read from query text file and process by line of query.
    with open(query_file) as f:
        for line in f:
            # A new doc set for each query.
            doc_set = set()
            # Tokenize the query into list of strings.
            terms = line.split()

            # Get a set of docs using find_docID_by_term with all the terms.
            for term in terms:
                doc_list = find_docID_by_term(term, index_folder_name)
                for doc in doc_list:
                    doc_set.add(doc)

            # Get weighted TF-IDFs for query and docs.
            nqs = []
            q_all_tfidfs = []
            doc_all_tfs = {}
            for term in terms:
                termID = find_termID_by_term(term, index_folder_name)
                iList = find_iList_by_termID(termID, index_folder_name)

                # Get weighted TF-IDFs for query.
                q_tf = 1 + math.log(terms.count(term))
                q_idf = math.log(1000 / len(iList[1]))
                q_all_tfidfs.append(q_tf * q_idf)

                # Get weighted TF-IDFs for docs.
                for doc in doc_set:
                    doc_tf = 0
                    for value in iList:
                        if value[0] == doc:
                            doc_tf = value[1]
                            break
                    if doc not in doc_all_tfs:
                        temp = []
                        if doc_tf == 0:
                            temp.append(doc_tf)
                            doc_all_tfs[doc] = temp
                        else:
                            temp.append(1 + math.log(doc_tf))
                            doc_all_tfs[doc] = temp
                    else:
                        if doc_tf == 0:
                            doc_all_tfs[doc].append(doc_tf)
                        else:
                            doc_all_tfs[doc].append(1 + math.log(doc_tf))

            # Get NQ.
            q_sumsq = 0
            for q_tfs in q_all_tfidfs:
                q_sumsq += math.pow(q_tfs,2)
            q_sumsq_sqrt = math.sqrt(q_sumsq)
            for q_tfs in q_all_tfidfs:
                nqs.append(q_tfs / q_sumsq_sqrt)

            # Get ND.
            nds = {}
            for doc_tfs in doc_all_tfs:
                sumsq = 0
                for tfidf in doc_all_tfs[doc_tfs]:
                    sumsq += math.pow(tfidf,2)
                sumsq_sqrt = math.sqrt(sumsq)
                for tfidf in doc_all_tfs[doc_tfs]:
                    tfidf_nd = tfidf / sumsq_sqrt
                    if doc_tfs not in nds:
                        temp = []
                        temp.append(tfidf_nd)
                        nds[doc_tfs] = temp
                    else:
                        nds[doc_tfs].append(tfidf_nd)

            # Compute scores from NQ and ND.
            scores = {nk: [d * nq for d, nq in zip(nd, nqs)] for nk, nd in nds.items()}
            sum_scores = {nk: sum(score) for nk, score in scores.items()}
            sorted_sum_scores = sorted(sum_scores.items(), key=operator.itemgetter(1))
            sorted_sum_scores.sort(key = lambda x : (-x[1], x[0]))

            # Write to output file.
            with open(output_file, 'a', encoding='utf-8') as fp:
                fp.write('Raw query:\t{}\n'.format(line.strip()))
                fp.write('Transformed query:\t{}\n'.format(terms))
                count = 0
                while count < num_result:
                    doc_ID = sorted_sum_scores[count][0]
                    doc_name = find_docName_by_docID(doc_ID, index_folder_name)
                    fp.write('Document: {}\t{}\n'.format(doc_ID, doc_name))

                    # Open doc file for reading and find body text.
                    HtmlFile = open(content_folder_name + '\\' + doc_name,'r', encoding='utf-8')
                    source_code = HtmlFile.read()
                    body = re.findall(r'<body[^>]+(.*)</body>', source_code, re.S)
                    script_tag = re.compile(r'<script.*</script>')
                    body_clean = script_tag.sub('', str(body))
                    res = re.sub(r'<.*?>', ' ', body_clean)
                    res = re.sub(r'(\\n)|(\\t)', '', res)
                    res = re.sub(r'[^\w\d]+', ' ', res)
                    doc_content = res[1:200]

                    fp.write('Document content:\t{}\n'.format(doc_content))
                    fp.write('Document score:\t{:.3f}\n'.format(sorted_sum_scores[count][1]))
                    fp.write('Term score:\t')
                    for x in range(len(terms)):
                        fp.write('{}: {:.3f}; '.format(terms[x], scores[doc_ID][x]))
                    fp.write('\n\n')
                    count += 1
                fp.write('\n\n')
    print('##### Your search has been completed. Go look at the output.txt file. #####')


# content_folder_name = 'ContentFolderName'
# index_folder_name = 'IndexFolderName'
query_file = 'Queries.txt'
num_result = 5

# Ask for user input.
print('##### Welcome to the ranked retrieval program! #####')
print()
# print('Enter your query text file name:')
# query_file = input()
print('Your input query file: ' + query_file)
# print('How many results do you want to retrieve?')
# num_result = int(input())
print('Retrieving ' + str(num_result) + ' of results for you in Outputs.txt.')
print()
print('Input where your index files are saved:')
index_folder_name = input()
print('Input where you want to retrieve the documents:')
content_folder_name = input()
print('Your search is retrieved based on documents from the folder: ' + content_folder_name)
print()

retrieveResult(query_file, num_result, content_folder_name, index_folder_name)