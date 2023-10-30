
# *! importtamos las librerias necesrias

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap # ** documentacion https://matplotlib.org/basemap/api/basemap_api.html
from netCDF4 import Dataset
import netCDF4 as nc
import numpy as np
import xarray as xr


def imagen_global(netcdf_file = '../netCDF/1990.nc'):
    # Reemplaza 'archivo.nc' con la ruta de tu archivo NetCDF
    data = xr.open_dataset(netcdf_file)

    lons = data.variables['lon'][:]
    lats = data.variables['lat'][:]
    time = data.variables['time'][:]
    preci = data.variables['pr'][:]
   # Crear una instancia de Basemap
    m = Basemap(projection='merc', llcrnrlat=-80, urcrnrlat=80, llcrnrlon=-180, urcrnrlon=400)

    # Crear una figura de Matplotlib
    fig = plt.figure(figsize=(12, 9))

    # Dibuja líneas de la costa y fronteras políticas
    m.drawcoastlines()
    m.drawcountries()
    lon , lat = np.meshgrid(lons,lats)
    x,y = m(lon, lat)
    C_scale = m.pcolor(x,y,np.squeeze(preci[3, : , :]), cmap = 'jet' )
    c_bar = m.colorbar(C_scale , location= 'right', pad = '10%' )

    # Dibujar meridianos y paralelos
    m.drawmeridians(range(-180, 200, 60), labels=[0, 0, 0, 1])
    m.drawparallels(range(-90, 91, 30), labels=[1, 0, 0, 0])

    # Mostrar el mapa
    plt.title("Mapa Base con Basemap")
    plt.show()

def extraccion_region(netcdf_file = '../netCDF/1990.nc',lat_min = 4, lat_max= 10, lon_min = 282 , lon_max = 287 , n = 3 ):
    
    # Reemplaza 'archivo.nc' con la ruta de tu archivo NetCDF
    dataset = xr.open_dataset(netcdf_file)

    # Recorta la región de interés
    subset = dataset.sel(lat=slice(lat_min, lat_max), lon=slice(lon_min, lon_max))
    xr.Dataset.to_netcdf(subset , '../NC_OUT/extraccion.nc')

    # Crear una instancia de Basemap
    lons = subset.variables['lon'][:]
    lats = subset.variables['lat'][:]
    time = subset.variables['time'][:]
    preci = subset.variables['pr'][:]

    m = Basemap(projection='merc', llcrnrlat= lat_min , urcrnrlat=lat_max, llcrnrlon= lon_min, urcrnrlon=lon_max)
    # Crear una figura de Matplotlib
    fig = plt.figure(figsize=(12, 9))

    # Dibuja líneas de la costa y fronteras políticas
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()
    lon , lat = np.meshgrid(lons,lats)
    x,y = m(lon, lat)
    C_scale = m.pcolor(x,y,np.squeeze(preci[n, : , :]), cmap = 'jet' )
    c_bar = m.colorbar(C_scale , location= 'right', pad = '10%' )
    
  
    # Dibujar meridianos y paralelos
    m.drawmeridians(range(lon_min , lon_max , 5), labels=[0, 0, 0, 1])
    m.drawparallels(range(lat_min, lat_max, 2), labels=[1, 0, 0, 0])


    # Mostrar el mapa
    plt.title("Mapa Base con Basemap")
    plt.show()