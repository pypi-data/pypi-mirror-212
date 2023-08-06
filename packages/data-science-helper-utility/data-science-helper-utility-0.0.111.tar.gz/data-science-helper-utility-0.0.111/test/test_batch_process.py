from data_science_helper import helper_batch_process as hbp
import pandas as pd

###############################################
############### PRUEBA TO CSV   ############### 
###############################################

############### PRUEBA STATA ############### 
file_input = ""
folder_output = ""

# stata_to_csv(file_input, folder_output, 100000)

############### PRUEBA EXCEL ############### 

file_input = ""
folder_output = ""
hbp.excel_to_csv(file_input, folder_output)


############### PRUEBA CSV TXT ############### 
file_input = ""
folder_output = ""

hbp.csv_to_csv(file_input, folder_output, 10000, encoding='latin1')




###############################################
############### PRUEBA ENCODING ############### 
###############################################


pathOrigin = "C:/Users/GNC/Desktop/OSOSEE/Scripts/data/inputencoding"
pathDestin = "C:/Users/GNC/Desktop/OSOSEE/Scripts/data/outoutencoding"

# ==============================================================================
# codigo para lectura de MULTIPLES ARCHIVOS
# ==============================================================================
# hbp.transformar(pathOrigin, pathDestin,  "N_DOC", ['NOMBRES','APELLIDO_PATERNO','APELLIDO_MATERNO'], ',' , chunksize=10000)

data = pd.read_csv("Data/Output/Sample_cifrado_18102022.csv", sep='|')

#datat = hbp.transformar(df2, pathDestin,  "COD_MOD", ['NOMBRES','APELLIDO_PATERNO','APELLIDO_MATERNO'], ',' , chunksize=10000)


pathOrigin = "D:/GNC/Noviembre/encodingData/data/input2"
pathDestin = "D:/GNC/Noviembre/encodingData/data/output"


datat = hbp.transformar(pathOrigin, pathDestin,  "dni", ["Region", "Rep", "Item"], ',' , chunksize=1000000)

datat = hbp.transformar(pathOrigin, pathDestin,  "dni", ['dpto', 'SECUENCIA', 'prov'], ',' , chunksize=1000000)
