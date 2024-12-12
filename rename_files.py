import os
import pandas as pd

# Function to rename files based on a mapping
def rename_files(source_folder, mapping_file):
    
    mapping_df = pd.read_excel(mapping_file)
    
    current_names = mapping_df.iloc[:, 6].tolist()  # Original names (column 6)
    new_names = mapping_df.iloc[:, 1].tolist()  # New names (column 1)
   
    files_in_folder = [f for f in os.listdir(source_folder) if f.endswith('.xlsx')]
    
    # Step 3: Loop through all files in the folder and rename them based on the mapping
    for file_name in files_in_folder:
        for i, current_name in enumerate(current_names):
            # Log the current_name and its type to understand why it's not being recognized as a string
            if not isinstance(current_name, str):
                print(f"Non-string value found at index {i}: {current_name} (Type: {type(current_name)})")

            # Ensure current_name is a string before using .strip()
            if isinstance(current_name, str) and current_name.strip() == file_name.strip():
                old_path = os.path.join(source_folder, file_name)
                new_path = os.path.join(source_folder, new_names[i])
                
                # Rename the file if the names match
                try:
                    os.rename(old_path, new_path)
                    print(f"Renamed: {file_name} -> {new_names[i]}")
                except Exception as e:
                    print(f"Error renaming {file_name}: {e}")

source_folder = 'D:/kardex_temp'
mapping_file = 'D:/ARTICULOS.xlsx' 

rename_files(source_folder, mapping_file)

