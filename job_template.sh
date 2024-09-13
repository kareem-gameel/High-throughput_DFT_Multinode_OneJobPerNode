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
gameelka@nia-login01:/scratch/o/ovoznyy/gameelka/psi4_remainder$ cat job_template.sh 
#!/bin/bash

# SLURM submission script for a single serial job on Niagara
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1  # 1 task for 1 file
#SBATCH --cpus-per-task=40    # Each task uses 40 CPUs
#SBATCH --time=5:00:00       # Set a time limit for debugging
#SBATCH --job-name=subdir_JOBID
#SBATCH --output=job_output_%j.txt
#SBATCH --error=job_error_%j.txt

# Load the required modules
module load CCEnv
module load StdEnv/2020
module load intel/2020
module load openmpi
module load psi4/1.5

# Set up a temporary directory for Psi4 scratch files
tmpdir="${SLURM_SUBMIT_DIR}/tmp"
mkdir -p "$tmpdir"

# Replace 'JOBID' with the actual subdir number when generating the script
xyz_file="molecule_JOBID.xyz"

if [ -d "$tmpdir" ]; then
    export PSI_SCRATCH="$tmpdir"

    # Check if the XYZ file exists and run Psi4 for the file
    if [ -f "$xyz_file" ]; then
        echo "Running Psi4 for $xyz_file"
        python run_psi4.py "$xyz_file"
    else
        echo "XYZ file $xyz_file not found in the directory" >&2
        exit 1
    fi
else
    echo "Failed to create directory $tmpdir" >&2
    exit 1
fi

# Clean up the temporary directory after the job is done
rm -rf "$tmpdir"
