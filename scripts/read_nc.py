import os
from datetime import datetime

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import imageio
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from dateutil.relativedelta import relativedelta
from netCDF4 import Dataset, num2date

# Path to your NetCDF4 file
# file_path = "etc/data/isimip2b/trm-tsukuba_gfdl-esm2m_ewembi_rcp60_2005soc_an-tot-heat-all_global_annual_2006_2099.nc4"
# file_path = "/tmp/climate_model_esr/data/gfdl-esm4_r1i1p1f1_ssp370_tos_60arcmin_global_monthly_2015_2100.nc"
var_name = "hurs"
file_path = f"etc/climate_model_esr/data3/mri-esm2-0_r1i1p1f1_w5e5_ssp370_{var_name}_global_daily_2015_2020.nc"
title_str = f"{var_name}, SSP370"

# Open the NetCDF4 file
with Dataset(file_path, mode="r") as fid:
    lat = fid.variables["lat"][:]
    lon = fid.variables["lon"][:]
    var = fid.variables[var_name][:]
    time_var = fid.variables["time"]

    if time_var.units == "months since 1601-1-1 00:00:00":
        time_vars = []
        len_time_var = time_var.shape[0]
        for i in range(len_time_var):
            time_vars.append(
                datetime(1601, 1, 1) + relativedelta(months=+int(time_var[i].data))
            )
    elif time_var.units == "days since 2015-1-1 00:00:00":
        time_vars = []
        len_time_var = time_var.shape[0]
        for i in range(len_time_var):
            time_vars.append(
                datetime(2015, 1, 1) + relativedelta(days=+int(time_var[i].data))
            )
    else:
        time_vars = [
            proc_data.strftime("%Y")
            for proc_data in num2date(
                time_var[:] * 365.25,
                units=time_var.units.replace("years", "days"),
                calendar=(
                    time_var.calendar
                    if "calendar" in time_var.ncattrs()
                    else "standard"
                ),
            )
        ]


# Define the bounds for New Zealand and South Pacific region
lat_bounds = [-50, -30]
lon_bounds = [165, 180]

download_data = True
create_plot = False

if download_data:
    ds = xr.open_dataset(file_path)
    cropped_ds = ds.sel(
        lat=slice(lat_bounds[1], lat_bounds[0]), lon=slice(lon_bounds[0], lon_bounds[1])
    )
    selected_var = cropped_ds[[var_name, "lat", "lon"]]
    selected_var.attrs["title"] = var_name
    selected_var.attrs["institution"] = "MRI"
    selected_var.attrs["senario"] = "SSP370"
    del selected_var.attrs["references"]
    del selected_var.attrs["contact"]
    del selected_var.attrs["project"]
    del selected_var.attrs["summary"]
    selected_var.to_netcdf(f"{var_name}.nc")

if create_plot:

    # Find the indices for the latitude and longitude bounds
    lat_indices = np.where((lat >= lat_bounds[0]) & (lat <= lat_bounds[1]))[0]
    lon_indices = np.where((lon >= lon_bounds[0]) & (lon <= lon_bounds[1]))[0]

    # Extract the data within the bounds
    lat_subset = lat[lat_indices]
    lon_subset = lon[lon_indices]
    var_subset = var[:, lat_indices, :][:, :, lon_indices]

    lat_subset = lat_subset[::-1]
    var_subset = var_subset[:, ::-1, :]

    # Create a meshgrid for lat and lon
    lon_subset, lat_subset = np.meshgrid(lon_subset, lat_subset)
    var_subset = np.ma.masked_where(var_subset == 0, var_subset)

    frames = []
    ts_data = []
    for i, proc_t in enumerate(range(var_subset.shape[0])):

        # Plot the data
        fig = plt.figure(figsize=(6, 7))
        ax1 = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

        ax1.coastlines()
        ax1.add_feature(cfeature.BORDERS, linestyle=":")
        ax1.add_feature(cfeature.LAND, edgecolor="black")
        ax1.add_feature(cfeature.OCEAN)

        # Create a custom colormap
        cmap = plt.cm.Reds
        cmap.set_bad(color="white")  # Set the color for masked values to white

        img = ax1.imshow(
            var_subset[proc_t, :, :],
            extent=[lon_bounds[0], lon_bounds[1], lat_bounds[0], lat_bounds[1]],
            origin="lower",
            transform=ccrs.PlateCarree(),
            cmap=cmap,
            interpolation="none",
        )

        # img.set_clim(0.0, var_subset.max())
        img.set_clim(var_subset.min(), var_subset.max())

        cbar = fig.colorbar(
            img, ax=ax1, shrink=0.3, aspect=10
        )  # Adjust shrink and aspect to change size

        ts_data.append(np.sum(var_subset[0 : proc_t + 1, :, :]))

        ts_remain = [np.nan] * (var_subset.shape[0] - len(ts_data))
        ts_all = ts_data + ts_remain

        plt.title(f"{title_str} \n Month: {time_vars[proc_t].strftime('%Y-%m-%d')}")
        # Save the frame to a file
        frame_filename = f"tmp_frame_{proc_t}.png"
        plt.savefig(frame_filename, bbox_inches="tight")
        plt.close()

        # Read the frame and add it to the list
        frames.append(imageio.imread(frame_filename))

    """
    frames = []
    ts_data = []
    for proc_t in range(var_subset.shape[0]):

        # Plot the data
        fig = plt.figure(figsize=(15, 7))
        ax1 = fig.add_subplot(1, 2, 1, projection=ccrs.PlateCarree())

        # Create the second subplot without any projection
        ax2 = fig.add_subplot(1, 2, 2)

        fig.subplots_adjust(wspace=0.05, hspace=0.0, top=0.92)

        ax1.coastlines()
        ax1.add_feature(cfeature.BORDERS, linestyle=":")
        ax1.add_feature(cfeature.LAND, edgecolor="black")
        ax1.add_feature(cfeature.OCEAN)

        # Create a custom colormap
        cmap = plt.cm.Reds
        cmap.set_bad(color="white")  # Set the color for masked values to white

        img = ax1.imshow(
            np.sum(var_subset[0 : proc_t + 1, :, :], 0),
            extent=[lon_bounds[0], lon_bounds[1], lat_bounds[0], lat_bounds[1]],
            origin="lower",
            transform=ccrs.PlateCarree(),
            cmap=cmap,
            interpolation="none",
        )

        img.set_clim(0.0, var_subset.max() * 10.0)

        cbar = fig.colorbar(
            img, ax=ax1, shrink=0.3, aspect=10
        )  # Adjust shrink and aspect to change size

        ts_data.append(np.sum(var_subset[0 : proc_t + 1, :, :]))

        ts_remain = [np.nan] * (var_subset.shape[0] - len(ts_data))
        ts_all = ts_data + ts_remain
        ax2.plot(range(len(ts_all)), ts_all, "k-")
        ax2.set_xlim(0, len(ts_all) - 1)
        ax2.set_ylim(0, np.sum(var_subset))
        ax2.set_xticks(range(len(ts_all))[::15])  # Set x-ticks at every 10th position
        ax2.set_xticklabels(time_vars[::15])  # Set x-tick labels at every 10th position

        plt.suptitle(f"{title_str} \n Year: {time_vars[proc_t]}")
        # Save the frame to a file
        frame_filename = f"tmp_frame_{proc_t}.png"
        plt.savefig(frame_filename, bbox_inches="tight")
        plt.close()

        # Read the frame and add it to the list
        frames.append(imageio.imread(frame_filename))
    """
    # Create a GIF from the frames
    imageio.mimsave(
        "output.gif", frames, duration=0.2, loop=0
    )  # Adjust duration as needed

    for frame_filename in [
        f"tmp_frame_{proc_t}.png" for proc_t in range(var_subset.shape[0])
    ]:
        os.remove(frame_filename)
