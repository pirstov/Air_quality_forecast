import numpy as np
import matplotlib.pyplot as plt
import cartopy  
import cartopy.crs as ccrs  
import cartopy.feature as cfeature
import xarray as xr
import pandas as pd
from datetime import datetime, timedelta
import os 
import glob
from PIL import Image

# Base path where NetCDF files are stored
base_path = "/scratch/project_2012160/CHIMERE/chimere_forecast/nest-FINLAND6-forecast/"

# Find the most recently created .nc file
nc_files = glob.glob(os.path.join(base_path, "chim_nest-FINLAND6-forecast_??????*_72_out.nc"))
if not nc_files:
    print("Error: No NetCDF file found in the directory.")
    exit()

file_path = max(nc_files, key=os.path.getctime)  # Select most recently created file
print(f"Using latest NetCDF file: {file_path}")

# Open the dataset
try:
    ds = xr.open_dataset(file_path)
except FileNotFoundError:
    print(f"Error: Unable to open {file_path}.")
    exit()

# Define variables to plot with shaded color maps
variables = {
    "PM25": {"label": "PM$_{2.5}$", "cmap": "cividis", "vmin": 0, "vmax": 5},  # Fine particulate matter
    "PM10": {"label": "PM$_{10}$", "cmap": "RdYlBu_r", "vmin": 0, "vmax": 10},   # Coarse particulate matter
    "NO2": {"label": "NO$_{2}$", "cmap": "Spectral_r", "vmin": 0, "vmax": 2},     # Nitrogen dioxide
    "O3": {"label": "O$_{3}$", "cmap": "coolwarm", "vmin": 0, "vmax": 30}      # Ozone
}

# Define function to delete old plots
def delete_old_plots(directory):
    if os.path.exists(directory):
        for file in glob.glob(os.path.join(directory, "*.png")):
            os.remove(file)
        print(f"Deleted existing plots in {directory}.")
    else:
        os.makedirs(directory)
        print(f"Created directory: {directory}.")

# Define function to create plots
def create_plot(sub, time_label, output_file, variable_name):
    cproj = ccrs.LambertConformal(central_longitude=24.2896, central_latitude=61.8417)
    
    fig = plt.figure(figsize=(6,6))
    ax = plt.subplot(projection=cproj)
    
    vmin = variables[variable_name]["vmin"]
    vmax = variables[variable_name]["vmax"]
    cmap = variables[variable_name]["cmap"]
    
    c = plt.pcolormesh(
        ds.nav_lon, ds.nav_lat, sub, cmap=cmap, transform=ccrs.PlateCarree(),
        shading='gouraud', vmin=vmin, vmax=vmax  # Using 'gouraud' for smooth shading
    )
    
    cbar = plt.colorbar(c, fraction=0.040, pad=0.2, extend="both")
    cbar.set_label(label=f'{variables[variable_name]["label"]} [µg m$^{-3}$]' if variable_name != "O3" else "O$_3$ [ppb]", fontsize=12)
    cbar.ax.tick_params(labelsize=12)

    ax.coastlines(color='k', linewidth=1)
    ax.add_feature(cartopy.feature.BORDERS, color='k', linewidth=0.6, alpha=0.3)
    
    # Highlight Finland's borders with a thick black line
    finland_border = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_0_countries',
        scale='10m',
        facecolor='none')
    ax.add_feature(finland_border, edgecolor='black', linewidth=1.5)
    
    # Mark Helsinki, Turku, and Hyytiälä on the map
    locations = {
        "Helsinki": (24.9458, 60.1920),
        "Turku": (22.2666, 60.4518),
        "Hyytiälä": (24.2948, 61.8456)
    }
    
    for city, (lon, lat) in locations.items():
        ax.plot(lon, lat, marker='o', color='red', markersize=5, transform=ccrs.PlateCarree())
        ax.text(lon + 0.5, lat, city, fontsize=10, transform=ccrs.PlateCarree(), color='black')
    
    ax.set_title(f"{variables[variable_name]['label']} Concentration\n{time_label} (Local Time)", fontweight="bold", fontsize=12)

    gl = ax.gridlines(draw_labels=True, alpha=0.3, dms=False, x_inline=False, y_inline=False)
    gl.xlabel_style = {'rotation': 0}

    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

# Extract date from filename
filename = os.path.basename(file_path)
date_str = filename.split("_")[2]  
start_time_utc = datetime.strptime(date_str, "%Y%m%d%H")

# Convert time to Helsinki local time (UTC+2)
start_time_local = start_time_utc + timedelta(hours=2) # TODO: There's some problem with the file timestamp and plot timestamp
plot_date_str = start_time_local.strftime('%Y-%m-%d')  # Extract date for naming

output_dir = "pm_plots"
delete_old_plots(output_dir)  # Delete existing plots before creating new ones

# Generate 24 plots for each variable
for variable in variables.keys():
    for i in range(24):  
        data_time_utc = start_time_utc + timedelta(hours=i)  # Original UTC time
        data_time_local = start_time_local + timedelta(hours=i)  # Convert to local time
        time_label = data_time_local.strftime('%Y-%m-%d %H:%M:%S')

        try:
            sub = ds[variable].sel(bottom_top=1).sel(time_counter=data_time_utc, method="nearest")
        except KeyError:
            print(f"Skipping time step {time_label} for {variable} - Not found in dataset.")
            continue

        # Naming format: variable_date_01.png, variable_date_02.png, ...
        output_file = os.path.join(output_dir, f"{variable}_{plot_date_str}_{i+1:02d}.png")
        create_plot(sub, time_label, output_file, variable)

print(f"Plots for PM₂.₅, PM₁₀, NO₂, and O₃ created for {plot_date_str} in local time.")

# Create webp animations
def create_webp_animation(feat):
    file_pattern = f"pm_plots/{feat}_{plot_date_str}_*.png"
    image_files = sorted(glob.glob(file_pattern))

    if not image_files:
        print(f"No images found for {feat}. Skipping animation.")
        return

    images = [Image.open(img) for img in image_files]
    f_out = f"pm_animations/{feat}_animation.webp"
    images[0].save(f_out, save_all=True, append_images=images[1:], duration=1000, loop=0)
    print(f"Animation saved as {f_out}")

os.makedirs("pm_animations", exist_ok=True)
for var in variables.keys():
    create_webp_animation(var)

