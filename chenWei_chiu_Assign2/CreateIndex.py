import os
import re
import json
from RunDataTransformer import DataTransformer

class IndexCreater:
    def __init__(self):
        self.total_file_size = 0
        self.total_tokens = 0
        self.unique_tokens = 0
        self.total_index_size = 0

    def add_stats(self, file_size, tokens, unique, index_size):
        self.total_file_size += file_size
        self.total_tokens += tokens
        self.unique_tokens += unique
        self.total_index_size += index_size

    def save_stats(self, filename):
        with open(filename, 'w', encoding='utf-8') as fp:
            fp.write('Total file size: {} bytes\n'.format(self.total_file_size))
            fp.write('Total tokens: {}\n'.format(self.total_tokens))
            fp.write('Unique tokens: {}\n'.format(self.unique_tokens))
            fp.write('Total index size: {} bytes\n'.format(self.total_index_size))
            fp.write('Average index size: {:.3f} bytes'.format(self.average_size))

    @property
    def average_size(self):
        return self.total_index_size / self.total_file_size

    def save(self, filename, file_to_save):
        with open(filename, 'w', encoding='utf-8') as fp:
           json.dump(file_to_save, fp)
    

def createIndex(doc_list, *, term_id_fp='TermIDFile.txt', doc_id_fp='DocumentIDFile.txt', 
        inverted_index_fp='InvertedIndex.txt', term_id_map_fp='TermIDMap.txt', stats_file='stats.txt', outputs_dir='outputs'):
    index_creater = IndexCreater()

    total_file_size = 0
    total_tokens = 0
    unique_tokens = 0
    total_index_size = 0

    # Create dictionaries.
    term_ID_map = {'':''}
    term_ID_file = {'':[]}
    doc_id_file = {'':[]}
    inverted_index = {'':[]}
    counted = set()

    # Iterate thru the lists of tokens.
    for curr_list in doc_list:
        

        # Get document ID and remove it from the list of tokens.
        documentID = curr_list[0]
        doc_id_file[documentID] = [documentID + '.txt', len(curr_list)]
        curr_list.remove(curr_list[0])
        temp_list = {}

        # Add token to counted set, term-ID map, term ID file, and a temp list.
        for word in curr_list:
            if word not in counted:
                term_ID = len(counted)
                term_ID_map[word] = term_ID
                #print('Word: {} setAs {}'.format(word, len(counted)))
                term_ID_file[len(counted)] = 1
            else:
                term_ID = term_ID_map[word]
                term_ID_file[term_ID] += 1
            if term_ID not in temp_list:
                temp_list[term_ID] = 0
            temp_list[term_ID] += 1
            counted.add(word)
            total_file_size += len(word)
            total_tokens += 1
        
        # Add term counts from temp list to inverted index.
        for term_ID in temp_list:
            if term_ID not in inverted_index:
                inverted_index[term_ID] = [[documentID, temp_list[term_ID]]]
            else:
                inverted_index[term_ID].append([documentID, temp_list[term_ID]])
    unique_tokens = len(counted)
    term_ID_map.pop('', None)
    term_ID_file.pop('', None)
    doc_id_file.pop('', None)
    inverted_index.pop('', None)

    # Save files.
    index_creater.save(term_id_fp, term_ID_file)
    index_creater.save(doc_id_fp, doc_id_file)
    index_creater.save(inverted_index_fp, inverted_index)
    index_creater.save(term_id_map_fp, term_ID_map)

    term_id_fp_size = os.path.getsize(term_id_fp)
    doc_id_fp_size = os.path.getsize(doc_id_fp)
    ilist_fp_size = os.path.getsize(inverted_index_fp)
    total_index_size = term_id_fp_size + doc_id_fp_size + ilist_fp_size
    index_creater.add_stats(total_file_size, total_tokens, unique_tokens, total_index_size)
    index_creater.save_stats(stats_file)  

# Ask for user input.
print('Enter your folder name:')
FolderName = input()
print('Enter your number of files to process:')
NumFilesToProcess = int(input())

# Get token lists from DataTransformer and create index.
doc_list = []
dataTransformer = DataTransformer()
doc_list = dataTransformer.dataTransform(FolderName, NumFilesToProcess)
createIndex(doc_list)