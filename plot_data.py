import matplotlib
matplotlib.use('Agg')
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import datetime
import utils
from matplotlib.colors import from_levels_and_colors
import os
import seaborn as sns
import pandas as pd

home_folder = os.getenv('HOME_FOLDER')

datetime_now = datetime.datetime.utcnow()

time, snow = utils.get_snow_data(datetime_now)
# Snow is shape (6, 909, 671), previous 6 hours

lons, lats = utils.get_coords()

fig = plt.figure(figsize=(11, 11))

m = Basemap(projection='cyl', llcrnrlon=lons.min(), llcrnrlat=lats.min(),\
              urcrnrlon=lons.max(), urcrnrlat=lats.max(),  resolution='i')
x, y = m(lons, lats)

levels_snow = (0.5, 1, 2.5, 5, 10, 15, 20, 25, 30, 40, 50, 70, 90, 150, 200)

colors_tuple = pd.read_csv(home_folder+'/cmap_snow_wxcharts.rgba', header=None).values    
cmap_snow, norm_snow = from_levels_and_colors(levels_snow,
                       sns.color_palette(colors_tuple, n_colors=len(levels_snow)),
                 extend='max')

img = m.arcgisimage(service='Canvas/World_Dark_Gray_Base', xpixels=800)
#img.set_alpha(0.8)
m.drawcountries(linewidth=0.6, linestyle='solid', color='black')
m.readshapefile(home_folder+'/shapefiles/DEU_adm/DEU_adm1', 'DEU_adm1',
                linewidth=0.2, color='black', zorder=3)

cs = m.contourf(x, y, snow[-1, :, :], levels=levels_snow,
                cmap=cmap_snow, norm=norm_snow, extend='max',
                alpha=1, zorder=2)

plt.title('SNOW 4 Analysis, ' + time[-1].strftime('%d %b %Y, %H UTC'))
plt.colorbar(orientation='horizontal', label='Snow depth [cm]',
             pad=0.02, fraction=0.035, ticks=levels_snow, format='%.1f')
plt.savefig(utils.folder_images+'hsnow_de.png', dpi=120, bbox_inches='tight')
#plt.show()
