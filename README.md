This project discover bus stops locations from activities points collected (activity_points.geojson) using the clustering method DBSCAN, cluster the information 
and analyze the density from each cluster to give recommended bus stops. DBSCAN uses haversine
metric and min samples = 1 to find spare activities. 

** Please see bus_stops.ipynb or .html for documentation and results **


The following files are:

1. bus_stops.html - is a presentation in HTML of the code, please open it in your browser to visualize code results.
2. bus_stops.ipynb - notebook with the code in python.
3. manage.py and others - files to run server and project.


Execution

Run ‘python manage.py runserver’ inside bus_stops folder.
Open http://127.0.0.1:8000/
Visualize the results.