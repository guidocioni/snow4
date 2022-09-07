# Configuration file for some common variables to all script
from mpl_toolkits.basemap import Basemap  # import Basemap matplotlib toolkit
import numpy as np
from matplotlib.offsetbox import AnchoredText
import matplotlib.colors as colors
import pandas as pd
from datetime import datetime
import os

# Output folder for images
folder_images = os.environ.get('WORK_FOLDER','/home/ekman/ssd/guido/')
# Resolution of images
dpi_resolution = 100

base_url = 'https://opendata.dwd.de/weather/nwp/snow4/obdn/'
grid_file = 'https://opendata.dwd.de/weather/nwp/snow4/grid/snow4_grid_germany.dat.bz2'


def annotation(ax, text, loc='upper right'):
    at = AnchoredText('%s' % text, prop=dict(size=8), frameon=True, loc=loc)
    at.patch.set_boxstyle("round,pad=0.,rounding_size=0.1")
    ax.add_artist(at)


def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=256):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap


def get_run(date):
    if 2 <= date.hour <= 7:
        run = '00'
    elif 8 <= date.hour <= 13:
        run = '06'
    elif 14 <= date.hour <= 19:
        run = '12'
    elif 20 <= date.hour <= 23:
        run = '18'
    return(run)


def index_marks(nrows, chunk_size):
    return range(1 * chunk_size, (nrows // chunk_size + 1) * chunk_size, chunk_size)


def split(df, chunk_size):
    indices = index_marks(df.shape[0], chunk_size)
    return np.split(df, indices)


def get_snow_data(datetime_now):
    run = get_run(datetime_now)
    filename = 'sn_vzp%s_obdn%s.asc.zip' % (datetime_now.strftime(
        '%Y%m%d') + run, datetime_now.strftime('%y%m%d') + run)

    widths = np.full(671, 7, dtype=int).tolist()
    df = pd.read_fwf(base_url + filename, skiprows=[0, 911, 1822, 2733, 3644, 4555],
                     widths=widths, header=None, lineterminator='\n', na_values=-99.9, compression='zip')

    date_end_file = filename[21:29]
    time = pd.date_range(end=datetime.strptime(
        date_end_file, '%y%m%d%H'), freq='1h', periods=6)

    chunks = split(df, 910)
    snow = np.empty(shape=(0, 910, 671), dtype=float)
    for c in chunks:
        if c.values.shape[0] != 0:
            snow = np.append(snow, [c.values], axis=0)
    snow = np.ma.masked_invalid(snow)
    snow = np.ma.masked_less_equal(snow, 1)

    return(time, snow)


def get_coords(height=False):
    ''' Get longitude and latitude from the coordinate file. If height is set to True then also get
    height values.'''
    coord = pd.read_fwf(grid_file, skiprows=20, header=None,
                        lineterminator='\n', compression='bz2')
    longitudes = np.array(coord)[0:910, 1:].astype("float")

    coord = pd.read_fwf(grid_file, skiprows=932, header=None,
                        lineterminator='\n', compression='bz2')
    latitudes = np.array(coord)[0:910, 1:].astype("float")

    if height:
        coord = pd.read_fwf(grid_file, skiprows=1844, header=None,
                            lineterminator='\n', compression='bz2')
        height = np.array(coord)[0:910, 1:].astype("float")
        height[height == 900] = np.nan
        height[height == -900] = np.nan
        return(longitudes, latitudes, height)
    else:
        return(longitudes, latitudes)
