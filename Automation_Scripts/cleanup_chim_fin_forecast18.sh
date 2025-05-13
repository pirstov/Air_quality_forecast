#!/bin/bash







# Set the directory containing the forecast files



TARGET_DIR="/scratch/project_2012160/CHIMERE/chimere_forecast/nest-FINLAND18-forecast"

TARGET_DIR2="/projappl/project_2012160/CHIMERE"
find "$TARGET_DIR2" -type f -name "time_*.txt" ! -name "*${TODAY}.txt" ! -name "*${YESTERDAY}.txt" -exec rm -f {} \;






# Get the dates for today, yesterday, and two days ago in YYYYMMDD format



TODAY=$(date +"%Y%m%d")



YESTERDAY=$(date -d "yesterday" +"%Y%m%d")



DAY_BEFORE_YESTERDAY=$(date -d "2 days ago" +"%Y%m%d")


THREE_DAYS_AGO=$(date -d "3 days ago" +%Y%m%d)




# Find and list files that would be deleted (without deleting them)



echo "Files that would be deleted:"







# List files for chim_nest-FINLAND18-forecast_*_72_out.nc



find "$TARGET_DIR" -type f   -name "chim_nest-FINLAND18-forecast_*_72_out.nc"   ! -name "*${TODAY}*"   ! -name "*${YESTERDAY}*"   ! -name "*${DAY_BEFORE_YESTERDAY}*" ! -name "*${THREE_DAYS_AGO}*"  -exec rm -f {} \;






# List files for chim_nest-FINLAND18-forecast_*_72_dem.nc



find "$TARGET_DIR" -type f   -name "chim_nest-FINLAND18-forecast_*_72_dem.nc"   ! -name "*${TODAY}*"   ! -name "*${YESTERDAY}*"   ! -name "*${DAY_BEFORE_YESTERDAY}*"   -exec rm -f {} \;







# List files for chim_nest-FINLAND18-forecast_*_72_bem.nc



find "$TARGET_DIR" -type f   -name "chim_nest-FINLAND18-forecast_*_72_bem.nc"   ! -name "*${TODAY}*"   ! -name "*${YESTERDAY}*"   ! -name "*${DAY_BEFORE_YESTERDAY}*"   -exec rm -f {} \;







# List files for chim_nest-FINLAND18-forecast_*_72_aem.nc



find "$TARGET_DIR" -type f   -name "chim_nest-FINLAND18-forecast_*_72_aem.nc"   ! -name "*${TODAY}*"   ! -name "*${YESTERDAY}*"   ! -name "*${DAY_BEFORE_YESTERDAY}*"   -exec rm -f {} \;



# List files for wrfout_d01_* (no _72_ added)



find "$TARGET_DIR" -type f   -name "wrfout_d01_*_00:00:00"   ! -name "*${TODAY}*"   ! -name "*${YESTERDAY}*"   ! -name "*${DAY_BEFORE_YESTERDAY}*" -name "*${THREE_DAYS_AGO}*" -exec rm -f {} \;


find "$TARGET_DIR" -type f -name "chim_nest-FINLAND18-forecast_*_72_sem.nc" ! -name "*${TODAY}*" ! -name "*${YESTERDAY}*" ! -name "*${DAY_BEFORE_YESTERDAY}*" -exec rm -f {} \;

find "$TARGET_DIR" -type f -name "chim_nest-FINLAND18-forecast_*_72_start.nc" ! -name "*${TODAY}*" ! -name "*${YESTERDAY}*" ! -name "*${DAY_BEFORE_YESTERDAY}*" -exec rm -f {} \;

find "$TARGET_DIR" -type f -name "end.*_72_nest-FINLAND18-forecast.nc" ! -name "*${TODAY}*" ! -name "*${YESTERDAY}*" ! -name "*${DAY_BEFORE_YESTERDAY}*" -exec rm -f {} \;

find "$TARGET_DIR" -type f -name "wrfrst_d01_*_00:00:00" ! -name "*${TODAY}*" ! -name "*${YESTERDAY}*" ! -name "*${DAY_BEFORE_YESTERDAY}*" ! -name "*${THREE_DAYS_AGO}*" -exec rm -f {} \;




echo "Clean run complete. Files were deleted."


