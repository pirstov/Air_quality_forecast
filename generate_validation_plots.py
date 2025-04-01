import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import json
import datetime
import urllib.parse
import xarray as xr
from netCDF4 import Dataset
from pandas.tseries.offsets import DateOffset
import argparse

# EXAMPLE USAGE
# python generate_validation_plots.py "val_data_2025_03_05.nc" 3

VALIDATION_MEASUREMENTS = ['HYY_META.Tmm168',       # Temperature, 16.8 m
                        'HYY_META.RH168',           # Relative humidity, 16.8 m
                        'HYY_META.WDU84',           # Wind direction 8.4 m
                        'HYY_META.WSU84',           # Wind speed 8.4 m
                        'HYY_META.Precipacc']       # Precipitation

def get_smear_stations():
        # Check the list of stations
        url = "https://smear-backend.2.rahtiapp.fi/search/station"
        response = requests.get(url)

        if response.status_code == 200:
            print(f"Stations available through the API")
            data = response.json()
            for i in data:
                print(i)

def get_smear_data(start_date = datetime.datetime.now(), days_to_fetch = 3, variables_to_fetch = VALIDATION_MEASUREMENTS):
    '''This function will fetch the observational data from Hyytiälä weather station.'''

    # Try to fetch the temperature data from 16.8 meters above ground level for the past two days
    datetime_start = start_date
    num_days_to_fetch = datetime.timedelta(days = days_to_fetch)

    datetime_end = (datetime_start + num_days_to_fetch).isoformat()
    datetime_start = datetime_start.isoformat()

    print(f"\nFetching observational data from {datetime_start} to {datetime_end}.")

    dt_start = urllib.parse.quote_plus(datetime_start)
    dt_end = urllib.parse.quote_plus(datetime_end)

    # Formulate the url string
    fetch_request = "https://smear-backend.2.rahtiapp.fi/search/timeseries?aggregation=ARITHMETIC"

    # Add starting datetime
    fetch_request += "&from=" + dt_start

    # Add length of interval between data points (in minutes, 1-60)
    fetch_request += "&interval=60"
    # Add quality (ANY or CHECKED)
    fetch_request += "&quality=ANY"

    # Add request variables
    for var in variables_to_fetch:
        fetch_request += "&tablevariable=" + var

    # Finally, add the ending datetime
    fetch_request += "&to=" + dt_end

    #print(f"Using the following URL:\n{fetch_request}")
    response = requests.get(fetch_request)

    if response.status_code == 200:
        # Fetch OK
        data = response.json()

        # A dictionary is returned, data will contain the measurements with time stamps
        df = pd.DataFrame.from_dict(data['data'])

        # Transform the time stamp into a default datetime format, assign it as an index
        df['datetime'] = pd.to_datetime(df['samptime'], errors = 'coerce')
        df.set_index('datetime', inplace = True)
        df.drop(columns = 'samptime', inplace = True)

        return df
    else:
        print(f"Unsuccessful")
        return pd.DataFrame()

def get_sim_data(file_name):
    df_sim = xr.open_dataset(file_name, engine = 'netcdf4')

    # The times of Chimere simulation are not in Helsinki time, need to adjust
    times = df_sim.Times.astype(str)
    utc_times = pd.to_datetime(times, format='%Y%m%d%H%M%S.%f')
    local_times = utc_times + DateOffset(hours=2)
    df_sim['local_times'] = pd.DatetimeIndex(local_times)

    # Go through each of the variables of interest, replacing the time counters with the datetime values
    df_sim = df_sim.assign_coords(hour=('local_times', local_times.hour))
    ignored_vars = ['Times']
    for var in df_sim.data_vars:
            df_sim[var] = df_sim[var].swap_dims({'time_counter':'local_times'})

    return df_sim

def prepare_sim_data(df_sim):
    MAGIC_LON = 43  # Magic number to reduce number of find_nearest calls to one
    MAGIC_LAT = 52  # Magic number to reduce number of find_nearest calls to one
    HYYTIALA_LON = 24.2896
    HYYTIALA_LAT = 61.8417

    def find_nearest(array, value):
        '''Helper function to select the grid point from the simulation output containing Hyytiälä measurement station'''
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx

    # Pick up the grid point corresponds to Hyytiälä
    idx_lon = find_nearest(df_sim.nav_lon[MAGIC_LON, :], HYYTIALA_LON)
    idx_lat = find_nearest(df_sim.nav_lat[:, MAGIC_LAT], HYYTIALA_LAT)

    # Vertical layer number, corresponds to the lowest layer
    VERT_LAYER_NUM = 1

    def select_grid_point(variable):
        '''Getter function which returns the data from grid point containing Hyytiälä station'''
        try:
            return variable.sel(bottom_top = VERT_LAYER_NUM).sel(x = idx_lon).sel(y = idx_lat)
        except:
            return variable.sel(x = idx_lon).sel(y = idx_lat)

    ch_temperature      = select_grid_point(df_sim.temp) - 273.15           # Temperature, from Kelvin to celsius
    ch_relhum           = select_grid_point(df_sim.sreh) * 100              # From [0...1] to [0%...100%]
    ch_precip           = select_grid_point(df_sim.topc)
    ch_pm25             = select_grid_point(df_sim.PM25)                    # UNUSED
    ch_win10_zonal      = select_grid_point(df_sim.u10m)
    ch_wind10_meridional= select_grid_point(df_sim.v10m)

    return ch_temperature, ch_relhum, ch_precip, ch_win10_zonal, ch_wind10_meridional

def compute_MAE(actual, predicted):
    '''Helper function for computed the mean absolute error (MAE) between two arrays'''
    return np.sum(np.abs(actual-predicted))/len(actual)

def plot_validation(time = np.array([x for x in range(100)]), chim = np.array([x**2.1 for x in range(100)]), obs = np.array([x**2 for x in range(100)]), label='y-axis', fig_name = 'dummy.png'):
    plt.figure(figsize = (8,4))
    plt.plot(time, obs, color='red', label='Observation')
    plt.plot(time, chim, color='blue', label='Simulation')
    plt.legend()
    plt.title(f"Forecast validation, MAE={round(compute_MAE(obs, chim),3)}")
    plt.ylabel(label)
    plt.grid()
    plt.savefig(fig_name, dpi = 350, bbox_inches='tight')
    plt.show()


def main():
    # Argument parser
    parser = argparse.ArgumentParser(description="Generate validation plots based on the provided simulation file and number of hours to validate over")

    # Defined arguments
    parser.add_argument('file_path', type=str, help='Path to the simulation file to be validated.')
    parser.add_argument('num_days', type=int, help='Number of days of validation data to be used')

    # Parse and access args
    args = parser.parse_args()
    file_path = args.file_path
    num_days = args.num_days

    df_sim = get_sim_data(file_name=file_path)
    df_obs = get_smear_data(start_date = pd.to_datetime(df_sim.local_times[0].values), days_to_fetch=num_days)

    sim_temp, sim_relhum, sim_precip, sim_wind10_zonal, sim_wind10_meridional = prepare_sim_data(df_sim)

    plot_validation(df_sim.local_times, sim_temp, df_obs['HYY_META.Tmm168'], 'Temperature (K)', 'validation_temp.png')
    plot_validation(df_sim.local_times, sim_relhum, df_obs['HYY_META.RH168'], 'Relative humidity', 'validation_relhum.png')
    plot_validation(df_sim.local_times, sim_precip, df_obs['HYY_META.Precipacc'], 'Precipitation', 'validation_precip.png')
    plot_validation(df_sim.local_times, np.sqrt(sim_wind10_zonal**2 + sim_wind10_meridional**2), df_obs['HYY_META.WSU84'], 'Wind speed (m/s)', 'validation_windsp.png')

    return

if __name__ == '__main__':
    main()


