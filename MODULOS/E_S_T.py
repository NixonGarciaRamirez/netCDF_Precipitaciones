import glob
import os
import numpy as np
import pandas as pd
from netCDF4 import Dataset, num2date
from collections.abc import Iterable
import netCDF4 as nc


def extraccion_1(directorio= '../netCDF/*.nc', directorio_raiz = '../netCDF', latt =  6.646697 , lonn = -75.460673):
    # *! identidicador de fechas automatico
    all_year = []# **con esto pordemo ver si glob esta leyendo y uniendo dentro de data todos los netCDF

    for i in glob.glob(directorio):

        data = Dataset(i, 'r') 
        time = data.variables['time']
        unidades = time.units
        calendario = time.calendar
        first_date = nc.num2date(time[0], units=unidades, calendar=calendario)
        first_year = first_date.year
        all_year.append(first_year)
        
    #print(all_year)
    
    

    # *! Cambio de nombres automaticos
    # Directorio que deseas explorar
    directorio = directorio_raiz  # Reemplaza con la ruta adecuada

    # Obtén una lista de nombres de archivos en el directorio
    Nombres_originales = os.listdir(directorio)

    # Itera a través de los nombres de archivos originales y los años
    for nombre_original, año in zip(Nombres_originales, all_year):
        # Construye el nuevo nombre del archivo con el año
        nombre_nuevo = f'{año}.nc'

        # Rutas de archivo original y nuevo
        ruta_original = os.path.join(directorio, nombre_original)
        ruta_nueva = os.path.join(directorio, nombre_nuevo)

        # Renombra el archivo
        os.rename(ruta_original, ruta_nueva)

       
            
    # *! este es el mejor metodo para generar las fechas necesarios dentro del DF
    time_variable = data['time']

    # Obtiene los valores de fecha y hora
    dates = nc.num2date(time_variable[:], units=time_variable.units, calendar=time_variable.calendar)

    # ** Imprime TODAS las fechas del netCDF
    for date in dates:
        print(date)
        
    # *! Creacion de un DF vacio
    df = pd.DataFrame(0.0 , columns= ['Precipitacion'], index = dates )



    # ** ahora debemos definir la lat y lon de interes
    lat_S =  latt
    lon_S = lonn

    all_year.sort(reverse= False)
    for i in all_year:
        data = Dataset('../netCDF/'+str(i)+'.nc', 'r')
        lat = data.variables['lat'][:]
        lon = data.variables['lon'][:]

        lat_V = (lat - lat_S)**2
        lon_V = (lon - lon_S)**2

        min_lat = lat_V.argmin()
        min_lon = lon_V.argmin()
        
        prec = data.variables['pr']
        
        # ** aqui vamos a exrtaer la fecha de inicio y la de fin
        time_variable = data['time']
        # Obtiene las unidades de tiempo y el calendario
        time_variable = data['time']
        dates = nc.num2date(time_variable[:], units=time_variable.units, calendar=time_variable.calendar)
            
        for x in np.arange(0, len(dates)):
            df.loc[dates[x]]['Precipitacion'] = prec[x, min_lat , min_lon]
            
        print("Se ejecuto de forma exitosa")

    df.to_csv('../CSV_OUT/generales/santarosa_P.csv')
    

        


def multiple_extraccion(directorio= '../netCDF/*.nc', directorio_raiz = '../netCDF', ubixaciones = '../XLSM/UBICACIONES.csv'):
    # *! identidicador de fechas automatico
    all_year = []# **con esto pordemo ver si glob esta leyendo y uniendo dentro de data todos los netCDF

    for i in glob.glob(directorio):

        data = Dataset(i, 'r') 
        time = data.variables['time']
        unidades = time.units
        calendario = time.calendar
        first_date = nc.num2date(time[0], units=unidades, calendar=calendario)
        first_year = first_date.year
        all_year.append(first_year)
        
    #print(all_year)
    
    

    # *! Cambio de nombres automaticos
    # Directorio que deseas explorar
    directorio = directorio_raiz  # Reemplaza con la ruta adecuada

    # Obtén una lista de nombres de archivos en el directorio
    Nombres_originales = os.listdir(directorio)

    # Itera a través de los nombres de archivos originales y los años
    for nombre_original, año in zip(Nombres_originales, all_year):
        # Construye el nuevo nombre del archivo con el año
        nombre_nuevo = f'{año}.nc'

        # Rutas de archivo original y nuevo
        ruta_original = os.path.join(directorio, nombre_original)
        ruta_nueva = os.path.join(directorio, nombre_nuevo)

        # Renombra el archivo
        os.rename(ruta_original, ruta_nueva)

            
            
    # *! este es el mejor metodo para generar las fechas necesarios dentro del DF
    time_variable = data['time']

    # Obtiene los valores de fecha y hora
    dates = nc.num2date(time_variable[:], units=time_variable.units, calendar=time_variable.calendar)

    # ** Imprime TODAS las fechas del netCDF
    '''for date in dates:
        print(date)'''
        
    # *! Creacion de un DF vacio
    df = pd.DataFrame(0.0 , columns= ['Precipitacion'], index = dates )



    # ** ahora debemos definir el lugar, lat y lon de los distintos puntos de interes mediante un csv

    locations = pd.read_csv(ubixaciones)
    for index, row in locations.iterrows():
        lugar = row['nombre']
        latitud = row['lat']
        longotud = row['lon']
  
        all_year.sort(reverse= False)
        
        for i in all_year:
            data = Dataset('../netCDF/'+str(i)+'.nc', 'r')
            lat = data.variables['lat'][:]
            lon = data.variables['lon'][:]

            lat_V = (lat - latitud)**2
            lon_V = (lon - longotud)**2

            min_lat = lat_V.argmin()
            min_lon = lon_V.argmin()
            
            prec = data.variables['pr']
            
            # ** aqui vamos a exrtaer la fecha de inicio y la de fin
            time_variable = data['time']
            # Obtiene las unidades de tiempo y el calendario
            time_variable = data['time']
            dates = nc.num2date(time_variable[:], units=time_variable.units, calendar=time_variable.calendar)
                
            for x in np.arange(0, len(dates)):
                df.loc[dates[x]]['Precipitacion'] = prec[x, min_lat , min_lon]

        df.to_csv(f'../CSV_OUT/lugares/{lugar}.csv')

            

# *! Combinacion de las distintas precipitacion en las distitnas ubicaciones seleccionadas anteriormente , este se usa en conjunto con la funcion multiple_extraccion
def Combinacion_df(csv_directory = '../CSV_OUT/lugares'):
  
    csv_files = os.listdir(csv_directory)

    combined_df = pd.DataFrame()


    for csv_file in csv_files:
        csv_path = os.path.join(csv_directory, csv_file)
        df = pd.read_csv(csv_path)
        combined_df = pd.concat([combined_df, df], ignore_index=False)

    combined_df.columns = ['Fecha', 'Precipitacion']

    combined_df.to_csv('../CSV_OUT/generales/1.csv')

    df1 = pd.read_csv('../CSV_OUT/generales/1.csv')
    df1.columns = ['xxxx','Fecha', 'Precipitacion']
    df1 = df1.drop(columns=['xxxx'])
    df2 = df1.groupby('Fecha').mean()
    df2.to_csv('../CSV_OUT/precipitacion_antioquia.csv')
    df2