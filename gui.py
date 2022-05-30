from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for

from Indexer import Indexer
from MergeIndexer import MergeIndexer
from FinalIndexer import FinalIndexer
from BooleanSearch import BooleanSearch
import time 
import os

TOKEN_POSITIONS = {}
app = Flask(__name__)

# build partial indexers
index = Indexer()
index.build_index('/Users/asl/UCI/2021-22/22S/CS121/a3/ANALYST')

@app.route('/')
def get_input():
    return render_template('search.html')


@app.route('/', methods=['POST'])
def get_user_query():
    if request.method == 'POST':
        query = request.form.items()
        token = ''
        for key,val in query:
            token = val
        return show_results(token)
    return render_template('search.html')


def show_results(query):
    results = boolean_search('finalDisk.txt', query)
    # boolean retrieval and search
    return render_template('results.html', query=query, results=results)

# gets user query and uses boolean search to find queries in the indexer. if urls are found, print the top 5
def boolean_search(final_disk_name, query):
    global TOKEN_POSITIONS
    
    # search the query via boolean search
    try:

      start = time.time()

      search = BooleanSearch(query, TOKEN_POSITIONS, final_disk_name)
      search.parse_query()
      matching_docids = search.search_query()

      end = time.time()

      if len(matching_docids) == 0:
        print('No results found')
        print("TOTAL TIME (MS) FOR THIS QUERY: ", (end - start) * 1000)
        return []
      else: 
        
        # get top 10 urls from query
        if len(matching_docids) > 10:
          matching_docids = matching_docids[:10]

        # printing urls associated with each docid
        for docid in matching_docids:
          print(index.urlhash[docid])

        print("TOTAL TIME (MS) FOR THIS QUERY: ", (end - start) * 1000)
        return [index.urlhash[doc_id] for doc_id in matching_docids]

    except Exception as e:
      print(e)


if __name__ == '__main__':
    # merge partial indexers
    merged_index = MergeIndexer(index.get_numfiles())
    merged_disk_path = merged_index.merge_all_indexers()

    # create final indexer by calculating the new f scores for each token in the merged disk
    num_documents = index.get_n()
    final_index = FinalIndexer(merged_disk_path, num_documents, index.get_numfiles())
    final_disk_name = final_index.create_new_file_with_new_scores()
    # get a dict of tokens with its positions
    TOKEN_POSITIONS = final_index.create_token_positions_dict(final_disk_name)

    app.run(host='0.0.0.0')