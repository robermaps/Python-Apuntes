# -*- coding: utf8 -*-
 
import os, shutil
 
# Valores de entrada del usuario
img_dir = str(input('Introduzca la ruta en la que se encuentran las imagenes: '))
 
prov_dir = str(input('Introduzca la ruta en la que se encuentran las provincias: '))
 
codigo = str(input('Introduzca el codigo EPSG al que quiere reproyectar las capas: ')) 
 
distancia = str(input('Introduzca la distancia entre curvas de nivel: '))
 
 
# Crear carpeta de salida
carpeta = f'{prov_dir}/cn{distancia}'
 
print(f'Creando la carpteta de salida -{carpeta}...')
 
if os.path.exists(carpeta):
    shutil.rmtree(carpeta)
    os.mkdir(carpeta)
    print('La carpeta ya esxistia y se ha sistituido por una nueva y vacia')
else:
    os.mkdir(carpeta)
    print('Carpeta creada')


## Generar raster virtual
print('Generando el raster virtual...')
 
# cambiar al directorio de las imágenes 
os.chdir(img_dir)
 
# comando para crear un archivo de texto que liste los MDE
os.system('dir /b *.tif > archivos.txt')
 
# comando para generar el mosaico en forma de raster virtual
os.system('gdalbuildvrt mosaico.vrt -input_file_list archivos.txt')
 
print('Raster virtual generado')


## Vectorizacion de curvas de nivel
print('Vectorizando curvas de nivel...')
 
os.system(f'gdal_contour -a elev -i {distancia} mosaico.vrt cn{distancia}.shp')
 
print('Curvas de nivel vectorizadas')
 
# Reproyeccion
print(f'Reproyectando las curvas de nivel a EPSG:{codigo}')
 
os.system(f'ogr2ogr -t_srs EPSG:{codigo} cn{distancia}_rep.shp cn{distancia}.shp')
 
print(f'Las curvas se han reproyectado a EPSG:{codigo}')

# Indice espacial
print('Creando indice espacial...')
 
os.system(f'ogrinfo cn{distancia}_rep.shp -sql "CREATE SPATIAL INDEX ON cn{distancia}_rep"')
 
print('Indice espacial creado')


## Recorte
print('Recortando las curvas de nivel para cada provincia en un nuevo archivo GeoPackage...')
 
# Cambiar a la carpeta de provincias
os.chdir(prov_dir)
 
# Creacion de contadores
count = 0
update = ''
 
# Iterar sobre los archivos de la carpeta de provincias
for provincia in os.listdir(prov_dir):
 
    # si los archivos son shapes...
    if provincia.endswith('.shp'):
 
        # añadir -update al comando 
        if count > 1:
            update = '-update'
 
        nombre = os.path.splitext(provincia)[0]
        print(f'Recortando curvas de nivel para la provincia de {nombre}')
 
        # comando para recortar capas
        os.system(f'ogr2ogr -f GPKG {carpeta}/cn{distancia}.gpkg -progress -clipsrc {provincia} {img_dir}/cn{distancia}_rep.shp {update} -nln {nombre}')
 
        # incrementar el contador
        count += 1
 
        print(f'Curvas de nivel para la provincia de {nombre} recortadas')
 
print('Terminado')