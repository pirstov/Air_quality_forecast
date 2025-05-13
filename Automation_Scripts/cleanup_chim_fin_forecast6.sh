#!/bin/bash



# Set the directory containing the forecast files

TARGET_DIR="/scratch/project_2012160/CHIMERE/chimere_forecast/nest-FINLAND6-forecast"



# Get the dates for today, yesterday, and two days ago in YYYYMMDD format

TODAY=$(date +"%Y%m%d")

YESTERDAY=$(date -d "yesterday" +"%Y%m%d")

DAY_BEFORE_YESTERDAY=$(date -d "2 days ago" +"%Y%m%d")



# Find and list files that would be deleted (without deleting them)

echo "Files that would be deleted:"



# List files for chim_nest-FINLAND6-forecast_*_72_out.nc

find "$TARGET_DIR" -type f   -name "chim_nest-FINLAND6-forecast_*_72_out.nc"   ! -name "*${TODAY}*"   ! -name "*${YESTERDAY}*"   ! -name "*${DAY_BEFORE_YESTERDAY}*"   -exec rm -f {} \;



# List files for chim_nest-FINLAND6-forecast_*_72_dem.nc

find "$TARGET_DIR" -type f   -name "chim_nest-FINLAND6-forecast_*_72_dem.nc"   ! -name "*${TODAY}*"   ! -name "*${YESTERDAY}*"   ! -name "*${DAY_BEFORE_YESTERDAY}*"   -exec rm -f {} \;



# List files for chim_nest-FINLAND6-forecast_*_72_bem.nc

find "$TARGET_DIR" -type f   -name "chim_nest-FINLAND6-forecast_*_72_bem.nc"   ! -name "*${TODAY}*"   ! -name "*${YESTERDAY}*"   ! -name "*${DAY_BEFORE_YESTERDAY}*"   -exec rm -f {} \;



# List files for chim_nest-FINLAND6-forecast_*_72_aem.nc

find "$TARGET_DIR" -type f   -name "chim_nest-FINLAND6-forecast_*_72_aem.nc"   ! -name "*${TODAY}*"   ! -name "*${YESTERDAY}*"   ! -name "*${DAY_BEFORE_YESTERDAY}*"   -exec rm -f {} \;

# List files for wrfout_d01_* (no _72_ added)

find "$TARGET_DIR" -type f   -name "wrfout_d01_*_00:00:00"   ! -name "*${TODAY}*"   ! -name "*${YESTERDAY}*"   ! -name "*${DAY_BEFORE_YESTERDAY}*"   -exec rm -f {} \;

find "$TARGET_DIR" -type f -name "chim_nest-FINLAND6-forecast_*_72_start.nc" ! -name "*${TODAY}*" ! -name "*${YESTERDAY}*" ! -name "*${DAY_BEFORE_YESTERDAY}*" -exec rm -f {} \;

find "$TARGET_DIR" -type f -name "end.*_72_nest-FINLAND6-forecast.nc" ! -name "*${TODAY}*" ! -name "*${YESTERDAY}*" ! -name "*${DAY_BEFORE_YESTERDAY}*" -exec rm -f {} \;

find "$TARGET_DIR" -type f -name "chim_nest-FINLAND6-forecast_*_72_sem.nc" ! -name "*${TODAY}*" ! -name "*${YESTERDAY}*" ! -name "*${DAY_BEFORE_YESTERDAY}*" -exec rm -f {} \;



echo "Clean run complete. files were deleted."
