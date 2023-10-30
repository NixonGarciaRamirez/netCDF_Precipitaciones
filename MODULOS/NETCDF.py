import glob
from netCDF4 import  Dataset
import netCDF4 as nc
import numpy as np
import pandas as pd
import os

# *! identidicador de fechas automatico
all_year = []# **con esto pordemo ver si glob esta leyendo y uniendo dentro de data todos los netCDF

for i in glob.glob('./archivos/*.nc'):

    data = Dataset(i, 'r') 
    time = data.variables['time']
    unidades = time.units
    calendario = time.calendar
    first_date = nc.num2date(time_variable[0], units=unidades, calendar=calendario)
    all_year.append(first_date)

    

# *! Cambio de nombres automaticos
# Directorio que deseas explorar
directorio = './archivos'  # Reemplaza con la ruta adecuada

# Obtén una lista de nombres de archivos en el directorio
Nombres_originales = os.listdir(directorio)

# Itera a través de las fechas y renombra los archivos
for i in Nombres_originales:
    for x in all_year:
        nombre_original = i
        nombre_nuevo = f'{x}.nc'
        ruta_original = os.path.join(directorio, nombre_original)
        ruta_nueva = os.path.join(directorio, nombre_nuevo)
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



# ** ahora debemos definir la lat y lon de interes
lat_S =   6.646697
lon_S = -75.460673

all_year.sort(reverse= False)
for i in all_year:
    data = Dataset('./archivos/'+str(i)+'.nc', 'r')
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

df.to_csv('prescipitacion_asnta_rosa_de_osos.csv')

