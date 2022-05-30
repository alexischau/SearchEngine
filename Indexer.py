from math import log
from Posting import Posting
import os
import json
from pathlib import Path
import json
import lxml
import lxml.html
from nltk.stem import PorterStemmer
import nltk
nltk.download('punkt')
from bs4 import BeautifulSoup
from collections import defaultdict
import unidecode

class Indexer:
    def __init__(self):
      # indexer is a dictionary where the key is the token
      # and the value is a list of postings
      self.indexer = {}
      self.urlhash = {}
      # n is the docid
      self.n = 0
      self.filenum = 1
      self.filesvisited = 0
      self.porter = PorterStemmer()
      self.lines_to_read = 100
      self.batch_threshold = 700 # TODO: 5000 (DEV), 700 (ANLAYST)
          
    # builds the in-memory indexer
    def build_index(self, dirpath: str) -> None:
      # get a list of all the jsons files within the directory
      documents_list = self.get_nested_files(Path(dirpath))
      
      # for each documnet
      for document in documents_list:
        document_as_str = str(document)

        if document_as_str.endswith(".json"):
          self.n += 1

          # increment number of files visited
          self.filesvisited += 1

          # if number of files visited reaches the batch threshold
          if self.filesvisited >= self.batch_threshold:
            
            print("BATCH CREATED AT ", self.filenum)

            # build a partial index from this batch and write to disk
            self.sort_and_write_to_disk()
            
            # empty the indexer and reset
            self.indexer = {}
            
            # reset number of files visited 
            self.filesvisited = 0
            
            # increment number of disks created
            self.filenum += 1
            
          f = open(document_as_str)

          # read the content from the json file
          document_json = json.loads(f.read())

          # get token frequency from the content
          token_freq = self.parse(document_json["content"])

          # add the tokens to indexer
          self.add_to_index(token_freq)
          
          # add n and its corresponding url to urlhash dictionary
          self.urlhash[self.n] = document_json["url"]

          f.close()
      
      print("BATCH CREATED AT ", self.filenum)
      self.sort_and_write_to_disk()


    # sort indexer by token (saves time when merging), serialize each item in indexer, write to disk
    def sort_and_write_to_disk(self):
      with open("disk" + str(self.filenum) + ".txt", "w") as f:
        # TODO: sort the indexer by token
        for token, postings in sorted(self.indexer.items()):
          serialized_index = '"' + token + ":"
          for posting in postings:
            serialized_index += "|" + str(posting.docid) + "," + str(posting.tfidf)
          serialized_index += '|"'       
          f.write(serialized_index)
          f.write('\n')

    # get size of disk in kilobytes
    def get_size_of_disk(self, disk_num):
      size_in_bytes = os.path.getsize("disk" + str(disk_num) + ".txt")
      return size_in_bytes / 1024

    # for each token in the document, if token is not in the Indexer then
    # add the token to the indexer and its posting to a new list. 
    # otherwise, append the token and its posting to the pre-existing list
    def add_to_index(self, token_freq) -> None:
      for token in token_freq:
       
        # calculate tf for token
        tf = 1 + log(token_freq[token], 10)
       
        # make a new Posting instance
        if token not in self.indexer:
          # TODO: add bonus points
          self.indexer[token] = [Posting(self.n, tf)] 
          
        else:
          self.indexer[token].append(Posting(self.n, tf))


    # takes in the content in the json object 
    # and returns a dictionary of all the tokens in the file and its frequency
    def parse(self, content) -> dict:
        soup = BeautifulSoup(content, 'lxml')
        # tokenize text here
        text = soup.get_text()
        token_list = nltk.word_tokenize(text)
        token_freq = defaultdict(int)
        
        for word in token_list:
            word = unidecode.unidecode(word)
            word_lower = word.lower()
            stem = self.porter.stem(word_lower)
            if stem.isalpha():
             token_freq[stem] += 1 

        # looking at bonus points once per tag type in doc
        for info in soup.find_all('title'):
            text = info.get_text()
            words = nltk.word_tokenize(text)
            for word in words:
              word = unidecode.unidecode(word)
              word_lower = word.lower()
              stem = self.porter.stem(word_lower)
              if stem.isalpha():
                token_freq[stem] += 11
        for info in soup.find_all('h1'):
            text = info.get_text()
            words = nltk.word_tokenize(text)
            for word in words:
              word = unidecode.unidecode(word)
              word_lower = word.lower()
              stem = self.porter.stem(word_lower)
              if stem.isalpha():
                token_freq[stem] += 4
        for info in soup.find_all('h2'):
            text = info.get_text()
            words = nltk.word_tokenize(text)
            for word in words:
              word = unidecode.unidecode(word)
              word_lower = word.lower()
              stem = self.porter.stem(word_lower)
              if stem.isalpha():
                token_freq[stem] += 3
        for info in soup.find_all('h3'):
            text = info.get_text()
            words = nltk.word_tokenize(text)
            for word in words:
              word = unidecode.unidecode(word)
              word_lower = word.lower()
              stem = self.porter.stem(word_lower)
              if stem.isalpha():
                token_freq[stem] += 2
        for info in soup.find_all('h4'):
            text = info.get_text()
            words = nltk.word_tokenize(text)
            for word in words:
              word = unidecode.unidecode(word)
              word_lower = word.lower()
              stem = self.porter.stem(word_lower)
              if stem.isalpha():
                token_freq[stem] += 0.5
        for info in soup.find_all('h5'):
            text = info.get_text()
            words = nltk.word_tokenize(text)
            for word in words:
              word = unidecode.unidecode(word)
              word_lower = word.lower()
              stem = self.porter.stem(word_lower)
              if stem.isalpha():
                token_freq[stem] += 0.5
        for info in soup.find_all('h6'):
            text = info.get_text()
            words = nltk.word_tokenize(text)
            for word in words:
              word = unidecode.unidecode(word)
              word_lower = word.lower()
              stem = self.porter.stem(word_lower)
              if stem.isalpha():
                token_freq[stem] += 0.5
        for info in soup.find_all('strong'):
            text = info.get_text()
            words = nltk.word_tokenize(text)
            for word in words:
              word = unidecode.unidecode(word)
              word_lower = word.lower()
              stem = self.porter.stem(word_lower)
              if stem.isalpha():
                token_freq[stem] += 1
        for info in soup.find_all('bold'):
            text = info.get_text()
            words = nltk.word_tokenize(text)
            for word in words:
              word = unidecode.unidecode(word)
              word_lower = word.lower()
              stem = self.porter.stem(word_lower)
              if stem.isalpha():
                token_freq[stem] += 0.5
        return token_freq
      

    # finds and returns a list of files inside a directory and its subdirectories
    def get_nested_files(self, path: Path) -> list:      
      all_files = []
      for item in path.iterdir():
        if os.path.isfile(item):
            all_files.append(item)
        else:
            for file_in_subdir in self.get_nested_files(item):
                all_files.append(file_in_subdir)
      return sorted(all_files)


    def get_numfiles(self) -> int:
      return self.filenum
    
    def get_n(self) -> int:
      return self.n