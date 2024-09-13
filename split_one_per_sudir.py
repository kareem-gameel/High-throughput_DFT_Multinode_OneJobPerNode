import os

def split_xyz_file(input_file, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Read all molecules from the input file
    with open(input_file, 'r') as file:
        molecules = []
        current_molecule = []
        while True:
            num_atoms_line = file.readline().strip()
            if not num_atoms_line:
                break
            mol_id_line = file.readline().strip()
            coordinates = [file.readline().strip() for _ in range(int(num_atoms_line))]
            current_molecule = (num_atoms_line, mol_id_line, coordinates)
            molecules.append(current_molecule)

    # Create 800 subdirectories, each for one molecule
    for i, (num_atoms, mol_id, coords) in enumerate(molecules):
        subdir = os.path.join(output_dir, f'subdir_{i+1:03d}')
        os.makedirs(subdir, exist_ok=True)
        output_file_path = os.path.join(subdir, f'molecule_{i+1:03d}.xyz')
        with open(output_file_path, 'w') as output_file:
            output_file.write(f"{num_atoms}\n")
            output_file.write(f"{mol_id}\n")
            for line in coords:
                output_file.write(f"{line}\n")

    print(f"Split {len(molecules)} molecules into {len(molecules)} subdirectories.")

# Example usage
input_file = 'tmqm_co_remainder_xtb_vtight.xyz'  # Your input file
output_dir = 'molecule_subdirectories'  # Directory to save the subdirectories
split_xyz_file(input_file, output_dir)
