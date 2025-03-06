import numpy as np
import matplotlib.pyplot as plt
import cartopy  
import cartopy.crs as ccrs  
import cartopy.feature as cfeature
import xarray as xr
from datetime import datetime, timedelta
import os
import imageio  
import glob 

base_path = "/scratch/project_2012160/CHIMERE/chimere_forecast/nest-FINLAND6-forecast/"
nc_files = sorted(glob.glob(os.path.join(base_path, "chim_nest-FINLAND6-forecast_??????*_72_out.nc")), reverse=True)

if not nc_files:
    print("Error: No NetCDF file found in the directory.")
    exit()

file_path = nc_files[0]  # Latest available file
print(f"Using NetCDF file: {file_path}")

try:
    ds = xr.open_dataset(file_path)
except FileNotFoundError:
    print(f"Error: Unable to open {file_path}.")
    exit()
    
def create_plot(sub, time_label, output_file, cmap='magma_r'):
    """Creates a PM₂.₅ concentration plot."""
    cproj = ccrs.LambertConformal(central_longitude=24.2896, central_latitude=61.8417)
    
    fig = plt.figure(figsize=(6,6))
    ax = plt.subplot(projection=cproj)
    
    c = plt.pcolormesh(
        ds.nav_lon, ds.nav_lat, sub, cmap=cmap, transform=ccrs.PlateCarree(),
        shading='gouraud', vmin=0, vmax=20
    )
    
    cbar = plt.colorbar(c, fraction=0.040, pad=0.2, extend="both")
    cbar.set_label(label='PM$_{2.5}$ [µg m$^{-3}$]', fontsize=12)
    cbar.ax.tick_params(labelsize=12)

    ax.coastlines(color='k', linewidth=1)
    ax.add_feature(cartopy.feature.BORDERS, color='k', linewidth=0.6, alpha=0.3)
    ax.set_title(f"PM$_{{2.5}}$ Concentration\n{time_label}", fontweight="bold", fontsize=12)

    gl = ax.gridlines(draw_labels=True, alpha=0.3, dms=False, x_inline=False, y_inline=False)
    gl.xlabel_style = {'rotation': 0}

    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

filename = os.path.basename(file_path)
date_str = filename.split("_")[2]  
start_time = datetime.strptime(date_str, "%Y%m%d%H")

output_dir = "pm_plots"
os.makedirs(output_dir, exist_ok=True)

plot_files = []
for i in range(72):  
    data_time = start_time + timedelta(hours=i)  
    time_label = data_time.strftime('%Y-%m-%d %H:%M:%S')

    try:
        sub = ds.PM25.sel(bottom_top=1).sel(time_counter=data_time, method="nearest")
    except KeyError:
        print(f"Skipping time step {time_label} - Not found in dataset.")
        continue

    output_file = os.path.join(output_dir, f"pm_plot_{i:02d}.png")
    create_plot(sub, time_label, output_file)
    plot_files.append(output_file)

gif_filename = "pm_forecast.gif"
gif_output = os.path.join(output_dir, gif_filename)

with imageio.get_writer(gif_output, mode='I', duration=0.5) as writer:
    for plot_file in plot_files:
        image = imageio.imread(plot_file)
        writer.append_data(image)

print(f"GIF created: {gif_output}")