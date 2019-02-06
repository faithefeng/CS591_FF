###Usage
This is a quick guide for using my script

**Command**
python Assignment1_Fan.py [-h] [-q QUERY] [-m MAX_RESULTS] [o ORDER]

optional arguments:
  -h, --help            show this help message and exit
  -q QUERY, --query QUERY
                        query term
  -m MAX_RESULTS, --max-results MAX_RESULTS
                        Max results
  -o ORDER, --order ORDER
                        ordered by: viewCount, relevance,...
  **Example**
  1. Get the 100 most viewed  videos containing the word "landslide", and the
  result will be stored in "results.txt"
  python Assignment1_Fan.py -q "landslide" -m 100 -o "viewCount"
