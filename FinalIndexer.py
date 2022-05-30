import os
from math import log

import nltk
nltk.download('punkt')
nltk.download('stopwords')

STOPWORDS = nltk.corpus.stopwords.words('english')
STOPWORDS.append({"we've", 'cannot', "they're", "they've", "let's", "where's", "when's", 'could', "he's", "here's", "who's", "we'd", "he'll", "why's", 'ought',
                 "she'd", "i'll", 'would', "i'm", "i've", "that's", "we'll", "can't", "they'll", "they'd", "he'd", "we're", "what's", "how's", "there's", "i'd", "she'll"})

class FinalIndexer:
  def __init__(self, merged_disk_path, num_documents, numfiles):
    self.merged_disk_path = merged_disk_path
    self.N = num_documents
    self.numfiles = numfiles

  # find the token positions after merging all the partial indexers into one file
  def create_token_positions_dict(self, final_disk_path: str) -> None:
    token_positions = {}
    with open(final_disk_path, "r") as f:
      position = 0
      for line in f:
        token = line.split(":")[0][1:]
        token_positions[token] = position + 1
        position += len(line)
    return token_positions
  
  def create_new_file_with_new_scores(self) -> 'path':
    merged_disk = open(self.merged_disk_path, 'r')
    final_disk = open('finalDisk.txt', 'w')

    # read from merged_disk line by line (each line is a token)
    try: 
      while True:
        token_line = next(merged_disk)                  # "aachen:|210,1|438,1|"
        
        token = token_line.split(':')[0]                # "aachen
        postings_list = token_line.split('|')[1:-1]     # ["210,2.32", "438,1"]
        
        # df is the number of documents that this term appears in
        df = len(postings_list)

        new_token_line = token + ':|'                    # "aachen:|

        # for each posting
        sorted_postings_list = []

        for posting in postings_list:
          
          # tf is the term frequency in the document
          docid, tf = posting.split(',')                          # "210,1" => docid = 210, tf = 1
          
          # idf is the inverted document frequency
          idf = log(self.N/df, 10)
          
          # tf-idf (final computed relevance score)
          tfidf = float(tf) * idf

          sorted_postings_list.append((docid, tfidf))

        # sort postings list by descending relevance score (instead of docid)
        sorted_postings_list.sort(key=lambda x: -x[1])

        if token[1:] in STOPWORDS and len(sorted_postings_list) > 20:
          sorted_postings_list[:21]
        
        for posting in sorted_postings_list:
          docid, tfidf = posting
          new_token_line += str(docid) + ',' + str("{0:.5f}".format(tfidf)) + '|'   # "aachen:|210,4|438,4|    (still needs quote)
        
        # add a quote to the end of new_token_line
        new_token_line += '"'                                     # "aachen:|210,4|438,4|"

        # after building the new_token_line, write to finalDisk.txt
        final_disk.write(new_token_line)
        final_disk.write('\n')

    except StopIteration:
      # print('end of line')
      pass      

    merged_disk.close()
    final_disk.close()

    # delete unneeded files
    self.delete_unneeded_files()

    # TODO: change this so its not hardcoded
    return 'finalDisk.txt'


  def delete_unneeded_files(self):
    for i in range(self.numfiles):
      os.remove('disk' + str(i + 1) + '.txt')
    
    for i in range(self.numfiles - 1):
      os.remove('mergedDisk' + str(i + 1) + '.txt')