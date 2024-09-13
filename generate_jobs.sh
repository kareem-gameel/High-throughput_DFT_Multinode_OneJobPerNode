#!/bin/bash

# Directory containing subdirectories
parent_dir="molecule_subdirectories"

# Loop over all subdirectories inside the parent directory
for subdir in "$parent_dir"/subdir_*; do
    if [ -d "$subdir" ]; then
        # Get the subdirectory number (e.g., 001 from subdir_001)
        subdir_number=$(basename "$subdir" | cut -d'_' -f2)

        # Generate job.sh inside each subdir
        sed "s/JOBID/$subdir_number/g" job_template.sh > "$subdir/job.sh"
        
        # Copy the run_psi4.py script to each subdir
        cp run_psi4.py "$subdir/"
    fi
done
