import os
import re
import csv
import sys

# Function to parse the XYZ file
def parse_xyz(file_name):
    with open(file_name, 'r') as xyz_file:
        lines = xyz_file.readlines()

    molecules = []
    i = 0
    while i < len(lines):
        num_atoms = int(lines[i].strip())  # Read number of atoms
        mol_id = lines[i + 1].strip()  # Read molecule ID
        coordinates = lines[i + 2:i + 2 + num_atoms]  # Read coordinates
        molecules.append((mol_id, coordinates))
        i += 2 + num_atoms  # Move to the next molecule in the file

    return molecules

# Function to generate Psi4 input files, run calculations, and save results
def run_psi4_for_molecules(molecules, output_file_base_name):
    results_file = f'{output_file_base_name}.out'

    # Open the CSV file for writing and add the header
    with open(results_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['mol_id', 'energy', 'calc_time'])

    # Iterate over each molecule and process it
    for mol_id, coordinates in molecules:
        # Create the Psi4 input file with the same name as the mol_id
        input_file_name = mol_id
        with open(input_file_name, 'w') as psi4_file:
            psi4_file.write(f"memory 100 GB\n\n")
            psi4_file.write(f"molecule {mol_id} {{\n")
            psi4_file.write(f"0 1\n")  # Default charge and multiplicity
            
            for coord in coordinates:
                psi4_file.write(coord)
            
            psi4_file.write(f"}}\n\n")
            psi4_file.write(f"set {{\n")
            psi4_file.write(f"  basis def2-SVPD\n")
            psi4_file.write(f"}}\n\n")
            psi4_file.write(f"energy('wb97mv')\n")

        print(f"Generated Psi4 input file: {input_file_name}")

        # Run Psi4 with the generated input file and 40 threads
        command = f"psi4 {input_file_name} -n 40"
        os.system(command)

        # Read the generated .dat file
        dat_file_name = f"{mol_id}.dat"
        if os.path.exists(dat_file_name):
            with open(dat_file_name, 'r') as dat_file:
                dat_content = dat_file.read()

            # Parse the total energy and total time from the .dat file
            energy_match = re.search(r'Total Energy =\s+([-\d.]+)', dat_content)
            time_match = re.search(r'total time\s+=\s+[\d.]+\sseconds\s+=\s+([\d.]+)\sminutes', dat_content)

            total_energy = float(energy_match.group(1)) if energy_match else None
            total_time_minutes = float(time_match.group(1)) if time_match else None

            # Append the results to the CSV file
            with open(results_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([mol_id, total_energy, total_time_minutes])

            print(f"Results for {mol_id} saved in {results_file}")
        else:
            print(f"Error: The file {dat_file_name} was not found.")

        # Clean up: Remove input and output files for the molecule if desired
        # Uncomment if cleanup is needed
        # os.remove(input_file_name)  # Remove the input file
        # if os.path.exists(dat_file_name):
        #     os.remove(dat_file_name)  # Remove the .dat file

# Main code execution
if len(sys.argv) < 2:
    print("Usage: python run_psi4.py <xyz_file>")
    sys.exit(1)

input_file_name = sys.argv[1]
molecules = parse_xyz(input_file_name)
output_file_base_name = os.path.splitext(input_file_name)[0]

# Run Psi4 calculations for all molecules
run_psi4_for_molecules(molecules, output_file_base_name)
