# import python packages
import json
import warnings
import pandas as pd, numpy as np, matplotlib.pyplot as plt, time
from sklearn.cluster import DBSCAN
from sklearn import metrics
from geopy.distance import great_circle
from shapely.geometry import MultiPoint
import folium

def get_centermost_point(cluster):
    centroid = (MultiPoint(cluster).centroid.x, MultiPoint(cluster).centroid.y)
    centermost_point = min(cluster, key=lambda point: great_circle(point, centroid).m)
    return tuple(centermost_point)

# Get coordinates from Geojson objects
def get_coordinates(geojson,type):

    with open(geojson) as f:
        data = json.load(f)

    data = data['features']
    if type == "p":
        data= [ dict({"lat": object['geometry']['coordinates'][1], "lon": object['geometry']['coordinates'][0]}.items()
              + object['properties'].items()) for object in data ]
    else:
        data = [dict({"coordinates": object['geometry']['coordinates']}.items()
               + object['properties'].items()) for object in data]
    return pd.DataFrame(data)


def start_find_points():

    warnings.filterwarnings('ignore')

    # Obtain coordinates from activity points and routes
    dataroutes = get_coordinates('stops/routes.geojson',"r")
    datapoints = get_coordinates('stops/activity_points.geojson',"p")
    coords = datapoints.as_matrix(columns=['lat', 'lon'])
    coords_routes = dataroutes['coordinates'].tolist()


    # define the number of kilometers in one radian
    kms_per_radian = 6371.0088
    km = 0.8
    # define epsilon as 1.5 kilometers, converted to radians for use by haversine
    epsilon = km / kms_per_radian
    print(str(km*1000) + " meters used for haversine metric")

    # Execute method DBSCAN, use just 1 min_samples  
    # because of isolate user activity points
    db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
    cluster_labels = db.labels_

    # get the number of clusters
    num_clusters = len(set(cluster_labels))

    # Print the outcome
    print('Estimated number of clusters: %d' % num_clusters)
    print('Silhouette coefficient: {:0.03f}'.format(metrics.silhouette_score(coords, cluster_labels)))

    # turn the clusters in to a pandas series, where each element is a cluster of points
    clusters = pd.Series([coords[cluster_labels == n] for n in range(num_clusters)])

    centermost_points = clusters.map(get_centermost_point)

    # unzip the list of centermost points (lat, lon) tuples into separate lat and lon lists
    lats, lons = zip(*centermost_points)

    # from these lats/lons create a new df of one representative point for each cluster
    rep_points = pd.DataFrame({'lon': lons, 'lat': lats})

    core_samples_mask = np.zeros_like(cluster_labels, dtype=bool)
    unique_labels = set(cluster_labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = 'k'

        class_member_mask = (cluster_labels == k)

        xy = coords[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                 markeredgecolor='k', markersize=14)

        xy = coords[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                 markeredgecolor='k', markersize=6)

    plt.title('Estimated number of clusters: %d' % num_clusters)
    # Show clusters
    # plt.show()

    # Create a web map from the first bus stop
    map = folium.Map(location=[lats[0], lons[0]], zoom_start=13,
                       tiles='Stamen Terrain')
    
    # Take all central points and marked them in the web map
    index = 1
    for lat, lon in zip(lats, lons):
        folium.Marker([lat, lon], popup=("Bus Stop for group: "+ str(index))).add_to(map)
        index+=1

    # Draw routes inside web map
    for route in coords_routes:
        route = [tuple([coordinates[1],coordinates[0]]) for coordinates in route]
        folium.PolyLine(route, color="orange", weight=2.5, opacity=1).add_to(map)

    # Save map as HTML for display as first page
    map.save('stops/templates/index.html')






