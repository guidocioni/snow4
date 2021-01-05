import matplotlib
matplotlib.use('Agg')
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import datetime
import utils
from matplotlib.colors import from_levels_and_colors

datetime_now = datetime.datetime.utcnow()

time, snow = utils.get_snow_data(datetime_now)
# Snow is shape (6, 909, 671), previous 6 hours

lons, lats = utils.get_coords()

fig = plt.figure(figsize=(14, 14))

m = Basemap(projection='cyl', llcrnrlon=lons.min(), llcrnrlat=lats.min(),\
              urcrnrlon=lons.max(), urcrnrlat=lats.max(),  resolution='i')
x, y = m(lons, lats)

levels_snow = (1, 5, 10, 15, 20, 30, 40, 50, 70, 90, 150)

colors = ["#DBF069", "#5AE463", "#E3BE45", "#65F8CA", "#32B8EB",
          "#1D64DE", "#E97BE4", "#F4F476", "#E78340", "#D73782", "#702072"]
cmap_snow, norm_snow = from_levels_and_colors(
    levels_snow, colors, extend='max')

img = m.arcgisimage(service='World_Topo_Map', xpixels=800)
#img.set_alpha(0.8)
m.drawcountries(linewidth=0.6, linestyle='solid', color='black')
m.readshapefile('shapefiles/DEU_adm/DEU_adm1', 'DEU_adm1',
                linewidth=0.2, color='black', zorder=3)

cs = m.contourf(x, y, snow[-1, :, :], levels=levels_snow,
                cmap=cmap_snow, norm=norm_snow, extend='max',
                alpha=1, zorder=2)

plt.title('SNOW 4 Analysis, ' + time[-1].strftime('%d %b %Y, %H UTC'))
plt.colorbar(orientation='horizontal',
             label='Snow depth [cm]', pad=0.02, fraction=0.03)
plt.savefig(utils.folder_images+'hsnow.png', dpi=120, bbox_inches='tight')
#plt.show()
