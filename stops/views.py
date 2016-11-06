from django.shortcuts import render
import requests, json
import find_centroids
from pathlib import Path

# method to capture GET and POST for search in Github repositories
def map_show(request):

    index = Path("stops/templates/index.html")
    if not index.is_file():
        find_centroids.start_find_points()

    if request.method == 'GET':
        return render(request, 'index.html')
