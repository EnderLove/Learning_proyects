import os
import pandas as pd

def rename_files(source_folder, mapping_file):
    
    mapping_df = pd.read_excel(mapping_file)
    
    current_names = mapping_df.iloc[:, 6].tolist()  
    new_names = mapping_df.iloc[:, 1].tolist() 
   
    files_in_folder = [f for f in os.listdir(source_folder) if f.endswith('.xlsx')]
    
    for i in enumerate(current_names):
        for j in enumerate(files_in_folder):
            if files_in_folder[i] == current_names[j]:
                print("I find it!!")
            else: pass

source_folder = 'D:/kardex_temp'
mapping_file = 'D:/ARTICULOS.xlsx' 

rename_files(source_folder, mapping_file)

