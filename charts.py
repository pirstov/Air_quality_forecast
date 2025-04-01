import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import os
import glob
from datetime import datetime, timedelta
from PIL import Image

# === Configuration ===
pie_variables = ["pHNO3", "pNH3", "pH2SO4", "pBCAR"]
oa_components = [
    "pPOA1", "pPOA2", "pPOA3", "pPOA4", "pPOA5", "pPOA6",
    "pBSOA1", "pBSOA2", "pBSOA3", "pBSOA4",
    "pASOA1", "pASOA2", "pASOA3", "pASOA4"
]

city_coords = {
    "Helsinki": (24.9458, 60.1920),
    "Tampere": (23.7610, 61.4978),
    "Turku": (22.2666, 60.4518),
    "Hyytiälä": (24.2948, 61.8456)
}

colors = ["#c33d2b", "#2a6496", "#4a7b4a", "#7a5d8c", "#c98a00"]
labels = ["pHNO3", "pNH3", "pH2SO4", "pBCAR", "OA"]

output_dir = "hourly_pie_charts"
os.makedirs(output_dir, exist_ok=True)

# === File loading ===
base_path = "/scratch/project_2012160/CHIMERE/chimere_forecast/nest-FINLAND6-forecast/"
nc_files = glob.glob(os.path.join(base_path, "chim_nest-FINLAND6-forecast_??????*_72_out.nc"))
if not nc_files:
    raise FileNotFoundError("No .nc files found in the specified directory.")

file_path = max(nc_files, key=os.path.getctime)
ds = xr.open_dataset(file_path)

filename = os.path.basename(file_path)
date_str = filename.split("_")[2]
start_time_utc = datetime.strptime(date_str, "%Y%m%d%H")
start_time_local = start_time_utc + timedelta(hours=2)

# === Utility functions ===
def get_nearest_grid_point(ds, lat, lon):
    lat_diff = ds["nav_lat"] - lat
    lon_diff = ds["nav_lon"] - lon
    dist = np.sqrt(lat_diff**2 + lon_diff**2)
    min_dist_idx = np.unravel_index(np.argmin(dist.values), dist.shape)
    return min_dist_idx  # (y_idx, x_idx)

def get_city_data(ds, time, lat, lon):
    try:
        y_idx, x_idx = get_nearest_grid_point(ds, lat, lon)
        values = [
            ds[v].sel(time_counter=time, method="nearest")
                 .isel(bottom_top=1, y=y_idx, x=x_idx).values.item()
            for v in pie_variables
        ]
        oa_value = sum([
            ds[v].sel(time_counter=time, method="nearest")
                 .isel(bottom_top=1, y=y_idx, x=x_idx).values.item()
            for v in oa_components
        ])
        values.append(oa_value)
        return np.array(values)
    except Exception as e:
        print(f"Error reading data at ({lat}, {lon}) for time {time}: {e}")
        return np.zeros(5)

# === Generate hourly pie charts ===
image_files = []
for hour in range(24):
    t_utc = start_time_utc + timedelta(hours=hour)
    t_local = start_time_local + timedelta(hours=hour)
    timestamp_str = t_local.strftime('%Y-%m-%d %H:%M:%S')

    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    axes = axes.flatten()

    for idx, (city, (lon, lat)) in enumerate(city_coords.items()):
        data = get_city_data(ds, t_utc, lat, lon)
        total = data.sum()
        ax = axes[idx]
        if total > 0:
            data = data / total
            ax.pie(data, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90, textprops={'fontsize': 8})
        else:
            ax.text(0.5, 0.5, "No data", ha='center', va='center')
        ax.set_title(f"{city}", fontsize=10)

    fig.suptitle(f"Aerosol Composition - {timestamp_str} (Local Time)", fontsize=14)
    img_file = os.path.join(output_dir, f"pie_{hour:02d}.png")
    fig.savefig(img_file, dpi=200, bbox_inches='tight')
    plt.close(fig)
    image_files.append(img_file)

# === Create .webp animation ===
animation_dir = "animations"
os.makedirs(animation_dir, exist_ok=True)
webp_output = os.path.join(animation_dir, "aerosol_composition_animation.webp")

images = [Image.open(f) for f in image_files]

# Get the size of the first image
base_size = images[0].size

# Resize all images to the same dimensions
images = [img.resize(base_size) for img in images]

# Save the animation
images[0].save(webp_output, save_all=True, append_images=images[1:], duration=1000, loop=0)
print(f"WebP animation saved: {webp_output}")