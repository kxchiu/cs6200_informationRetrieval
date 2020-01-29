# cs5100_foundationsOfAI
This is a repository for my individual projects from the course CS 6200 Information Retrieval at Northeastern University--Seattle. Throughout the course, I implemented a web search engine through applying information retrieval theories using Python and from ground up without BeautifulSoup.

## Assignment 1
In Assignment 1, I implemented a web crawler that crawls from Karen Sparck Jones' Wikipedia page and only under the Wikipedia domain. The crawlers takes in two input: the seed URL and the number of URLs to crawl. It saves the HTML of the crawled pages into txt files and updates the overall crawling statistics in stats.txt. It also crawls with the polite rule of sleeping for 1s before the next crawl.

## Assignment 2
In Assignment 2, I implemented the indexer that indexes terms from the body of the crawled HTML files. It creates an inverted index list from the indexed terms and generates several index files (Term to Term ID, Document to Document ID, Term ID to Document ID, inverted index).

## Assignment 3
In Assignment 3, I implemented a simple search engine that takes in the user input queries from a txt file and returns the top 10 documents with the highest document relevence scores for each query. It indexes the terms in the user queries, compute the tf-idf for the query and documents using the index files from Assignment 2, sort the documents from highest to lowest scores, and returns the top 10 documents.
