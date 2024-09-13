#!/bin/bash

# Change to the molecule_subdirectories directory where all subdirectories are located
cd molecule_subdirectories || { echo "molecule_subdirectories not found, exiting."; exit 1; }

# Loop through subdirectories from subdir_002 to subdir_800
for i in $(seq -w 002 800)
do
    dir_name="subdir_$i"
    if [ -d "$dir_name" ]; then  # Check if it's a directory
        cd "$dir_name"
        if [ -f "job.sh" ]; then  # Check if job.sh exists in the directory
            echo "Submitting job in $dir_name"
            sbatch job.sh
        else
            echo "No job.sh found in $dir_name, skipping..."
        fi
        cd ..
    else
        echo "$dir_name does not exist, skipping..."
    fi
done
