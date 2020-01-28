import os
import re
import string
from os import listdir
from os.path import isfile, join


res_list = []

class DataTransformer:
    def dataTransform(self, folder_name, num_files_to_process, *, outputs_dir=''):
        # Get path and files.
        mypath = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(mypath, folder_name)
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
        currFileNum = 0

        for fileName in onlyfiles:
            document_list = []

            # Stop when number of files reached.
            if currFileNum >= num_files_to_process:
                print('Reached maximum number of files to process: {} file(s). Aborting...'.format(currFileNum))
                break

            print('Processing file: {}'.format(fileName))

            # Open file for reading.
            HtmlFile = open(path + '\\' + fileName,'r', encoding='utf-8')
            source_code = HtmlFile.read()

            # Find title and body text.
            fileNum = re.findall(r'\d+', fileName, re.S)
            title = re.findall(r'<title>(.*)</title>', source_code, re.S)
            print('Title of the page: {}'.format(title))
            document_list.append(fileNum[0])
            body = re.findall(r'<body[^>]+(.*)</body>', source_code, re.S)
            
            # Clean up body text.
            script_tag = re.compile(r'<script.*</script>')
            body_clean = script_tag.sub('', str(body))
            res = re.sub(r'<.*?>', ' ', body_clean)
            res = re.sub(r'(\\n)|(\\t)', '', res)
            res = re.sub(r'[^\w\d]+', ' ', res).split()

            # Append tokens to list and append that list into result list.
            for word in res:
                document_list.append(word)
            res_list.append(document_list)
            HtmlFile.close()
            currFileNum += 1
            
        # Return the list of lists of tokens.
        return res_list