import urllib.request 
import json
import django
import os

from datetime import datetime
from movies.models import Movie


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


def BatchTask():
    url = "https://yts.mx/api/v2/list_movies.json"

    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    json_str = urllib.request.urlopen(req).read().decode("utf-8")
    data = json.loads(json_str)

    for movie in data["data"]["movies"]:
        
        title   = movie["title"]
        year    = movie["year"]
        rating  = movie["rating"]
        genres  = "장르"
        summary = movie["summary"]

        Movie.objects.create(
            title = title,
            year = year,
            rating = rating,
            genres = genres,
            summary = summary
        )

BatchTask()
print("====================================")
print("Success")
print(datetime.now())