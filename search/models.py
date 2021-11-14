from django.conf import settings

from django.db import models
import requests
from django.shortcuts import render , redirect
class Videos(models.Model):
    video_id = models.CharField(
        null=False,
        blank=False,
        max_length=200
    )

    title = models.CharField(
        null=True,
        blank=True,
        max_length=500
    )

    publishedDateTime = models.DateTimeField()

    thumbnailsUrls = models.URLField()


search_url = 'https://www.googleapis.com/youtube/v3/search'
video_url = 'https://www.googleapis.com/youtube/v3/videos'

search_params = {
            'part' : 'snippet',
            # 'q' : request.POST['search'],
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'order' : 'date',
            'maxResults' : 9,
            'type' : 'video'
        }

        
r = requests.get(search_url, params = search_params)

        
results = r.json()['items']
video_ids = []
for result in results:
    video_ids.append(result['id']['videoId'])

video_params = {
    'part' : 'snippet,contentDetails',
    'key' : settings.YOUTUBE_DATA_API_KEY,
    'id' : ','.join(video_ids)
}

r = requests.get(video_url,params = video_params)
results = r.json()['items']
print(results)
def save(self, *args,**kwargs):
    for result in results:
        self.title =   result['snippet']['title']
        self.video_id = result['id']
        self.publishedDateTime = result['snippet']['publishedAt']
        self.thumbnailsUrls = result['snippet']['thumbnails']['high']['url']
    super().save(*args, **kwargs)
    
def __str__(self):
    return self.title