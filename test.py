import xarray as xr
import matplotlib.pyplot as plt

# Path to your .nc file
file_path = '/scratch/project_2012160/CHIMERE/chimere_forecast/nest-FINLAND6-forecast/chim_nest-FINLAND6-forecast_2025030500_72_out.nc'

# Load the .nc file using xarray
ds = xr.open_dataset(file_path)

# List available variables
print(ds.data_vars)

# Suppose you want to visualize a variable called 'temperature'
if 'PM25' in ds:
    PM25 = ds['PM25']

    # Plot the data (this will create a static plot)
    PM25.plot()
    plt.title("PM25 Visualization")
    plt.show()
else:
    print("Variable 'PM25' not found in the dataset.") 