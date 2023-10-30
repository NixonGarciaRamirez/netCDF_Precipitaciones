import glob
import os
import numpy as np
import pandas as pd
from netCDF4 import Dataset, num2date
from collections.abc import Iterable
import netCDF4 as nc

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

        df.to_csv(f'../CSV_OUT/{lugar}.csv')

            


