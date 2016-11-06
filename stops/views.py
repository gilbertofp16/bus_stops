from django.shortcuts import render
import requests, json
import find_centroids

# method to capture GET and POST for search in Github repositories
def map_show(request):

    find_centroids.start_find_points()

    if request.method == 'GET':
        return render(request, 'index.html')
