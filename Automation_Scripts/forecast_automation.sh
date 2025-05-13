#!/bin/bash
#SBATCH --account=project_2012160
#SBATCH --nodes=4
#SBATCH --partition=medium
#SBATCH --time=10:00:00
#SBATCH --ntasks-per-node=128
#SBATCH --output=forecast_automation_%j.out
#SBATCH --error=forecast_automation_%j.err

source /appl/profile/zz-csc-env.sh

NETCDFINC=${NETCDF_FORTRAN_INSTALL_ROOT}/include NETCDFLIBF=${NETCDF_FORTRAN_INSTALL_ROOT}/lib
module load nco python-data/3.10-24.04 gcc/11.2.0 openmpi/4.1.2 openblas/0.3.18-omp blitz/1.0.2 eccodes/2.24.2 netcdf-c/4.8.1 netcdf-fortran/4.5.3 hdf5/1.10.7-mpi

date

cd  /projappl/project_2012160/CHIMERE/
echo "Start Automation Executing!"
./00_downloadNCEP.sh
echo "Download Completed!"
./01_forecast_FIN18.sh
echo "Fin18 Executed!"
./01_forecast_FIN6.sh
echo "Fin6 Executed!"
echo "Process END!!!"

echo "Clean Old Files!!!"
./cleanup_chim_fin_forecast18.sh
./cleanup_chim_fin_forecast6.sh

# After running the model, carry out validation and upload the validation data to Allas
./forecast_automation_validation.sh

# Extract some simulation data for Helsinki to be used in comparison to the random forest model
sbatch extract_pm25_helsinki.sh

### Create the forecast plots and upload them to Allas ###
# Generate pollutant forecast plots, air pressure plots and aerosol plots
sbatch generate_all_plots.sh

# TODO: Allas credentials not found, try to load credentials here too
set -a
source allas_s3_cred_v2.env
set +a

# Upload the data to Allas one by one
sbatch upload_plots_to_allas.sh /scratch/project_2012160/Air_quality_forecast/pm_plots pm_plots

sbatch upload_plots_to_allas.sh /scratch/project_2012160/Air_quality_forecast/aerosol_plots aerosol_plots

sbatch upload_plots_to_allas.sh /scratch/project_2012160/Air_quality_forecast/pressure_plots pressure_plots
