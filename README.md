
# High-throughput DFT Parallelization: One Job per Node

This repository contains scripts designed for running high-throughput DFT calculations on the Niagara cluster using multiple nodes with one job per node.

## Overview
The pipeline provided in this repository is designed to handle large-scale DFT calculations by parallelizing the process across multiple nodes, where each node runs a single job. This setup ensures efficient use of computational resources for extensive quantum chemistry calculations, particularly for Psi4-based workflows.

## Files in the Repository

1. **job_template.sh**:
   - This SLURM job template is set up to run a single task (DFT calculation) per node, with 40 CPUs allocated per task.
   - It includes the creation of a temporary directory for Psi4 scratch files and runs the Psi4 calculation using the `run_psi4.py` script for the provided XYZ files.

2. **run_psi4.py**:
   - A Python script that reads an XYZ file, generates the Psi4 input file, and runs the DFT calculation using Psi4.
   - After the calculation, it extracts the total energy and calculation time from the Psi4 output, logs the results, and optionally cleans up intermediate files.
   
3. **generate_jobs.sh**:
   - Generates individual job scripts (`job.sh`) inside each subdirectory in the `molecule_subdirectories` folder.
   - Replaces placeholders in `job_template.sh` with appropriate directory and file names.

4. **submit_jobs.sh**:
   - A submission script that loops through the `molecule_subdirectories` directory and submits jobs for all available subdirectories from `subdir_002` to `subdir_800`.

## How to Use the Repository

1. **Set Up the Molecule Subdirectories**:
   - Each molecule should have its own subdirectory within `molecule_subdirectories`, with an XYZ file named `molecule_XXX.xyz` where `XXX` is the molecule number.

2. **Generate Job Scripts**:
   - Run `generate_jobs.sh` to generate job scripts for each subdirectory. This script will copy `run_psi4.py` to each subdirectory and create the corresponding `job.sh` file.

3. **Submit Jobs**:
   - Use `submit_jobs.sh` to submit all the jobs in the `molecule_subdirectories`. The script will look for `job.sh` files in each subdirectory and submit them to the Niagara cluster using `sbatch`.

4. **Temporary Directories**:
   - Each job creates a temporary directory to store Psi4's scratch files. The directory is cleaned up after the job completes. This is crucial for efficient parallelization as Psi4 uses the `PSI_SCRATCH` environment variable to store intermediate data.

## Requirements
- Niagara cluster access.
- Psi4 version 1.5 installed on the cluster.

This setup is ideal for large-scale DFT computations, enabling the efficient distribution of computational load across multiple nodes.
