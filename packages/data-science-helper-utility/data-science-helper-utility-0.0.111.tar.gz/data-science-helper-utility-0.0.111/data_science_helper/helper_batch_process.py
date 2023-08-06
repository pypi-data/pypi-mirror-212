import pandas as pd
import numpy as np
import csv
import os

import hashlib
import csv

def find_delimiter(filename):
    sniffer = csv.Sniffer()
    with open(filename) as fp:
        delimiter = sniffer.sniff(fp.read(5000)).delimiter
    return delimiter
    

# Para futuras versiones
def spss_to_csv(file_input, folder_output):
    DATA = file_input
    return DATA


def stata_to_csv(file_input, folder_output, chunksize = 100000, columns = []):
    # definiendo rutas de salida
    fileName = os.path.basename(file_input)
    fileBaseName, fileExt = os.path.splitext(fileName)
    fileOutName = os.path.join(folder_output, 'out_' + fileBaseName + '.csv')
    fileOutLabels = os.path.join(folder_output, 'out_' + fileBaseName + '_LABELS.xlsx')
    
    encoding = "utf-8-sig"
    separator = "|"
    
    if os.path.exists(fileOutName):
        os.remove(fileOutName)

    if os.path.exists(fileOutLabels):
        os.remove(fileOutLabels)

    
    if fileExt.lower() == '.dta':
        # 1: Cargando datos por chunks - generando el iterador
        
        data_chunks = pd.read_stata(file_input,
                                    chunksize = chunksize,
                                    convert_categoricals = False,
                                    iterator=True)
        
        var_labels = pd.DataFrame( data_chunks.variable_labels().items() )
        val_labels = pd.DataFrame( data_chunks.value_labels().items() )
        dat_label = pd.DataFrame( data= [data_chunks.data_label] )
        # Diccionario Descripcion 
        with pd.ExcelWriter( fileOutLabels ) as writer:
            dat_label.to_excel(writer, sheet_name='DATA LABEL')
            var_labels.to_excel(writer, sheet_name='VARIABLE LABELS')
            val_labels.to_excel(writer, sheet_name='VALUE LABELS')
        
        count = 0
        for data in data_chunks:
            
            count += 1
            print(f"Chunk N° {count} - {data.shape}")
            
            # 2 Removiendo los palotes si existen en la data
            ncols = data.shape[1]
            for idx in range( ncols ):
                data.iloc[:,idx] = data.iloc[:,idx].astype('str').replace('nan',np.nan).replace("NaT", np.nan).replace("|","*")
            
            # 3 FILTRANDO LAS COLUMNAS REQUERIDAS
            if columns !=[]:
                common_cols = data.columns.intersection(columns)
                data = data[common_cols].copy()
            
            # 4 Escribir Data
            if count > 1:
                header = False
            else:
                header = True
            data.to_csv(fileOutName,
                        header = header,
                        sep = separator,
                        encoding = encoding,
                        index = False,
                        mode = 'a')                        
    return fileOutName



def excel_to_csv(file_input, folder_output, columns = []):
    
    # definiendo rutas de salida
    fileName = os.path.basename(file_input)
    fileBaseName, fileExt = os.path.splitext(fileName)
    fileOutName = os.path.join(folder_output, 'out_' + fileBaseName + '.csv')
    encoding = "utf-8-sig"
    separator = "|"
    
    if fileExt.lower() in ['.xlsx', '.xls', '.xlsb'] :
        # 1: Cargando datos por chunks - generando el iterador
        # agregar la extension con el ENGINE para otros formatos
        dict_engine = {'.xlsb' : 'pyxlsb',
                       '.xlsx' : 'openpyxl',
                       '.xls'  : 'xlrd'}

        engine = dict_engine.get(fileExt.lower())
        
        
        xls = pd.ExcelFile(file_input, 
                           engine = engine)
        sheets = xls.sheet_names
        print(sheets)

        count = 0
        for sheet in sheets:
            fileOutName = os.path.join(folder_output, 'out_' + fileBaseName + f'__{sheet}.csv')
            # Eliminar Archivo Existente                
            if os.path.exists(fileOutName):
                os.remove(fileOutName)


            data = pd.read_excel(file_input, 
                                 dtype = str,
                                 sheet_name=sheet,
                                 engine = engine)
            count += 1
            print(f"Sheet N° {count} - {data.shape}")
            
            # 2 Removiendo los palotes si existen en la data
            ncols = data.shape[1]
            for idx in range( ncols ):
                data.iloc[:,idx] = data.iloc[:,idx].replace("|","*")

            # 3 FILTRANDO LAS COLUMNAS REQUERIDAS
            if columns !=[]:
                common_cols = data.columns.intersection(columns)
                data = data[common_cols].copy()
            
            # 4 Escribir Data
            if count > 1:
                header = False
            else:
                header = True
            data.to_csv(fileOutName,
                        header = header,
                        sep = separator,
                        encoding = encoding,
                        index = False,
                        mode = 'a')                        
    else:
        print(f"Error, extension no permitida ({fileExt})")

    return fileOutName



def csv_to_csv(file_input, folder_output, chunksize = 100000, columns = [], **kwargs):
    # definiendo rutas de salida
    fileName = os.path.basename(file_input)
    fileBaseName, fileExt = os.path.splitext(fileName)
    fileOutName = os.path.join(folder_output, 'out_' + fileBaseName + '.csv')
    out_encoding = "utf-8-sig"
    separator = "|"

    in_separator = find_delimiter(file_input)
    print(f"SEPARADOR : {in_separator }")
    
    
    if fileExt.lower() in ['.csv', '.txt'] :
        # 1 Carga Data por CHUNKS
        count = 0
        
        for data in pd.read_csv(file_input,
                                sep = in_separator,
                                dtype = str,
                                chunksize = chunksize,
                                **kwargs):
            count += 1
            print(f"Chunk N° {count} - {data.shape}")

            # 2 Removiendo los palotes si existen en la data
            ncols = data.shape[1]
            for idx in range( ncols ):
                data.iloc[:,idx] = data.iloc[:,idx].replace("|","*")

            # 3 FILTRANDO LAS COLUMNAS REQUERIDAS
            if columns !=[]:
                common_cols = data.columns.intersection(columns)
                data = data[common_cols].copy()
            
            # 4 Escribir Data
            if count > 1:
                header = False
            else:
                header = True
            data.to_csv(fileOutName,
                        header = header,
                        sep = separator,
                        encoding = out_encoding,
                        index = False,
                        mode = 'a')                        
    else:
        print(f"Error, extension no permitida ({fileExt})")

    return fileOutName







# FUNCION
def transformar(urlIn, urlOut, columnId, columnsMask, chunksize = 100000):
    
    # Listado de archivos que acepta la funcion
    tipo_archivos = ['.txt', '.csv', '.dta', '.xlsx', '.xls']
    
    # Tabla vacia de encripcion
    encryption_table = pd.DataFrame(data = None,
                                    columns = [columnId, 'new_id'],
                                    dtype = str)
    
    # urlIn : ruta especifica
    if isinstance(urlIn, str):
        listFiles = os.listdir(urlIn)
        filesIn = listFiles
        # filesIn = [file for file in listFiles if ".csv" in file.lower()]

        # Iterando archivos
        for fileName in filesIn:
            fileExt = os.path.splitext(fileName)[1].lower()
            
            # Verificando que el tipo de archivo se encuentre en la lista
            if fileExt in tipo_archivos:

                filePath = os.path.join(urlIn, fileName) # INPUT PATH
                fileOut = "Out_" + str(fileName)         # OUTPUT FILE NAME
                pathOut = os.path.join(urlOut, fileOut)  # OUTPUT PATH

                # Eliminar archivo si existe
                if os.path.exists(pathOut):
                    os.remove(pathOut)

                print(pathOut, fileOut)
                count = 0


                if fileExt in ['.csv', '.txt'] :
                    
                    separator = find_delimiter(filePath)
                    print(f"SEPARADOR : {separator }")

                    
                    # 1 Carga Data por CHUNKS
                    for data in pd.read_csv(filePath,
                                            sep=separator,
                                            dtype=str,
                                            chunksize=chunksize):
                        count += 1
                        print(f"Chunk N° {count}", data.shape)

                        # 2 Obtener los ID de las tablas
                        temp = data[columnId].drop_duplicates().copy()
                        temp = pd.merge(temp, encryption_table, on=columnId,
                                        how='left').copy()
                        temp = temp[temp['new_id'].isna()].copy() # keep NAN values
        
                        last_id = encryption_table.shape[0] # ultimo elemento  numeracion
                        num_new_rows = temp.shape[0]
                        temp['new_id'] = range(last_id + 1, last_id + num_new_rows + 1)
        
                        # 3 Agregando al diccionario principal
                        encryption_table = encryption_table.append(temp, ignore_index=True)
        
                        # 4 Cruzamos con la tabla
                        data = pd.merge(data, encryption_table, on=columnId, how='left').copy()
                        data[columnId] =  data['new_id']  # copiando los nuevos ID en COLUMNID
        
                        # 5 Eliminando new_id de la tabla
                        data.drop('new_id', axis=1, inplace=True)
        
                        # 6 Enmascarando las columnas COLUMNMASK
                        for col in columnsMask:
                            if col in data.columns:
                                data[col] = '*'
                        
                        # 7 Escribir Data
                        if count > 1:
                            header = False
                        else:
                            header = True
                        data.to_csv(pathOut, header=header, sep=separator, index=False, mode='a')
                
                elif fileExt == '.dta':
                    # Cambiando de nombre al archivo
                    pathOut = os.path.splitext(pathOut)[0] + '.csv'
                    
                    # 1 Carga Data por CHUNKS
                    for data in pd.read_stata(filePath,
                                              chunksize = chunksize,
                                              convert_categoricals = False ):
                        count += 1
                        print(f"Chunk N° {count}", data.shape)

                        # 2 Obtener los ID de las tablas
                        temp = data[columnId].drop_duplicates().copy()
                        temp = pd.merge(temp, encryption_table, on=columnId,
                                        how='left').copy()
                        temp = temp[temp['new_id'].isna()].copy() # keep NAN values
        
                        last_id = encryption_table.shape[0] # ultimo elemento  numeracion
                        num_new_rows = temp.shape[0]
                        temp['new_id'] = range(last_id + 1, last_id + num_new_rows + 1)
        
                        # 3 Agregando al diccionario principal
                        encryption_table = encryption_table.append(temp, ignore_index=True)
        
                        # 4 Cruzamos con la tabla
                        data = pd.merge(data, encryption_table, on=columnId, how='left').copy()
                        data[columnId] =  data['new_id']  # copiando los nuevos ID en COLUMNID
        
                        # 5 Eliminando new_id de la tabla
                        data.drop('new_id', axis=1, inplace=True)
        
                        # 6 Enmascarando las columnas COLUMNMASK
                        for col in columnsMask:
                            if col in data.columns:
                                data[col] = '*'
                        
                        # 7 Escribir Data
                        if count > 1:
                            header = False
                        else:
                            header = True
                        
                        
                        data.to_csv(pathOut, 
                                    header = header, 
                                    sep = separator,
                                    index = False,
                                    mode = 'a')
                        
                elif fileExt in ['.xlsx', '.xls']:
                    # Cambiando de nombre al archivo
                    pathOut = os.path.splitext(pathOut)[0] + '.csv'
                    
                    
                    data = pd.read_excel(filePath, dtype = str)
                    
                    print(f"Chunk N° {count}", data.shape)
                    
                    # 2 Obtener los ID de las tablas
                    temp = data[columnId].drop_duplicates().copy()
                    temp = pd.merge(temp, encryption_table, 
                                    on=columnId,
                                    how='left').copy()
                    temp = temp[temp['new_id'].isna()].copy() # keep NAN values
                    
                    last_id = encryption_table.shape[0] # ultimo elemento  numeracion
                    num_new_rows = temp.shape[0]
                    temp['new_id'] = range(last_id + 1, last_id + num_new_rows + 1)
                    
                    # 3 Agregando al diccionario principal
                    encryption_table = encryption_table.append(temp, ignore_index=True)
                    
                    # 4 Cruzamos con la tabla
                    data = pd.merge(data, encryption_table, on=columnId, how='left').copy()
                    data[columnId] =  data['new_id']  # copiando los nuevos ID en COLUMNID
        
                    # 5 Eliminando new_id de la tabla
                    data.drop('new_id', axis=1, inplace=True)
        
                    # 6 Enmascarando las columnas COLUMNMASK
                    for col in columnsMask:
                        if col in data.columns:
                            data[col] = '*'
                        
                    # 7 Escribir Data
                    if count > 1:
                        header = False
                    else:
                        header = True
                        
                        
                    data.to_csv(pathOut, 
                                header = header, 
                                sep = separator,
                                index = False,
                                mode = 'a')
                else:
                    print("ERROR")
                    
            else:
                print(f" --> El Archivo {fileName} no es un formato valido")
        
        return urlOut


    # urlIn : Data Frame    
    elif isinstance(urlIn, pd.core.frame.DataFrame):
        
        data = urlIn.copy()
        
        temp = data[columnId].drop_duplicates().copy()
        temp = pd.merge(temp, encryption_table, on=columnId, how='left').copy()
        temp = temp[temp['new_id'].isna()].copy() # keep NAN values
        last_id = encryption_table.shape[0] # ultimo elemento para seguir la numeracion
        num_new_rows = temp.shape[0]
        temp['new_id'] = range(last_id + 1, last_id + num_new_rows + 1)
        # 3 Agregando al diccionario principal
        encryption_table = encryption_table.append(temp, ignore_index=True)

        print(f"Encryption table: {encryption_table.shape}")
        # 4 Cruzamos con la tabla
        data = pd.merge(data, encryption_table, on=columnId, how='left').copy()
        data[columnId] =  data['new_id']  # copiando los nuevos ID en la columna COLUMNID

        # 5 Eliminando new_id de la tabla
        data.drop('new_id', axis=1, inplace=True)
        
        # 6 Enmascarando las columnas COLUMNMASK
        for col in columnsMask:
            if col in data.columns:
                data[col] = '*'
        return data

    else:
        print('Proveer directorio con lista de archivos  "csv" o dataframe')





# FUNCION
def sample_data(urlIn = None, urlOut = None, columnId = None,
                columnsSample = None, nsample =None, dataToSample = None, chunksize = 100000):
    """
    Parameters
    ----------
        urlIn     : [STR] Ruta de entrada
        urlOut    : [STR] Ruta de Salida
        columnId  : [STR] Columna con la que se trackeara las otras bases
        columnsSample : [LIST] Listado de Columnas consideradas para el muestreo
        (debe contener columnId) - Referencia
        nsample   : [INT] Longitud de la muestras
        dataToSample  : [STR] Patron del nombre de archivo del cual se tomara
        el muestreo
        chunksize : [INT] Tamaño del chunk o lote para procesar la data
    -------
    """
    if isinstance(urlIn, str):
        # filtrando los archivos CSV de entrada
        filesIn = [file for file in os.listdir(urlIn) if ".csv" in file.lower()]
        
        # filtrando la base de la cual se tomara el muestreo
        fileSample = [x for x in filesIn if dataToSample.lower() in x.lower()][0]

        # FORMANDO LA DATA DE MUESTRA
        unique_data = pd.DataFrame(data=None, columns=columnsSample, dtype=str)
        filePath = os.path.join(urlIn, fileSample)
        
        # validando el Separador
        separator = find_delimiter(filePath)
        print(f"SEPARADOR : {separator}")

        
        count = 0
        print(f"Realizando el muestreo de la base {fileSample}")
        for data in pd.read_csv(filePath, sep=separator, dtype=str, chunksize=chunksize):
            count += 1
            print(f" * Chunk N° {count}", data.shape)
            newColums = columnsSample + [columnId]
            temp = data[newColums].drop_duplicates().copy()
            unique_data = unique_data.append(temp).copy()
        unique_data = unique_data.drop_duplicates().reset_index(drop=True).copy()
        # Tomando la Muestra
        sample_data = unique_data.sample(n=nsample).reset_index(drop=True)
        sample_data["sample"] = "1"

        sample_data = sample_data[[columnId, "sample"]].drop_duplicates().copy()

        # TOMANDO LA MUESTRA DE LOS ARCHIVOS DE ENTRADA
        for fileName in filesIn:
            filePath = os.path.join(urlIn, fileName) # INPUT PATH
            fileOut = "Sample_" + str(fileName)      # OUTPUT FILE NAME
            pathOut = os.path.join(urlOut, fileOut)  # OUTPUT PATH
            # Remove file if exist
            if os.path.exists(pathOut):
                os.remove(pathOut)
            print(pathOut, fileOut)
            
            # validando el Separador
            separator = find_delimiter(filePath)
            print(f"SEPARADOR : {separator}")


            # 1 Carga Data por CHUNKS
            count = 0
            for data in pd.read_csv(filePath, sep=separator, dtype=str, chunksize=chunksize):
                count += 1
                print(f"Chunk N° {count}", data.shape)
                # 2 Cruzamos con la tabla
                data = pd.merge(data, sample_data, on= columnId, how='left').copy()

                # print( set( data['sample'].values) )
                data.dropna(subset=['sample'], inplace=True)

                # 3 Eliminando sample de la tabla
                data.drop('sample', axis=1, inplace=True)

                # 4 Escribir Data
                if count > 1:
                    header = False
                else:
                    header = True
                data.to_csv(pathOut, header=header, sep=separator, index=False, mode='a')

    elif isinstance(urlIn, pd.core.frame.DataFrame):

        # FORMANDO LA DATA DE MUESTRA
        data = urlIn.copy()
        newColums = columnsSample + [columnId]
        unique_data = data[newColums].drop_duplicates().copy()
        try:
            unique_data = unique_data.drop_duplicates().reset_index(drop=True).copy()
            # Tomando la Muestra
            sample_data = unique_data.sample(n=nsample).reset_index(drop=True)
            sample_data["sample"] = "1"

            sample_data = sample_data[[columnId, "sample"]].drop_duplicates().copy()

        except:
            print("La cantidad de muestras debe ser menor a la poblacion.")

        # TOMANDO LA MUESTRA DE LOS ARCHIVOS DE ENTRADA
        data = pd.merge(data, sample_data, on=columnId, how='left').copy()

        data.dropna(subset=['sample'], inplace=True)

        # 3 Eliminando sample de la tabla
        data.drop('sample', axis=1, inplace=True)

        return data
    else:
        print('Proveer directorio con lista de archivos  "csv" o dataframe')