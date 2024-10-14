from os.path import basename, join

import matplotlib.pyplot as plt
import rioxarray as xr


def plot_geotiff(geotiff_path: str, workdir: str, invalid_value: float = 9999.0):
    # import xarray as xr
    dem = xr.open_rasterio(geotiff_path)
    x = dem[0]
    x = x.where(x != invalid_value)
    x.plot()
    plt.title(x.TIME)
    plt.savefig(join(workdir, basename(geotiff_path).replace("tif", "png")))
    plt.close()
