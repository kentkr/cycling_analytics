# gpxpy would not import in this environment. Instead it's loaded from the following py 3.7 installation location
import sys
sys.path.insert(1,'/Applications/anaconda_custom/anaconda3/lib/python3.7/site-packages/gpxpy')
import gpxpy
import matplotlib.pyplot as plt
import pandas as pd

# import pandas as pd # if this fails, above change sys.path.insert to sys.path.append https://stackoverflow.com/questions/4383571/importing-files-from-different-folder
# import numpy as np

file1 = open('/Users/kylekent/Desktop/research/CS_misc/GitHub/strava_project/strava_export_10-13-20/activities/794638496.gpx', 'r')
data = gpxpy.parse(file1)

# info on this file
print('Name: ' + str(data.tracks[0].name))
print('Description: ' + str(data.tracks[0].description))
# start and end time
print('Start: ' + str(data.tracks[0].get_time_bounds().start_time))
print('End: ' + str(data.tracks[0].get_time_bounds().end_time))
# bounds of the gpx data
bounds = data.tracks[0].get_bounds()
print('Latitude bounds: (%f,%f)' % (bounds.min_latitude, bounds.max_latitude))
print('Longitude bounds: (%f,%f)' % (bounds.min_longitude, bounds.max_longitude))

# duration in seconds converted to minutes
data.tracks[0].get_duration()/60
# distance in meters converted to kilometers
data.tracks[0].length_2d()/1000

# quickly visualizing the track
track_coords = [[point.latitude, point.longitude, point.elevation]
                for track in data.tracks
                    for segment in track.segments
                        for point in segment.points]
coords_df = pd.DataFrame(track_coords, columns = ['latitude', 'longitude', 'altitude'])
fig = plt.figure(figsize = (12,9))
coords_df.plot('longitude', 'latitude', color = 'red', linewidth = 1.5)

# -------------------------------------------------------------------------------------------------------
# now mapping and loading all gpx data