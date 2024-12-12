import os
import pandas as pd

#source_folder = "D:/backup_kardex"
mapping_file = "D:/ARTICULOS.xlsx"

mapping_df = pd.read_excel(mapping_file)

current_names = mapping_df.iloc[:, 6].tolist()
print(type (current_names[0]))

#files_in_folder = [f for f in os.listdir(source_folder) if f.endswith('.xlsx')]
#print (files_in_folder)

