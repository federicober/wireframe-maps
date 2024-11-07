from pyrosm import get_data
from pyrosm import OSM
import geopandas
import matplotlib.pyplot as plt

# # Download data for the city of Helsinki
fp = get_data("test_pbf")

# Initialize the OSM parser object
osm = OSM(fp)
# osm = OSM("Paris.osm.pbf")
print(osm)

# Read all drivable roads
# =======================
drive_net: geopandas.GeoDataFrame = osm.get_network(network_type="driving")
print(drive_net)
ret = drive_net.plot()
print(ret)
plt.show()
