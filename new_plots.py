import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr
from datetime import datetime, timedelta
import os
import cv2
import glob

# Base directory for NetCDF files
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

# Extract start time from filename
filename = os.path.basename(file_path)
date_str = filename.split("_")[2]  
start_time = datetime.strptime(date_str, "%Y%m%d%H")

# Define pollutants with high-contrast colormaps
variables = {
    "PM2.5": {"name": "PM$_{2.5}$", "cmap": "coolwarm"},
    "PM10": {"name": "PM$_{10}$", "cmap": "cividis"},
    "NO2": {"name": "NO$_{2}$", "cmap": "turbo"},
    "O3": {"name": "O$_{3}$", "cmap": "Spectral"},
}

# Function to dynamically determine color scale
def get_vmin_vmax(data):
    """Calculate min-max range for better contrast scaling."""
    return np.nanpercentile(data, 5), np.nanpercentile(data, 95)  # Use 5th-95th percentile range

# Function to create video with pause functionality
def create_video(ds, var_name, props, start_time, video_output):
    """Generates an .mp4 video for a single pollutant with high-quality playback."""
    images = []
    fps = 5  # Frames per second (adjust as needed)

    for i in range(72):  
        data_time = start_time + timedelta(hours=i)
        time_label = data_time.strftime('%Y-%m-%d %H:%M:%S')

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={"projection": ccrs.LambertConformal(central_longitude=24.2896, central_latitude=61.8417)})

        try:
            sub = ds[var_name].sel(bottom_top=1).sel(time_counter=data_time, method="nearest")
        except KeyError:
            print(f"Skipping time step {time_label} for {var_name} - Not found in dataset.")
            plt.close(fig)
            continue

        # Dynamically determine vmin and vmax
        vmin, vmax = get_vmin_vmax(sub)

        # Create the plot
        c = ax.pcolormesh(ds.nav_lon, ds.nav_lat, sub, cmap=props["cmap"], transform=ccrs.PlateCarree(),
                          shading='gouraud', vmin=vmin, vmax=vmax)

        ax.coastlines(color='k', linewidth=1)
        ax.add_feature(cfeature.BORDERS, color='k', linewidth=0.6, alpha=0.3)
        ax.set_title(f"{props['name']} Concentration\n{time_label}", fontsize=12, fontweight="bold")

        cbar = plt.colorbar(c, ax=ax, fraction=0.05, pad=0.05, extend="both")
        cbar.set_label(label=f"{props['name']} [µg m$^{-3}$]", fontsize=12, fontweight="bold")
        cbar.ax.tick_params(labelsize=10)

        plt.tight_layout()

        # Save frame as image
        fig.canvas.draw()
        image = np.array(fig.canvas.renderer.buffer_rgba())
        images.append(image)

        plt.close(fig)  # Free memory

    if not images:
        print(f"No valid frames generated for {var_name}. Skipping video creation.")
        return

    # Convert images to video using OpenCV
    height, width, _ = images[0].shape
    video_writer = cv2.VideoWriter(video_output, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))

    for img in images:
        video_writer.write(cv2.cvtColor(img, cv2.COLOR_RGBA2BGR))  # Convert RGBA to BGR for OpenCV

    video_writer.release()
    print(f"Video created: {video_output}")

# Generate videos for each pollutant
for var, props in variables.items():
    video_filename = f"{var}_forecast.mp4"
    create_video(ds, var, props, start_time, video_filename)
 