from bokeh.plotting import figure, show
from itertools import chain
from more_itertools import distribute, collapse

from utils.maps import *

data = LoadCircoData()

# print(data)

p = figure(aspect_scale=1,
		   x_range=(-7, 12),
		   y_range=(40, 52))

print(len(data))
for circo in data:
	print("{} - {} - Circo {}-{} ".format(circo["properties"]["nom_reg"], circo["properties"]["nom_dpt"], circo["properties"]["code_dpt"], circo["properties"]["num_circ"]))
	# unnested = list(chain(*circo["geometry"]["coordinates"]))
	# print(unnested)
	for coordinates in circo["geometry"]["coordinates"]:
		try:
			lon, lat = zip(*coordinates)
		except ValueError:
			lon, lat = zip(*list(chain(*coordinates)))
		lon = list(lon)
		lat = list(lat)
		p.line(lon, lat, line_width=1, line_color="silver")
		# if circo["properties"]["ID"] == "ZA002":
		# 	print(list(chain(*circo["geometry"]["coordinates"])))
		# 	print(len(list(chain(*circo["geometry"]["coordinates"]))))
	# break

show(p)