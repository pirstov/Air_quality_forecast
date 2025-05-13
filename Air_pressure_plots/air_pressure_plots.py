from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as crs
import cartopy.feature as cfeature
from wrf import getvar, interplevel, to_np, latlon_coords, get_cartopy, ALL_TIMES
import os
from datetime import datetime

# Directory containing the wrfout files
directory = "/scratch/project_2012160/CHIMERE/chimere_forecast/nest-FINLAND6-forecast/"
files = [f for f in os.listdir(directory) if f.startswith('wrfout_d01_')]

# Extract datetime from filename and get the latest
def extract_datetime(filename):
    date_str = filename.split('_')[2]
    time_str = filename.split('_')[3]
    return f"{date_str}_{time_str}"

latest_file = max(files, key=lambda f: extract_datetime(f))
ncfile_path = os.path.join(directory, latest_file)

# Open NetCDF file
ncfile = Dataset(ncfile_path)

# Read all available times
times = getvar(ncfile, "times", timeidx=ALL_TIMES, meta=False)
times_dt = [np.datetime64(t).astype('datetime64[s]').astype(datetime) for t in times]

# Loop through each hour of the day
for target_hour in range(24):
    target_indices = [i for i, t in enumerate(times_dt) if t.hour == target_hour and t.minute == 0]
    if not target_indices:
        print(f"No data found for {target_hour:02d}:00:00")
        continue

    time_idx = target_indices[0]

    # Get variables at the selected time step
    p = getvar(ncfile, "pressure", timeidx=time_idx)
    z = getvar(ncfile, "z", timeidx=time_idx)
    ua = getvar(ncfile, "ua", timeidx=time_idx)
    va = getvar(ncfile, "va", timeidx=time_idx)
    wspd = getvar(ncfile, "wspd_wdir", timeidx=time_idx)

    # Interpolate to 400 hPa
    ht_400 = interplevel(z, p, 400)
    u_400 = interplevel(ua, p, 400)
    v_400 = interplevel(va, p, 400)
    wspd_400 = interplevel(wspd, p, 400)

    wspd_2d = to_np(wspd_400[0, :, :])
    lats, lons = latlon_coords(ht_400)
    cart_proj = get_cartopy(ht_400)

    # PLOTTING
    fig = plt.figure(figsize=(12, 9))
    ax = plt.axes(projection=cart_proj)
    ax.coastlines(color='k', linewidth=2)
    gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.3, linestyle='--')
    gl.xlabel_style = {'size': 15}
    gl.ylabel_style = {'size': 15}

    levels_ht = np.arange(7000., 8000., 15.)
    contours = plt.contour(to_np(lons), to_np(lats), to_np(ht_400), levels=levels_ht, colors="black", transform=crs.PlateCarree())
    plt.clabel(contours, inline=1, fontsize=10)

    levels_ws = np.arange(0, 40, 1)
    wspd_plot = plt.contourf(to_np(lons), to_np(lats), wspd_2d,
                             levels=levels_ws, cmap="viridis",
                             transform=crs.PlateCarree(), extend="both")
    cbar = plt.colorbar(wspd_plot, fraction=0.042, pad=0.15)
    cbar.ax.set_ylabel('Wind speed (m/s)', fontsize=16)

    plt.quiver(to_np(lons[::6, ::6]), to_np(lats[::6, ::6]),
               to_np(u_400[::6, ::6]), to_np(v_400[::6, ::6]),
               transform=crs.PlateCarree(), scale=1000, color="white")

    ax.set_extent([19, 31, 59.5, 69], crs=crs.PlateCarree())
    ax.add_feature(cfeature.BORDERS, linestyle=":", linewidth=1.5)
    ax.add_feature(cfeature.LAND, edgecolor='black')

    cities = {"Helsinki": (24.94, 60.17), "Tampere": (23.76, 61.5), "Oulu": (25.47, 65.01)}
    for city, (lon, lat) in cities.items():
        ax.plot(lon, lat, marker='x', markersize=8, color='red', transform=crs.PlateCarree())
        ax.text(lon + 0.3, lat, city, fontsize=12, color='red', transform=crs.PlateCarree())

    plot_time = times_dt[time_idx].strftime("%Y-%m-%d %H:%M:%S")
    plt.title(f"400 hPa Geopotential Height and Wind Speed - {plot_time}", fontsize=22)

    # Save plot
    save_time = times_dt[time_idx].strftime("%Y%m%d_%H%M")
    save_path = f"/scratch/project_2012160/Air_quality_forecast/pressure_plots/air_press_{save_time}.png"
    fig.savefig(save_path, dpi=500)
    plt.close(fig)  # Close the figure to save memory
    print(f"Saved: {save_path}")
