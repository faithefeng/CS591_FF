# This is the source code for programming assignment 1 of CS 591
# Author: Fan Feng
# Email: ffeng2@crimson.ua.edu
# Date: Jan 26th 2019
# Modification notes:


import argparse
from apiclient.discovery import build
from apiclient.errors import HttpError
#from oauth2client.tools import argparse

#### The following part are copied directly from the sample file
# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyDjuJyo90Wf06NNAanMi7OVKy4iLS-67Ws"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
def get_Video_results(search_response):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
    
  # Merge video ids
  search_videos = []
  for search_result in search_response.get('items', []):
    search_videos.append(search_result['id']['videoId'])
  video_ids = ','.join(search_videos)
 
  # Call the videos.list method to retrieve details for each video.
  video_response = youtube.videos().list(
    id=video_ids,
    part='snippet, statistics'
  ).execute()
  
  # Add each result to the list, and then display the list of matching videos.
  videos = []
  for video_result in video_response.get('items', []):
    videos.append('%s, \t %s,\t %s ,%s \n' % (video_result["id"],
                  video_result['snippet']['title'],
                  video_result['statistics']['viewCount'],
                  video_result['snippet']['publishedAt']))
  return videos


def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve videos matching the specified
  # query term.
  startDate = '2018-01-01T00:00:00.000Z'
  endDate   = '2019-01-01T00:00:00.000Z'
  search_response = youtube.search().list(
    q=options.query,
    part="id,snippet",
    maxResults=options.max_results,
    type='video',
    publishedAfter = startDate,
    publishedBefore = endDate,
    order = options.order
  ).execute()
    
  print(search_response['nextPageToken'])
  nextPageToken = search_response['nextPageToken']
  
  # run the command again
  search_response2 = youtube.search().list(
    q=options.query,
    part="id,snippet",
    maxResults=options.max_results,
    type='video',
    publishedAfter = startDate,
    publishedBefore = endDate,
    order = options.order,
    pageToken = nextPageToken
  ).execute()
  
  videos = get_Video_results(search_response)
  videos = videos + get_Video_results(search_response2)
  
  print "video:\n", "".join(videos), "\n"
  print "The number of results is %d"%len(videos)
  return videos

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-q','--query',help ="query term",default = "landslide")
  parser.add_argument('-m','--max-results', help="Max results", default=50)
  parser.add_argument('-o','--order', help="ordered by:viewCount, relevance,...",default='viewCount')
  args = parser.parse_args()

  try:
    results = youtube_search(args)
     
    with open("results.txt", "w") as f:
        f.write("2018-01-01T00:00:00.000Z" + "\t"+"2019-01-01T00:00:00.000Z"+"\n")
        for line in results:
            f.write(line.encode("utf-8"))
 
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
