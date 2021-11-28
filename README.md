<div>
    <p style="font-size:30px;"> Digital House - Desafio Final | <img src="https://www.digitalhouse.com/logo-DH.png" align="center" width="300" height="300"></p>
</div>

<font color='blue'>
    
Tabla de Contenidos:

1. [Introducción](#intro)
2. [Construcción del dataset](#dataset)
3. [EDA](#eda)
4. [Modelado](#modelado)

<hr>
<div id='intro'>
    <h2> Introducción </h2>
</div>
<hr>

<p>La presente notebook tiene por objetivo el desarrollo del Trabajo Práctico Final Integrador del Grupo 7.

Hoy en día una ambulancia del SAME tarda aproximadamente entre 20 y 30 mínutos en llegar a lugar de un accidente (<a href="https://www.lanacion.com.ar/sociedad/same-una-emergencia-cada-155-minutos-nid1442582/">Referencia</a>). Este tiempo de llegada es en el mejor de los casos cuando la llamada se realiza al 107 y no al 911, como ocurre muchas veces y en el traspaso de la urgencia se pierde todavía más tiempo. Minutos perdidos que podrían ser muy valiosos...
    
La idea de este proyecto es poder predecir la cantidad de accidentes que pueden llegar a haber en una determinada zona de la Ciudad Autónoma de Buenos Aires, considerando distintas variables de las fechas y estado del clima. De esta forma, podrían ubicarse `Spots Ambulatorios` en <b>zonas de mayor riesgo de accidentes de tránsito</b>, llegando a estos lugares con mayor rapidez.
    
Para ello, se elaboró un dataset que fue obtenido de la página del <a href="https://data.buenosaires.gob.ar/dataset/">CABA</a>, junto a otros datos fueron obtenido través de un scrapping realizado sobre la página <a href="https://www.wunderground.com/">Wunderground</a>.</p>

`Imports de librerías necesarias`


```python
import pandas as pd
from datetime import datetime
import re
from datetime import date, datetime, timedelta
import geopandas as gpd
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import random
import numpy as np
from datetime import datetime as dt
import shapely.wkt
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
#import built_in_functions

%matplotlib inline
```


```python

```

<hr>
<div id='dataset'>
    <h2> Construcción del dataset </h2>
</div>
<hr>

<p>Las siguientes celdas constan tanto de <b>lectura</b> como de <b>limpieza</b> de datos para formar el dataset de siniestros viales.


```python
#Importamos DF Siniestros
siniestros_df = pd.read_csv('Victimas_siniestros_2015-2018.csv')

#Convertimos a Geo Points
siniestros_df = gpd.GeoDataFrame(siniestros_df,geometry=gpd.points_from_xy(siniestros_df.x, siniestros_df.y))
#siniestros_df['fecha'] = pd.to_datetime(siniestros_df['fecha'],format='%m/%d/%Y')
siniestros_df.head()
```

    /Users/bpeco/opt/anaconda3/lib/python3.8/site-packages/IPython/core/interactiveshell.py:3146: DtypeWarning: Columns (9) have mixed types.Specify dtype option on import or set low_memory=False.
      has_raised = await self.run_ast_nodes(code_ast.body, cell_name,





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>causa</th>
      <th>rol</th>
      <th>tipo</th>
      <th>sexo</th>
      <th>edad</th>
      <th>mes</th>
      <th>periodo</th>
      <th>fecha</th>
      <th>hora</th>
      <th>lugar_hecho</th>
      <th>...</th>
      <th>x</th>
      <th>y</th>
      <th>geom</th>
      <th>cantidad_victimas</th>
      <th>comuna</th>
      <th>geom_3857</th>
      <th>tipo_colision1</th>
      <th>participantes_victimas</th>
      <th>participantes_acusados</th>
      <th>geometry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>homicidio</td>
      <td>conductor</td>
      <td>moto</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2.0</td>
      <td>2015</td>
      <td>2/14/2015</td>
      <td>19:00:00</td>
      <td>cafayate y severo garcia grande de zequeira</td>
      <td>...</td>
      <td>-58.508658</td>
      <td>-34.653489</td>
      <td>0101000020E610000057E042B51B414DC008419885A553...</td>
      <td>1</td>
      <td>9.0</td>
      <td>0101000020110F0000DE9B958180D858C1EC802966CD68...</td>
      <td>motovehiculo - vehiculo</td>
      <td>moto</td>
      <td>automovil</td>
      <td>POINT (-58.50866 -34.65349)</td>
    </tr>
    <tr>
      <th>1</th>
      <td>homicidio</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2.0</td>
      <td>2015</td>
      <td>2/25/2015</td>
      <td>3:00:00</td>
      <td>lugones, leopoldo av. y udaondo, guillermo av.</td>
      <td>...</td>
      <td>-58.447680</td>
      <td>-34.543513</td>
      <td>0101000020E6100000CC4C4C904D394DC0FAF382D99145...</td>
      <td>1</td>
      <td>13.0</td>
      <td>0101000020110F0000BFBC457BDFD158C1E1DDA818C14B...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>POINT (-58.44768 -34.54351)</td>
    </tr>
    <tr>
      <th>2</th>
      <td>homicidio</td>
      <td>peaton</td>
      <td>peaton</td>
      <td>femenino</td>
      <td>NaN</td>
      <td>2.0</td>
      <td>2015</td>
      <td>2/27/2015</td>
      <td>8:00:00</td>
      <td>avda jujuy y avda independencia</td>
      <td>...</td>
      <td>-58.403516</td>
      <td>-34.618839</td>
      <td>0101000020E6100000FBC35B67A6334DC03F854E1F364F...</td>
      <td>1</td>
      <td>3.0</td>
      <td>0101000020110F0000F8067D6812CD58C189755F66A55F...</td>
      <td>peaton - vehiculo</td>
      <td>peaton</td>
      <td>"transporte publico"</td>
      <td>POINT (-58.40352 -34.61884)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>homicidio</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>3.0</td>
      <td>2015</td>
      <td>03-02-15</td>
      <td>18:30:00</td>
      <td>lavalle 1730</td>
      <td>...</td>
      <td>-58.391329</td>
      <td>-34.603168</td>
      <td>0101000020E6100000312FB20D17324DC064587D9E344D...</td>
      <td>1</td>
      <td>1.0</td>
      <td>0101000020110F00005621683DBFCB58C10B59E69B815B...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>POINT (-58.39133 -34.60317)</td>
    </tr>
    <tr>
      <th>4</th>
      <td>homicidio</td>
      <td>pasajero</td>
      <td>camion</td>
      <td>masculino</td>
      <td>NaN</td>
      <td>4.0</td>
      <td>2015</td>
      <td>04-09-15</td>
      <td>1:20:00</td>
      <td>ave salvador m del carril 2434</td>
      <td>...</td>
      <td>-58.492895</td>
      <td>-34.587489</td>
      <td>0101000020E61000009BDD7231173F4DC02D782AD7324B...</td>
      <td>1</td>
      <td>15.0</td>
      <td>0101000020110F00006F2F76D4C9D658C1750825735D57...</td>
      <td>vehiculo - vehiculo</td>
      <td>camion</td>
      <td>camion</td>
      <td>POINT (-58.49290 -34.58749)</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 30 columns</p>
</div>




```python
#Importamos DF Barrios
barrios = gpd.read_file("barrios.csv")
```


```python
def from_wkt(dataframe, wkt_column):
    '''
    Obtiene las coordenadas de una columna WKT.

    Retorna un dataframe igual a `dataframe` con una columna nueva `coordenadas` en la cual se encuentra la columna `wkt_column` en el correcto formato geoespacial.

    Parameters
    ----------
    dataframe : dataframe en el cual se encuentra la columna WKT.

    wkt_column : columna a través de la cual se va a obtener la nueva columna `coordenadas` en formato geoespacial.
    '''


    dataframe["coordenadas"]= dataframe[wkt_column].apply(shapely.wkt.loads)
    geo_barrios = gpd.GeoDataFrame(dataframe, geometry='coordenadas')
    return geo_barrios
```


```python
# change geometry
barrios = from_wkt(barrios, "WKT")
```


```python
barrios["WKT"] = barrios["WKT"].apply(shapely.wkt.loads) 
barrios = gpd.GeoDataFrame(barrios, geometry='WKT')
type(barrios)
```




    geopandas.geodataframe.GeoDataFrame




```python
n=0
for index_siniestros, row_siniestros in siniestros_df.iterrows():
    if n in [1000, 5000, 10000, 15000, 25000, 30000]:
        print(n)
    for index_barrios, row_barrios in barrios.iterrows():
        if row_barrios['coordenadas'].contains(row_siniestros['geometry']):
            siniestros_df.loc[n, 'Barrio'] = row_barrios['barrio']
            break
    n+=1
```

    1000
    5000
    10000
    15000
    25000
    30000



```python
siniestros_df.head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>causa</th>
      <th>rol</th>
      <th>tipo</th>
      <th>sexo</th>
      <th>edad</th>
      <th>mes</th>
      <th>periodo</th>
      <th>fecha</th>
      <th>hora</th>
      <th>lugar_hecho</th>
      <th>...</th>
      <th>y</th>
      <th>geom</th>
      <th>cantidad_victimas</th>
      <th>comuna</th>
      <th>geom_3857</th>
      <th>tipo_colision1</th>
      <th>participantes_victimas</th>
      <th>participantes_acusados</th>
      <th>geometry</th>
      <th>Barrio</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>homicidio</td>
      <td>conductor</td>
      <td>moto</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2.0</td>
      <td>2015</td>
      <td>2/14/2015</td>
      <td>19:00:00</td>
      <td>cafayate y severo garcia grande de zequeira</td>
      <td>...</td>
      <td>-34.653489</td>
      <td>0101000020E610000057E042B51B414DC008419885A553...</td>
      <td>1</td>
      <td>9.0</td>
      <td>0101000020110F0000DE9B958180D858C1EC802966CD68...</td>
      <td>motovehiculo - vehiculo</td>
      <td>moto</td>
      <td>automovil</td>
      <td>POINT (-58.50866 -34.65349)</td>
      <td>MATADEROS</td>
    </tr>
    <tr>
      <th>1</th>
      <td>homicidio</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2.0</td>
      <td>2015</td>
      <td>2/25/2015</td>
      <td>3:00:00</td>
      <td>lugones, leopoldo av. y udaondo, guillermo av.</td>
      <td>...</td>
      <td>-34.543513</td>
      <td>0101000020E6100000CC4C4C904D394DC0FAF382D99145...</td>
      <td>1</td>
      <td>13.0</td>
      <td>0101000020110F0000BFBC457BDFD158C1E1DDA818C14B...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>POINT (-58.44768 -34.54351)</td>
      <td>BELGRANO</td>
    </tr>
    <tr>
      <th>2</th>
      <td>homicidio</td>
      <td>peaton</td>
      <td>peaton</td>
      <td>femenino</td>
      <td>NaN</td>
      <td>2.0</td>
      <td>2015</td>
      <td>2/27/2015</td>
      <td>8:00:00</td>
      <td>avda jujuy y avda independencia</td>
      <td>...</td>
      <td>-34.618839</td>
      <td>0101000020E6100000FBC35B67A6334DC03F854E1F364F...</td>
      <td>1</td>
      <td>3.0</td>
      <td>0101000020110F0000F8067D6812CD58C189755F66A55F...</td>
      <td>peaton - vehiculo</td>
      <td>peaton</td>
      <td>"transporte publico"</td>
      <td>POINT (-58.40352 -34.61884)</td>
      <td>BALVANERA</td>
    </tr>
    <tr>
      <th>3</th>
      <td>homicidio</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>3.0</td>
      <td>2015</td>
      <td>03-02-15</td>
      <td>18:30:00</td>
      <td>lavalle 1730</td>
      <td>...</td>
      <td>-34.603168</td>
      <td>0101000020E6100000312FB20D17324DC064587D9E344D...</td>
      <td>1</td>
      <td>1.0</td>
      <td>0101000020110F00005621683DBFCB58C10B59E69B815B...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>POINT (-58.39133 -34.60317)</td>
      <td>SAN NICOLAS</td>
    </tr>
    <tr>
      <th>4</th>
      <td>homicidio</td>
      <td>pasajero</td>
      <td>camion</td>
      <td>masculino</td>
      <td>NaN</td>
      <td>4.0</td>
      <td>2015</td>
      <td>04-09-15</td>
      <td>1:20:00</td>
      <td>ave salvador m del carril 2434</td>
      <td>...</td>
      <td>-34.587489</td>
      <td>0101000020E61000009BDD7231173F4DC02D782AD7324B...</td>
      <td>1</td>
      <td>15.0</td>
      <td>0101000020110F00006F2F76D4C9D658C1750825735D57...</td>
      <td>vehiculo - vehiculo</td>
      <td>camion</td>
      <td>camion</td>
      <td>POINT (-58.49290 -34.58749)</td>
      <td>AGRONOMIA</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 31 columns</p>
</div>



> Generamos un dataframe con las fechas correspondientes 2015 hasta 2018. Nos va a ser útil más adelante en la notebook para generar el dataset complemento (es decir, cuando no hubieron accidentes).


```python
Dates_combined = pd.date_range(start='1/1/2015', end='05/31/2018', freq = "1 H")
Dates_combined = Dates_combined.format(formatter=lambda x: x.strftime('%Y-%m-%d %H'))
Dates_combined = pd.DataFrame(Dates_combined)
Dates_combined = Dates_combined.rename(columns={0: 'Date'})
Dates_combined['Hour'] = Dates_combined['Date'].apply(lambda x : x.split()[1])

Dates_combined['Date'] = pd.to_datetime(Dates_combined['Date'],format = '%Y-%m-%d')
Dates_combined['Date'] = Dates_combined['Date'].dt.date
Dates_combined['Hour'] = Dates_combined['Hour'].astype(int)
Dates_combined
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Date</th>
      <th>Hour</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2015-01-01</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2015-01-01</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2015-01-01</td>
      <td>2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2015-01-01</td>
      <td>3</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2015-01-01</td>
      <td>4</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>29900</th>
      <td>2018-05-30</td>
      <td>20</td>
    </tr>
    <tr>
      <th>29901</th>
      <td>2018-05-30</td>
      <td>21</td>
    </tr>
    <tr>
      <th>29902</th>
      <td>2018-05-30</td>
      <td>22</td>
    </tr>
    <tr>
      <th>29903</th>
      <td>2018-05-30</td>
      <td>23</td>
    </tr>
    <tr>
      <th>29904</th>
      <td>2018-05-31</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>29905 rows × 2 columns</p>
</div>




```python
siniestros_df = siniestros_df.dropna(subset=['fecha', 'mes', 'hora']).reset_index(drop=True)
#siniestros_df = siniestros_df.dropna(subset=['mes'])
```


```python
#siniestros_df.info()
```

 

> Funcion para estandarizar la fecha de una columna



```python
def format_date_in_df(dataset, date_column):
    '''
    Estandariza el formato de una columna fecha con varios formatos.

    Retorna un dataframe igual a `dataset` con una columna nueva `date_columns` estandarizada separando año, mes y día con una "/".

    Parameters
    ----------
    dataframe : dataframe en el cual se encuentra la columna de fecha a estandarizar.

    date_column : columna a través de la cual se va a obtener la nueva columna `fecha_std` en formato estandarizado.
    '''
    
    #1er paso reemplazar los guiones por '/'
    dataset[date_column] = dataset[date_column].apply(lambda f: f.replace('-', '/'))
    
    #2do paso extraer el dia de la columna fecha
    pattern = '/(\d+)/'
    re.compile(pattern, flags=re.IGNORECASE)
    dias = dataset[date_column].apply(lambda f: re.search(pattern, f).groups()[0])
    
    #dataset[date_column] = dataset[date_column].apply(lambda f: '0' + f if f[0] != 0 or (f[:2] != '10' and f[:2] != '11' and f[:2] != '12') else pass)
    
    dataset['dia'] = dias
    
    #3er paso juntar el dia, mes y año con la '/'
    dataset['fecha_std'] = dataset.dia + '/' + dataset.mes.astype(str) + '/' + dataset.periodo.astype(str)
    #display(dataset['dia/mes/periodo'])
    
    #4to paso crear la columna estandarizada
    dataset['fecha_std'] = dataset['fecha_std'].apply(lambda f: datetime.strptime(f, '%d/%m/%Y'))
    
    return dataset
```


```python
#Reemplazamos los valores nulos por 0
siniestros_df.mes.fillna(value=0., inplace=True)

#Cambiamos el tipo de dato de la columna "mes"
siniestros_df.mes = siniestros_df.mes.astype(int)
```


```python
#Usamos la función creada para formatear la columna de fecha
siniestros_df = format_date_in_df(siniestros_df, 'fecha')
```


```python
siniestros_df['solo_hora'] = siniestros_df.hora.apply(lambda h: h.split(':')[0])
```


```python
#Pasamos a tipo de dato fecha la columna 'fecha_std'
siniestros_df['fecha_std'] = siniestros_df['fecha_std'].dt.date
```

 

 

`Creación del dataset complemento`

Todo lo anterior estaba relacionado a un dataset donde para cada fecha, hora y barrio había una accidente.
Si nos hubiéramos quedado con solo ese dataset, el modelo iba a estar entrenado de forma sesgada con la premisa de que siempre va a haber una accidente, y esto es un error.

Es por ello que lo que continúa es la elaboración del dataset complemento, es decir, fechas, horas y barrios donde no hubieron accidentes.

 

> La lista que se encuentra a continuación es una "clave" que se formó a través de la concatenación de la fecha, hora y barrio con un guión bajo, de toda aquella fecha_hora_barrio en la que hubo un accidente


```python
fechas_confirm = siniestros_df[['fecha_std', 'solo_hora', 'Barrio']].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)
fechas_confirm
```




    0          2015-02-14_19_MATADEROS
    1            2015-02-25_3_BELGRANO
    2           2015-02-27_8_BALVANERA
    3        2015-03-02_18_SAN NICOLAS
    4           2015-04-09_1_AGRONOMIA
                       ...            
    33157            2018-05-30_17_nan
    33158    2018-05-31_20_SAN NICOLAS
    33159    2018-05-31_9_VILLA CRESPO
    33160    2018-05-31_9_VILLA CRESPO
    33161      2018-05-31_14_CHACARITA
    Length: 33162, dtype: object



 

> A continuanción se forma la lista con la misma lógica de la "clave" con guión bajo, para toda posible fecha, hora y barrio. Con esta lista lo que estamos suponiendo -a priori- es que en todas estas claves NO hubo un accidente.


```python
Dates_combined['Date_as_DT'] = pd.to_datetime(Dates_combined['Date'])
```


```python
Dates_combined.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Date</th>
      <th>Hour</th>
      <th>Date_as_DT</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2015-01-01</td>
      <td>0</td>
      <td>2015-01-01</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2015-01-01</td>
      <td>1</td>
      <td>2015-01-01</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2015-01-01</td>
      <td>2</td>
      <td>2015-01-01</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2015-01-01</td>
      <td>3</td>
      <td>2015-01-01</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2015-01-01</td>
      <td>4</td>
      <td>2015-01-01</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Dates_combined
date_hour_barrio_df = pd.DataFrame()
```


```python
n = 0
for index, row in Dates_combined.iterrows():
    for b in barrios.barrio:
        date_hour_barrio_df.loc[n,"Key"] = str(row['Date']) + "_" + str(row['Hour']) + "_" + b
        n+=1
        
```


```python
date_hour_barrio_df=pd.read_csv('complemento_df.csv').drop("Unnamed: 0", axis=1)
date_hour_barrio_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Key_final</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2015-01-01_0_CHACARITA</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2015-01-01_0_PATERNAL</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2015-01-01_0_VILLA CRESPO</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2015-01-01_0_VILLA DEL PARQUE</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2015-01-01_0_ALMAGRO</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
    </tr>
    <tr>
      <th>1435387</th>
      <td>2018-05-31_23_BELGRANO</td>
    </tr>
    <tr>
      <th>1435388</th>
      <td>2018-05-31_23_RECOLETA</td>
    </tr>
    <tr>
      <th>1435389</th>
      <td>2018-05-31_23_RETIRO</td>
    </tr>
    <tr>
      <th>1435390</th>
      <td>2018-05-31_23_NUÃ‘EZ</td>
    </tr>
    <tr>
      <th>1435391</th>
      <td>2018-05-31_23_BOCA</td>
    </tr>
  </tbody>
</table>
<p>1435392 rows × 1 columns</p>
</div>




```python
#NO CORRER
#n=0
#for index, row in data_2015.iterrows():
#    if n in [1000, 2500, 5000, 10000, 50000, 100000, 200000, 300000, 400000]:
#        print(n)
#    texto = row['Key']
#    try:
#        flag = int(texto[10:12])
#        texto = texto[:10]+'_'+texto[10:12]+'_'+texto[12:]
#    except:
#        texto=texto[:10]+'_'+texto[10:11]+'_'+texto[11:]
#    
#    data_2015.loc[n, 'Key_final'] = texto
#    
#    n+=1
```

> Luego de formar la lista de claves donde todas son asumidas como "no accidentes", guardamos en una lista los índices de las llaves que aparecen en la lista `fechas_confirm` (recordando que esta última lista era la que tenía las "claves" de los registros confirmados con accidentes).
>
> Posteriormente estos índices los removemos de la lista de "no accidentes", por lo que ahora sí esta lista está conformada únicamente por momentos-lugares donde NO hubieron accidentes.


```python
drop_indexes = []
n=0
for index, row in date_hour_barrio_df.iterrows():
    if n in [10000, 50000, 100000, 250000, 500000, 750000, 1000000]:
        print(n)
    if row['Key_final'] in fechas_confirm.values:
        drop_indexes.append(index)

    n+=1
#Dates_combined.drop(drop_indexes, inplace = True)
```

    10000
    50000
    100000
    250000
    500000
    750000
    1000000



```python
date_hour_barrio_df.drop(drop_indexes, inplace = True)
```


```python
date_hour_barrio_df.reset_index(drop=True, inplace=True)
```


```python
date_hour_barrio_df.head(2)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Key_final</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2015-01-01_0_CHACARITA</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2015-01-01_0_PATERNAL</td>
    </tr>
  </tbody>
</table>
</div>




```python
date_hour_barrio_df['fecha_std'] = date_hour_barrio_df.Key_final.apply(lambda k: k.split('_')[0])
date_hour_barrio_df['solo_hora'] = date_hour_barrio_df.Key_final.apply(lambda k: k.split('_')[1])
date_hour_barrio_df['Barrio'] = date_hour_barrio_df.Key_final.apply(lambda k: k.split('_')[2])
```


```python
date_hour_barrio_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Key_final</th>
      <th>fecha_std</th>
      <th>solo_hora</th>
      <th>Barrio</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2015-01-01_0_CHACARITA</td>
      <td>2015-01-01</td>
      <td>0</td>
      <td>CHACARITA</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2015-01-01_0_PATERNAL</td>
      <td>2015-01-01</td>
      <td>0</td>
      <td>PATERNAL</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2015-01-01_0_VILLA CRESPO</td>
      <td>2015-01-01</td>
      <td>0</td>
      <td>VILLA CRESPO</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2015-01-01_0_VILLA DEL PARQUE</td>
      <td>2015-01-01</td>
      <td>0</td>
      <td>VILLA DEL PARQUE</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2015-01-01_0_ALMAGRO</td>
      <td>2015-01-01</td>
      <td>0</td>
      <td>ALMAGRO</td>
    </tr>
  </tbody>
</table>
</div>




```python
#full_df
#full_df.to_csv('solo_accidentes.csv')
```


```python
#pd.read_csv('solo_accidentes.csv').drop('Unnamed: 0', axis=1)
```


```python
#siniestros_df.to_csv('solo_accidentes_v2.csv')
```


```python
#full_df = pd.read_csv('solo_accidentes.csv').drop('Unnamed: 0', axis=1)
```

 

 

`Unión de dataframe de accidentes y no accidentes`


```python
#Append de Sinistros DF con Dates Combined + Merge con clima
full_df = siniestros_df.append(date_hour_barrio_df.drop('Key_final',axis=1), ignore_index=True)
```


```python
full_df['fecha_std_datetime'] = full_df['fecha_std'].apply(lambda d: pd.to_datetime(d))
```


```python
#Creamos una columna que tiene únicamente el dia y el mes
full_df['dia/mes'] = full_df['fecha_std_datetime'].apply(lambda f: str(f.day)+'/'+str(f.month))
```


```python
full_df.info()
```

    <class 'geopandas.geodataframe.GeoDataFrame'>
    RangeIndex: 1439983 entries, 0 to 1439982
    Data columns (total 36 columns):
     #   Column                        Non-Null Count    Dtype         
    ---  ------                        --------------    -----         
     0   causa                         33162 non-null    object        
     1   rol                           32830 non-null    object        
     2   tipo                          32067 non-null    object        
     3   sexo                          32969 non-null    object        
     4   edad                          32610 non-null    float64       
     5   mes                           33162 non-null    float64       
     6   periodo                       33162 non-null    float64       
     7   fecha                         33162 non-null    object        
     8   hora                          33162 non-null    object        
     9   lugar_hecho                   29462 non-null    object        
     10  direccion_normalizada         32403 non-null    object        
     11  tipo_calle                    33162 non-null    object        
     12  direccion_normalizada_arcgis  32396 non-null    object        
     13  calle1                        32403 non-null    object        
     14  altura                        7094 non-null     float64       
     15  calle2                        24941 non-null    object        
     16  codigo_calle                  23890 non-null    float64       
     17  codigo_cruce                  20659 non-null    float64       
     18  geocodificacion               32074 non-null    object        
     19  semestre                      33162 non-null    float64       
     20  x                             32074 non-null    float64       
     21  y                             32074 non-null    float64       
     22  geom                          32074 non-null    object        
     23  cantidad_victimas             33162 non-null    float64       
     24  comuna                        32071 non-null    float64       
     25  geom_3857                     32074 non-null    object        
     26  tipo_colision1                31829 non-null    object        
     27  participantes_victimas        32036 non-null    object        
     28  participantes_acusados        32488 non-null    object        
     29  geometry                      33162 non-null    geometry      
     30  Barrio                        1438895 non-null  object        
     31  dia                           33162 non-null    object        
     32  fecha_std                     1439983 non-null  object        
     33  solo_hora                     1439983 non-null  object        
     34  fecha_std_datetime            1439983 non-null  datetime64[ns]
     35  dia/mes                       1439983 non-null  object        
    dtypes: datetime64[ns](1), float64(11), geometry(1), object(23)
    memory usage: 395.5+ MB



```python
full_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>causa</th>
      <th>rol</th>
      <th>tipo</th>
      <th>sexo</th>
      <th>edad</th>
      <th>mes</th>
      <th>periodo</th>
      <th>fecha</th>
      <th>hora</th>
      <th>lugar_hecho</th>
      <th>...</th>
      <th>tipo_colision1</th>
      <th>participantes_victimas</th>
      <th>participantes_acusados</th>
      <th>geometry</th>
      <th>Barrio</th>
      <th>dia</th>
      <th>fecha_std</th>
      <th>solo_hora</th>
      <th>fecha_std_datetime</th>
      <th>dia/mes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>homicidio</td>
      <td>conductor</td>
      <td>moto</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2.0</td>
      <td>2015.0</td>
      <td>2/14/2015</td>
      <td>19:00:00</td>
      <td>cafayate y severo garcia grande de zequeira</td>
      <td>...</td>
      <td>motovehiculo - vehiculo</td>
      <td>moto</td>
      <td>automovil</td>
      <td>POINT (-58.50866 -34.65349)</td>
      <td>MATADEROS</td>
      <td>14</td>
      <td>2015-02-14</td>
      <td>19</td>
      <td>2015-02-14</td>
      <td>14/2</td>
    </tr>
    <tr>
      <th>1</th>
      <td>homicidio</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2.0</td>
      <td>2015.0</td>
      <td>2/25/2015</td>
      <td>3:00:00</td>
      <td>lugones, leopoldo av. y udaondo, guillermo av.</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>POINT (-58.44768 -34.54351)</td>
      <td>BELGRANO</td>
      <td>25</td>
      <td>2015-02-25</td>
      <td>3</td>
      <td>2015-02-25</td>
      <td>25/2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>homicidio</td>
      <td>peaton</td>
      <td>peaton</td>
      <td>femenino</td>
      <td>NaN</td>
      <td>2.0</td>
      <td>2015.0</td>
      <td>2/27/2015</td>
      <td>8:00:00</td>
      <td>avda jujuy y avda independencia</td>
      <td>...</td>
      <td>peaton - vehiculo</td>
      <td>peaton</td>
      <td>"transporte publico"</td>
      <td>POINT (-58.40352 -34.61884)</td>
      <td>BALVANERA</td>
      <td>27</td>
      <td>2015-02-27</td>
      <td>8</td>
      <td>2015-02-27</td>
      <td>27/2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>homicidio</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>3.0</td>
      <td>2015.0</td>
      <td>03/02/15</td>
      <td>18:30:00</td>
      <td>lavalle 1730</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>POINT (-58.39133 -34.60317)</td>
      <td>SAN NICOLAS</td>
      <td>02</td>
      <td>2015-03-02</td>
      <td>18</td>
      <td>2015-03-02</td>
      <td>2/3</td>
    </tr>
    <tr>
      <th>4</th>
      <td>homicidio</td>
      <td>pasajero</td>
      <td>camion</td>
      <td>masculino</td>
      <td>NaN</td>
      <td>4.0</td>
      <td>2015.0</td>
      <td>04/09/15</td>
      <td>1:20:00</td>
      <td>ave salvador m del carril 2434</td>
      <td>...</td>
      <td>vehiculo - vehiculo</td>
      <td>camion</td>
      <td>camion</td>
      <td>POINT (-58.49290 -34.58749)</td>
      <td>AGRONOMIA</td>
      <td>09</td>
      <td>2015-04-09</td>
      <td>1</td>
      <td>2015-04-09</td>
      <td>9/4</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 36 columns</p>
</div>



 

 

`Agregado de variables que pueden influir en la ocurrencia de un accidente`

### ==> Variable: Estación del año <==


```python
Y = 2015
estaciones = [('verano', (date(Y,  1,  1),  date(Y,  3, 20))),
           ('otoño', (date(Y,  3, 21),  date(Y,  6, 20))),
           ('invierno', (date(Y,  6, 21),  date(Y,  9, 22))),
           ('primavera', (date(Y,  9, 23),  date(Y, 12, 20))),
           ('verano', (date(Y, 12, 21),  date(Y, 12, 31)))]
```


```python
def obtener_estacion(fecha):
    '''
    Obteniene la estación del año a la cual pertenece una fecha.

    Parameters
    ----------
    fecha : fecha de la cual se desea conocer la estación.
    '''
    if isinstance(fecha, datetime):
        fecha = fecha.date()
        
    #print(fecha.day==29)
    #print(fecha.month==2)
    if fecha.day == 29 and fecha.month == 2:
        #print(fecha)
        fecha = fecha - timedelta(1)
        #print(fecha)
        
    fecha = fecha.replace(year=Y) #reemplaza cualquier año por el 2015 (o lo definido en la variable Y)
    return next(estacion for estacion, (empieza, termina) in estaciones
                if empieza <= fecha <= termina)

```


```python
full_df['estacion'] = full_df['fecha_std_datetime'].apply(lambda f: obtener_estacion(f))
```

 

### ==> Variable: Fin de semana <==


```python
full_df['dia_semana'] = full_df.fecha_std_datetime.apply(lambda f: f.strftime("%A"))
```


```python
def get_dummie_day(day):
    '''
    Convierte en dummie dependiendo si una `fecha` es día hábil o no.

    Parameters
    ----------
    day : día del cual se desea obtener la variable dummie.
    '''
    
    if day in ['Saturday', 'Sunday']:
        return 1
    else:
        return 0
```


```python
full_df['fin_de_semana_dummie'] = full_df['dia_semana'].apply(lambda d: get_dummie_day(d))
```


```python
#full_df#[['fecha_std', 'solo_hora', 'dia/mes', 'Barrio', 'estacion', 'fin_de_semana_dummie']]
```


```python

```

 

### ==> Variable: Estado del clima <==

`Levantamos el dataset del clima`

<p>Para obtener esta información, realizamos un scrapping sobre la página <a href="https://www.wunderground.com/">Wunderground</a>.

La base de este scrapping fue obtenido gracias al Profesor Felix Penna. Utilizando dicha .ipynb como apoyo, sumado a algunos cambios que realizamos, logramos sacar la información del clima para cada fecha y hora comprendida entre el 01/01/2015 y el 31/05/2018, dado que la información de siniestros disponible data el mismo rango de fechas. Esta data la guardamos en el csv `info_clima.csv`<br> Sin embargo, hubieron algunas fechas para las cuales la página no devolvía información alguna, por lo que luego estos registros serán descartados.</p>


```python
clima_df = pd.read_csv('info_clima.csv').drop(['Unnamed: 0', 'Rain_Ml'], axis=1)
```


```python
clima_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Date</th>
      <th>Hour</th>
      <th>AM/PM</th>
      <th>Wind_Speed</th>
      <th>Condition</th>
      <th>Only_Hour</th>
      <th>Full_Hour</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2015-01-01</td>
      <td>12:00</td>
      <td>AM</td>
      <td>2.0</td>
      <td>Fair</td>
      <td>12</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2015-01-01</td>
      <td>1:00</td>
      <td>AM</td>
      <td>2.0</td>
      <td>Fair</td>
      <td>1</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2015-01-01</td>
      <td>2:00</td>
      <td>AM</td>
      <td>7.0</td>
      <td>Mostly Cloudy</td>
      <td>2</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2015-01-01</td>
      <td>3:00</td>
      <td>AM</td>
      <td>9.0</td>
      <td>Fair</td>
      <td>3</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2015-01-01</td>
      <td>4:00</td>
      <td>AM</td>
      <td>7.0</td>
      <td>Fair</td>
      <td>4</td>
      <td>4.0</td>
    </tr>
  </tbody>
</table>
</div>



> La columna "Condition" del dataset de clima contiene información sobre cómo estaba el clima en general ese día. Dada la variedad de distintas respuestas, y considerando que esta es una variable que posteriormente va a ser "dummificada", para reducir la dimensionalidad del dataset, homogeneizamos las respuestas. Es por ello que creamos el diccionario map_weather.


```python
#Disminuimos la cantidad de valores en Condition
map_weather = {'Fair / Windy':"Windy",
'Fair':"Fair",
'Partly Cloudy':"Cloudy",
'Mostly Cloudy':"Cloudy",
'Cloudy':"Cloudy",
'Drizzle':"Drizzle",
'Thunder':"Storm",
'Light Rain with Thunder':"Storm",
'T-Storm':"Storm",
'Fog':"Fog",
'Rain Shower':"Rain",
'Cloudy / Windy':"Windy",
'Light Rain':"Rain",
'Rain':"Rain",
'Heavy Rain':"Rain",
'Rain Shower / Windy':"Rain",
'Mostly Cloudy / Windy':"Cloudy",
'Shallow Fog':"Fog",
'Light Drizzle':"Drizzle",
'Haze':"Fog",
 'Partly Cloudy / Windy':"Windy",
 'Heavy T-Storm':"Storm",
 'Smoke':"Fog",
 'Heavy Rain Shower':"Rain",
 'Thunder in the Vicinity':"Storm",
 'Drizzle and Fog':"Fog",
 'Rain / Windy':"Rain",
 'Mist':"Fog",
 'Light Rain / Windy':"Rain",
 'T-Storm / Windy':"Storm",
 'Heavy T-Storm / Windy':"Storm",
 'Low Drifting Dust':"Fog",
 'Thunder and Hail':"Storm",
 'Thunder and Hail /':"Storm",
 'Heavy Drizzle':"Drizzle",
 'Heavy Drizzle / Windy':"Drizzle",
 'Drizzle / Windy':"Drizzle",
 'Volcanic Ash':"Volcanic Ash",
 'Light Drizzle / Windy':"Windy",
 'Showers in the Vicinity':"Rain",
 'Light Rain Shower':"Rain",
 'Thunder / Windy':"Storm",
 'Duststorm':"Storm"}
```


```python
clima_df['Condition'] = clima_df['Condition'].map(map_weather)
```


```python
clima_df['Date'] = pd.to_datetime(clima_df['Date'])
```


```python
clima_df['Full_Hour'] = clima_df['Full_Hour'].astype(int)
```


```python

```


```python
full_df['solo_hora']=full_df['solo_hora'].astype(int)
```

 

 

`Juntamos la información de accidentes y no accidentes con la de clima`


```python
final_df = full_df.merge(clima_df, left_on=['fecha_std_datetime', 'solo_hora'], right_on=['Date', 'Full_Hour'], how='left')#.drop_duplicates()
```

> Descartamos los registros en los cuales falta la información del clima


```python
final_df = final_df[(final_df['Wind_Speed'].notnull())]
```


```python
final_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>causa</th>
      <th>rol</th>
      <th>tipo</th>
      <th>sexo</th>
      <th>edad</th>
      <th>mes</th>
      <th>periodo</th>
      <th>fecha</th>
      <th>hora</th>
      <th>lugar_hecho</th>
      <th>...</th>
      <th>estacion</th>
      <th>dia_semana</th>
      <th>fin_de_semana_dummie</th>
      <th>Date</th>
      <th>Hour</th>
      <th>AM/PM</th>
      <th>Wind_Speed</th>
      <th>Condition</th>
      <th>Only_Hour</th>
      <th>Full_Hour</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>homicidio</td>
      <td>conductor</td>
      <td>moto</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2.0</td>
      <td>2015.0</td>
      <td>2/14/2015</td>
      <td>19:00:00</td>
      <td>cafayate y severo garcia grande de zequeira</td>
      <td>...</td>
      <td>verano</td>
      <td>Saturday</td>
      <td>1</td>
      <td>2015-02-14</td>
      <td>7:00</td>
      <td>PM</td>
      <td>33.0</td>
      <td>Windy</td>
      <td>7.0</td>
      <td>19.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>homicidio</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2.0</td>
      <td>2015.0</td>
      <td>2/25/2015</td>
      <td>3:00:00</td>
      <td>lugones, leopoldo av. y udaondo, guillermo av.</td>
      <td>...</td>
      <td>verano</td>
      <td>Wednesday</td>
      <td>0</td>
      <td>2015-02-25</td>
      <td>3:00</td>
      <td>AM</td>
      <td>24.0</td>
      <td>Fair</td>
      <td>3.0</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>homicidio</td>
      <td>peaton</td>
      <td>peaton</td>
      <td>femenino</td>
      <td>NaN</td>
      <td>2.0</td>
      <td>2015.0</td>
      <td>2/27/2015</td>
      <td>8:00:00</td>
      <td>avda jujuy y avda independencia</td>
      <td>...</td>
      <td>verano</td>
      <td>Friday</td>
      <td>0</td>
      <td>2015-02-27</td>
      <td>8:00</td>
      <td>AM</td>
      <td>20.0</td>
      <td>Cloudy</td>
      <td>8.0</td>
      <td>8.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>homicidio</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>3.0</td>
      <td>2015.0</td>
      <td>03/02/15</td>
      <td>18:30:00</td>
      <td>lavalle 1730</td>
      <td>...</td>
      <td>verano</td>
      <td>Monday</td>
      <td>0</td>
      <td>2015-03-02</td>
      <td>6:00</td>
      <td>PM</td>
      <td>13.0</td>
      <td>Fair</td>
      <td>6.0</td>
      <td>18.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>homicidio</td>
      <td>pasajero</td>
      <td>camion</td>
      <td>masculino</td>
      <td>NaN</td>
      <td>4.0</td>
      <td>2015.0</td>
      <td>04/09/15</td>
      <td>1:20:00</td>
      <td>ave salvador m del carril 2434</td>
      <td>...</td>
      <td>otoño</td>
      <td>Thursday</td>
      <td>0</td>
      <td>2015-04-09</td>
      <td>1:00</td>
      <td>AM</td>
      <td>13.0</td>
      <td>Fair</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 46 columns</p>
</div>




```python

```

 

`Levantamos la información de días feriados`


```python
feriados= pd.read_csv('Feriados_15-18.csv',delimiter=";")
```


```python
feriados = feriados[feriados['FECHA']<='2018-05-31']
```


```python
feriados['FECHA'] = pd.to_datetime(feriados['FECHA'], format="%d/%m/%Y")
```

Se la agregamos al dataset de accidentes y no accidentes


```python
final_df=pd.merge(final_df,feriados,how='left', left_on="fecha_std_datetime", right_on="FECHA")
```


```python
final_df=final_df.drop(['FECHA'],axis=1)
```


```python
final_df['FERIADO'].fillna(0, inplace=True)
```


```python
final_df.head(2)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>causa</th>
      <th>rol</th>
      <th>tipo</th>
      <th>sexo</th>
      <th>edad</th>
      <th>mes</th>
      <th>periodo</th>
      <th>fecha</th>
      <th>hora</th>
      <th>lugar_hecho</th>
      <th>...</th>
      <th>dia_semana</th>
      <th>fin_de_semana_dummie</th>
      <th>Date</th>
      <th>Hour</th>
      <th>AM/PM</th>
      <th>Wind_Speed</th>
      <th>Condition</th>
      <th>Only_Hour</th>
      <th>Full_Hour</th>
      <th>FERIADO</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>homicidio</td>
      <td>conductor</td>
      <td>moto</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2.0</td>
      <td>2015.0</td>
      <td>2/14/2015</td>
      <td>19:00:00</td>
      <td>cafayate y severo garcia grande de zequeira</td>
      <td>...</td>
      <td>Saturday</td>
      <td>1</td>
      <td>2015-02-14</td>
      <td>7:00</td>
      <td>PM</td>
      <td>33.0</td>
      <td>Windy</td>
      <td>7.0</td>
      <td>19.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>homicidio</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2.0</td>
      <td>2015.0</td>
      <td>2/25/2015</td>
      <td>3:00:00</td>
      <td>lugones, leopoldo av. y udaondo, guillermo av.</td>
      <td>...</td>
      <td>Wednesday</td>
      <td>0</td>
      <td>2015-02-25</td>
      <td>3:00</td>
      <td>AM</td>
      <td>24.0</td>
      <td>Fair</td>
      <td>3.0</td>
      <td>3.0</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
<p>2 rows × 47 columns</p>
</div>





`Agrupamos por hora, estación del año, lugar y estado del clima`


```python
#La columna 'causa' nunca va está vacía, por lo que quedandonos con esa columna, nos aseguramos contar los registros bien
grouped_df = pd.DataFrame(final_df.groupby(['solo_hora', 'Barrio', 'estacion', 'fin_de_semana_dummie', 'FERIADO', 'Condition']).count().causa.reset_index())#.to_csv('prueba.csv')
```


```python
grouped_df.rename(columns={'causa': 'cantidad_accidentes'}, inplace=True)#.sort_values('causa', ascending=False)
```


```python
grouped_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>solo_hora</th>
      <th>Barrio</th>
      <th>estacion</th>
      <th>fin_de_semana_dummie</th>
      <th>FERIADO</th>
      <th>Condition</th>
      <th>cantidad_accidentes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>AGRONOMIA</td>
      <td>invierno</td>
      <td>0</td>
      <td>0.0</td>
      <td>Cloudy</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0</td>
      <td>AGRONOMIA</td>
      <td>invierno</td>
      <td>0</td>
      <td>0.0</td>
      <td>Drizzle</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0</td>
      <td>AGRONOMIA</td>
      <td>invierno</td>
      <td>0</td>
      <td>0.0</td>
      <td>Fair</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0</td>
      <td>AGRONOMIA</td>
      <td>invierno</td>
      <td>0</td>
      <td>0.0</td>
      <td>Fog</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0</td>
      <td>AGRONOMIA</td>
      <td>invierno</td>
      <td>0</td>
      <td>0.0</td>
      <td>Rain</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>




```python
grouped_dummie_df = pd.get_dummies(grouped_df.drop(['cantidad_accidentes'], axis=1).astype(str))
```


```python
#groued_dummie_df['dia/mes'] = grouped_df['dia/mes']
grouped_dummie_df['cantidad_accidentes'] = grouped_df['cantidad_accidentes']
```


```python
grouped_dummie_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>solo_hora_0</th>
      <th>solo_hora_1</th>
      <th>solo_hora_10</th>
      <th>solo_hora_11</th>
      <th>solo_hora_12</th>
      <th>solo_hora_13</th>
      <th>solo_hora_14</th>
      <th>solo_hora_15</th>
      <th>solo_hora_16</th>
      <th>solo_hora_17</th>
      <th>...</th>
      <th>FERIADO_1.0</th>
      <th>Condition_Cloudy</th>
      <th>Condition_Drizzle</th>
      <th>Condition_Fair</th>
      <th>Condition_Fog</th>
      <th>Condition_Rain</th>
      <th>Condition_Storm</th>
      <th>Condition_Volcanic Ash</th>
      <th>Condition_Windy</th>
      <th>cantidad_accidentes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>53702</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>53703</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <th>53704</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>53705</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>53706</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>53707 rows × 90 columns</p>
</div>




```python
data_model_df = grouped_dummie_df.copy()
```

 


```python

```

`Guardamos el dataset que utilizaremos para modelar en un .csv`


```python
#data_model_df = pd.read_csv('dataset_for_model.csv')
```


```python
data_model_df.to_csv('dataset_for_model_VFinal.csv', index=False)
```


```python
#full_df[full_df.comuna.isnull()]
```

 

 

 

 

<hr>
<div id='eda'>
    <h2> EDA </h2>
</div>
<hr>


```python
data_eda = final_df.copy()#pd.read_csv('final_df.csv').drop('Unnamed: 0', axis=1)
```


```python
data_eda.head(3)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>causa</th>
      <th>rol</th>
      <th>tipo</th>
      <th>sexo</th>
      <th>edad</th>
      <th>mes</th>
      <th>periodo</th>
      <th>fecha</th>
      <th>hora</th>
      <th>lugar_hecho</th>
      <th>...</th>
      <th>dia_semana</th>
      <th>fin_de_semana_dummie</th>
      <th>Date</th>
      <th>Hour</th>
      <th>AM/PM</th>
      <th>Wind_Speed</th>
      <th>Condition</th>
      <th>Only_Hour</th>
      <th>Full_Hour</th>
      <th>FERIADO</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>homicidio</td>
      <td>conductor</td>
      <td>moto</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2.0</td>
      <td>2015.0</td>
      <td>2/14/2015</td>
      <td>19:00:00</td>
      <td>cafayate y severo garcia grande de zequeira</td>
      <td>...</td>
      <td>Saturday</td>
      <td>1</td>
      <td>2015-02-14</td>
      <td>7:00</td>
      <td>PM</td>
      <td>33.0</td>
      <td>Windy</td>
      <td>7.0</td>
      <td>19.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>homicidio</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2.0</td>
      <td>2015.0</td>
      <td>2/25/2015</td>
      <td>3:00:00</td>
      <td>lugones, leopoldo av. y udaondo, guillermo av.</td>
      <td>...</td>
      <td>Wednesday</td>
      <td>0</td>
      <td>2015-02-25</td>
      <td>3:00</td>
      <td>AM</td>
      <td>24.0</td>
      <td>Fair</td>
      <td>3.0</td>
      <td>3.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>homicidio</td>
      <td>peaton</td>
      <td>peaton</td>
      <td>femenino</td>
      <td>NaN</td>
      <td>2.0</td>
      <td>2015.0</td>
      <td>2/27/2015</td>
      <td>8:00:00</td>
      <td>avda jujuy y avda independencia</td>
      <td>...</td>
      <td>Friday</td>
      <td>0</td>
      <td>2015-02-27</td>
      <td>8:00</td>
      <td>AM</td>
      <td>20.0</td>
      <td>Cloudy</td>
      <td>8.0</td>
      <td>8.0</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
<p>3 rows × 47 columns</p>
</div>




```python
#Chequeo de Valores Nulos
#Función para calcular el porcentaje de valores nulos de un dataframe
def get_percentages_null_values(df):
    '''
    Obtiene los porcentajes de valores nulos de todas las columnas de un `df`.

    Parameters
    ----------
    df : dataframe del cual se desea conocer los porcentajes de nulos por columna
    '''
    
    null_values_info = df.apply(lambda x: x.isnull().sum()/df.shape[0]*100).sort_values(ascending=False)
    display(null_values_info)
```


```python
solo_accidentes = data_eda[data_eda['causa'].notnull()]
```


```python
get_percentages_null_values(solo_accidentes)
```


    altura                          78.301942
    codigo_cruce                    56.703632
    codigo_calle                    51.305521
    calle2                          25.019069
    lugar_hecho                     21.387080
    tipo_colision1                   3.561580
    tipo                             3.209529
    comuna                           3.191926
    Barrio                           3.186059
    x                                3.186059
    y                                3.186059
    geom                             3.186059
    geom_3857                        3.186059
    geocodificacion                  3.186059
    participantes_victimas           2.775333
    direccion_normalizada_arcgis     2.405680
    calle1                           2.382210
    direccion_normalizada            2.382210
    edad                             2.188582
    rol                              1.496215
    participantes_acusados           1.402335
    sexo                             0.891862
    tipo_calle                       0.000000
    hora                             0.000000
    fecha                            0.000000
    periodo                          0.000000
    mes                              0.000000
    FERIADO                          0.000000
    cantidad_victimas                0.000000
    semestre                         0.000000
    Full_Hour                        0.000000
    Only_Hour                        0.000000
    Condition                        0.000000
    Wind_Speed                       0.000000
    AM/PM                            0.000000
    Hour                             0.000000
    Date                             0.000000
    fin_de_semana_dummie             0.000000
    dia_semana                       0.000000
    estacion                         0.000000
    dia/mes                          0.000000
    fecha_std_datetime               0.000000
    solo_hora                        0.000000
    fecha_std                        0.000000
    dia                              0.000000
    geometry                         0.000000
    causa                            0.000000
    dtype: float64



```python
data_eda_null_info = pd.DataFrame(solo_accidentes.count(), columns=['Non-Null Count'])

data_eda_null_info['Dtype'] = solo_accidentes.dtypes
```


```python
cantidad_registros_totales = len(solo_accidentes['estacion'])
cantidad_registros_totales
```




    17043




```python
data_eda_null_info['Percentage Full'] = 100-(data_eda_null_info['Non-Null Count']/cantidad_registros_totales*100)

data_eda_null_info.sort_values(by='Percentage Full', ascending=False, inplace=True)

data_eda_null_info.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Non-Null Count</th>
      <th>Dtype</th>
      <th>Percentage Full</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>altura</th>
      <td>3698</td>
      <td>float64</td>
      <td>78.301942</td>
    </tr>
    <tr>
      <th>codigo_cruce</th>
      <td>7379</td>
      <td>float64</td>
      <td>56.703632</td>
    </tr>
    <tr>
      <th>codigo_calle</th>
      <td>8299</td>
      <td>float64</td>
      <td>51.305521</td>
    </tr>
    <tr>
      <th>calle2</th>
      <td>12779</td>
      <td>object</td>
      <td>25.019069</td>
    </tr>
    <tr>
      <th>lugar_hecho</th>
      <td>13398</td>
      <td>object</td>
      <td>21.387080</td>
    </tr>
  </tbody>
</table>
</div>




```python
empties_in_final_df_agrupado = data_eda_null_info[data_eda_null_info['Percentage Full'] >= 0.0]
```


```python
clrs=[]
for x in empties_in_final_df_agrupado['Percentage Full']:
    if x > 60:
        clrs.append('#C70039')
    elif x > 20:
        clrs.append('#FF5733')
    elif x > 10:
        clrs.append('#FFC300')
    else:
        clrs.append('#DAF7A6')
```


```python
fig, ax = plt.subplots(figsize=(20,8))
#plt.rcParams.update({'font.size': 14})
plt.xticks(rotation=45)
plt.tight_layout()
ax.set_title('Distribución de registros nulos por columnas', fontweight='bold', fontsize=18)
ax.set_xlabel('Columnas del dataset Siniestros', fontweight='bold', fontsize=14)
ax.set_ylabel('Cantidad de registros', fontweight='bold', fontsize=14)
#ax.set_yticklabels(['{:,.0%}'.format(x) for x in ax.get_yticks()])
ax.bar(empties_in_final_df_agrupado.index, empties_in_final_df_agrupado['Percentage Full'], data=empties_in_final_df_agrupado, color=clrs)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.text(0.7, 0.95, 'Figura 1.\n Distribución de variables nulas en el dataset', transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox= dict(boxstyle='round', facecolor='wheat', alpha=0.5))
#ax.set_xticklabels(info_properatti_df.index, rotation=45)
#plt.savefig('datos_nulos')

```




    Text(0.7, 0.95, 'Figura 1.\n Distribución de variables nulas en el dataset')




![png](output_134_1.png)


 

 


```python
siniestros_df['solo_hora'] = siniestros_df['solo_hora'].astype(int)
```


```python
def plot_variable_years(years_list, dataframe, column_groupby, column_count, title, x_axis_title, y_axis_title, kind='Normal', shareX_option=False, shareY_opcion=True):
    '''
    Grafica una cantidad de visualizaciones según la cantidad de años y las variables utilizadas.
    
    Parameters
    ----------
    years_list : debe ser una lista con los años a través de los cuales se desea graficar. Dependiendo de la longitud de `years_list` va a cambiar la cantidad de gráficos logrados.
    
    dataframe : datos a partir del cual se van a agrupar y contar los datos.
    
    column_groupby : columna por la cual se desea agrupar.
    
    column_count : columna que sea desea contar.
    
    title : titulo del gráfico. Si no se pasa como dato, la visualización no tendrá título.
    
    x_axis_title : título del eje X. Si no se pasa como dato, cada gráfico no tendrá su correspondiente título para el eje x.
    
    y_axis_title : título del eje Y. Si no se pasa como dato, cada gráfico no tendrá su correspondiente título para el eje y.
    
    kind : `plot_variable_years` permite graficar 2 tipos de visualizaciones: barras o geoespacial. Si se omite, se utilizará por defecto `Normal` y se graficarán barras; de lo contrario se graficarán -de ser posible-, los datos geoespaciales.
    '''
    
    
    fig, axes = plt.subplots(2, 2, figsize=(15,10), sharex=False, sharey=True)
    fig.suptitle(title, fontsize='18')
    i=0
    j=0
    for y in years_list:
        acc_year = dataframe[dataframe.periodo==y]
        if kind != 'Geo':
            df = pd.DataFrame(acc_year.groupby(column_groupby)[column_count].count()).reset_index()
        else:
            acc_barrios = acc_year.groupby('Barrio').causa.count().sort_values(ascending=False)
            acc_barrios = barrios.merge(acc_barrios, how='left', left_on='barrio', right_on=acc_barrios.index)
        #print(y)
        #display(df.head(2))
        if y == years_list[0]:
            i=0
            j=0
        elif y == years_list[1]:
            i=0
            j=1
        elif y == years_list[2]:
            i=1
            j=0
        else:
            i=1
            j=1
        #print(i, j)
        if kind != 'Geo':
            sns.barplot(x=column_groupby, y=column_count,data=df, ax=axes[i, j])
        else:
            acc_barrios.plot('causa', figsize=(10,10), legend=True, ax=axes[i,j], vmin=0, vmax=800)

    
        
        axes[i, j].set_title(y)
        axes[i, j].set_xlabel(x_axis_title)
        axes[i, j].set_ylabel(y_axis_title)
        axes[1,1].text(0.3, 0.9, '*Información del año incompleta', horizontalalignment='center', verticalalignment='center', transform=axes[1,1].transAxes)
    
    
    plt.show()

```

 

> Vemos en el siguiente gráfico que muestra la `Distribución de accidentes por DÍA para cada año`, que los días no son una variable que aporten valor a la cantidad de accidentes. Por ende, es probable que esta variable sea removida para modelar.


```python
plot_variable_years(list(siniestros_df.periodo.unique()), siniestros_df, 'dia', 'causa', 'Disttribución de accidentes por dia',\
                    'Dia', 'Cantidad de accidentes', kind='Normal')
```


![png](output_141_0.png)


 

> A diferencia de la anterior visualización, en el siguiente gráfico que muestra la `Distribución de accidentes por HORA para cada año`, esta variable sí influye en la cantidad de accidentes. 

> Hay una clara tendencia a lo largo de los años que la cantidad de accidentes sub cerca del mediodía, teniendo picos por las tardes.


```python
plot_variable_years(list(siniestros_df.periodo.unique()), siniestros_df, 'solo_hora', 'causa', 'Disttribución de accidentes por hora',\
                    'Hora', 'Cantidad de accidentes', kind='Normal')
```


![png](output_144_0.png)


 

> Vemos en el siguiente gráfico que muestra la `Distribución de accidentes por MES para cada año`, al igual que los "días" no es una variable que incluye en la cantidad de accidentes. Por ende, es probable que los mismos sean removidos para modelar.


```python
plot_variable_years(list(siniestros_df.periodo.unique()), siniestros_df, 'mes', 'causa', 'Disttribución de accidentes por mes',\
                    'Mes', 'Cantidad de accidentes', kind='Normal')
```


![png](output_147_0.png)



```python

```


```python
grouped_final_df_agrupado = pd.DataFrame(grouped_df.groupby(['estacion']).sum()['cantidad_accidentes'])
Estacion=grouped_final_df_agrupado.index.values.tolist()
grouped_final_df_agrupado['Estacion']=Estacion
fig, ax=plt.subplots()
sns.barplot(x='Estacion',y='cantidad_accidentes',data=grouped_final_df_agrupado, ax=ax)
ax.set_title('Cantidad de accidente por estación')
```




    Text(0.5, 1.0, 'Cantidad de accidente por estación')




![png](output_149_1.png)



```python

```

> En la siguiente visualización se puede ver cómo la localización influye en la cantidad de accidentes. Los barrios Palermo, Flores, Recoleta es donde ocurren a lo largo de los años mayor cantidad de accidentes.


```python
plot_variable_years(list(siniestros_df.periodo.unique()), siniestros_df, 'Barrio', 'causa', 'Disttribución de accidentes por Barrio',\
                    'Barrio', 'Cantidad de accidentes', kind='Geo')
```


![png](output_152_0.png)



```python
feriados['FECHA_std'] = feriados['FECHA'].apply(lambda f: pd.to_datetime(f))
```


```python
siniestros_df['fecha_std'] = siniestros_df['fecha_std'].apply(lambda f: pd.to_datetime(f))
```


```python
feriados.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>FECHA</th>
      <th>FERIADO</th>
      <th>FECHA_std</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2015-01-01</td>
      <td>1</td>
      <td>2015-01-01</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2016-01-01</td>
      <td>1</td>
      <td>2016-01-01</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2017-01-01</td>
      <td>1</td>
      <td>2017-01-01</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2018-01-01</td>
      <td>1</td>
      <td>2018-01-01</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2015-04-02</td>
      <td>1</td>
      <td>2015-04-02</td>
    </tr>
  </tbody>
</table>
</div>




```python
siniestros_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>causa</th>
      <th>rol</th>
      <th>tipo</th>
      <th>sexo</th>
      <th>edad</th>
      <th>mes</th>
      <th>periodo</th>
      <th>fecha</th>
      <th>hora</th>
      <th>lugar_hecho</th>
      <th>...</th>
      <th>comuna</th>
      <th>geom_3857</th>
      <th>tipo_colision1</th>
      <th>participantes_victimas</th>
      <th>participantes_acusados</th>
      <th>geometry</th>
      <th>Barrio</th>
      <th>dia</th>
      <th>fecha_std</th>
      <th>solo_hora</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>homicidio</td>
      <td>conductor</td>
      <td>moto</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2</td>
      <td>2015</td>
      <td>2/14/2015</td>
      <td>19:00:00</td>
      <td>cafayate y severo garcia grande de zequeira</td>
      <td>...</td>
      <td>9.0</td>
      <td>0101000020110F0000DE9B958180D858C1EC802966CD68...</td>
      <td>motovehiculo - vehiculo</td>
      <td>moto</td>
      <td>automovil</td>
      <td>POINT (-58.50866 -34.65349)</td>
      <td>MATADEROS</td>
      <td>14</td>
      <td>2015-02-14</td>
      <td>19</td>
    </tr>
    <tr>
      <th>1</th>
      <td>homicidio</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2</td>
      <td>2015</td>
      <td>2/25/2015</td>
      <td>3:00:00</td>
      <td>lugones, leopoldo av. y udaondo, guillermo av.</td>
      <td>...</td>
      <td>13.0</td>
      <td>0101000020110F0000BFBC457BDFD158C1E1DDA818C14B...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>POINT (-58.44768 -34.54351)</td>
      <td>BELGRANO</td>
      <td>25</td>
      <td>2015-02-25</td>
      <td>3</td>
    </tr>
    <tr>
      <th>2</th>
      <td>homicidio</td>
      <td>peaton</td>
      <td>peaton</td>
      <td>femenino</td>
      <td>NaN</td>
      <td>2</td>
      <td>2015</td>
      <td>2/27/2015</td>
      <td>8:00:00</td>
      <td>avda jujuy y avda independencia</td>
      <td>...</td>
      <td>3.0</td>
      <td>0101000020110F0000F8067D6812CD58C189755F66A55F...</td>
      <td>peaton - vehiculo</td>
      <td>peaton</td>
      <td>"transporte publico"</td>
      <td>POINT (-58.40352 -34.61884)</td>
      <td>BALVANERA</td>
      <td>27</td>
      <td>2015-02-27</td>
      <td>8</td>
    </tr>
    <tr>
      <th>3</th>
      <td>homicidio</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>3</td>
      <td>2015</td>
      <td>03/02/15</td>
      <td>18:30:00</td>
      <td>lavalle 1730</td>
      <td>...</td>
      <td>1.0</td>
      <td>0101000020110F00005621683DBFCB58C10B59E69B815B...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>POINT (-58.39133 -34.60317)</td>
      <td>SAN NICOLAS</td>
      <td>02</td>
      <td>2015-03-02</td>
      <td>18</td>
    </tr>
    <tr>
      <th>4</th>
      <td>homicidio</td>
      <td>pasajero</td>
      <td>camion</td>
      <td>masculino</td>
      <td>NaN</td>
      <td>4</td>
      <td>2015</td>
      <td>04/09/15</td>
      <td>1:20:00</td>
      <td>ave salvador m del carril 2434</td>
      <td>...</td>
      <td>15.0</td>
      <td>0101000020110F00006F2F76D4C9D658C1750825735D57...</td>
      <td>vehiculo - vehiculo</td>
      <td>camion</td>
      <td>camion</td>
      <td>POINT (-58.49290 -34.58749)</td>
      <td>AGRONOMIA</td>
      <td>09</td>
      <td>2015-04-09</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 34 columns</p>
</div>




```python
siniestros_feriados=pd.merge(siniestros_df,feriados,how='left', left_on="fecha_std", right_on="FECHA_std")
```


```python
siniestros_feriados['feriado_dummie'] = siniestros_feriados.FERIADO.apply(lambda f: 0 if pd.isna(f) else 1)
```


```python
cantidad_no_feriados = len(siniestros_feriados[siniestros_feriados['feriado_dummie']==0].fecha_std.unique())
cantidad_feriados = len(siniestros_feriados[siniestros_feriados['feriado_dummie']==1].fecha_std.unique())
```


```python
print('Cantidad No Feriados -->', cantidad_no_feriados)
print('Cantidad Feriados -->', cantidad_feriados)
```

    Cantidad No Feriados --> 1223
    Cantidad Feriados --> 24



```python
siniestros_feriados=siniestros_feriados.feriado_dummie.value_counts()
siniestros_feriados
```




    0    32744
    1      418
    Name: feriado_dummie, dtype: int64




```python
print('Ratio Accidentes dia habil -->', siniestros_feriados.iloc[0]/cantidad_no_feriados)
print('Ratio Accidentes dia feriado -->', siniestros_feriados.iloc[1]/cantidad_feriados)
ratios=[siniestros_feriados.iloc[0]/cantidad_no_feriados,siniestros_feriados.iloc[1]/cantidad_feriados ]
```

    Ratio Accidentes dia habil --> 26.77350776778414
    Ratio Accidentes dia feriado --> 17.416666666666668



```python
fig, ax = plt.subplots()
sns.barplot(x=['Hábil', 'Feriado'],y=ratios, ax=ax, palette='Paired_r')
ax.set_title("Ratio de accidentes según tipo de día")
```




    Text(0.5, 1.0, 'Ratio de accidentes según tipo de día')




![png](output_163_1.png)



```python

```


```python
fig, ax = plt.subplots(2,2, figsize=(15,9))
causas_count = siniestros_df.causa.value_counts().reset_index()
ax[0,0].set_title('Cantidad de Lesiones vs Homicidios')
sns.barplot(x=causas_count['index'], y=causas_count['causa'], data=causas_count, ax=ax[0,0])

roles_count = siniestros_df[siniestros_df.causa=='homicidio'].rol.value_counts().reset_index()
roles_count=roles_count[roles_count['index'].isin(['conductor', 'peaton', 'pasajero', 'ciclista'])]
ax[0,1].set_title('Cantidad de `roles` fallecidos')
sns.barplot(x=roles_count['index'], y=roles_count['rol'], data=roles_count, ax=ax[0,1])

tipos_count=siniestros_df[siniestros_df.causa=='homicidio'].tipo.value_counts().reset_index()
tipos_count=tipos_count[tipos_count['tipo']>3]
ax[1,0].set_title('Cantidad de `tipo` fallecidos')
sns.barplot(x=tipos_count['index'], y=tipos_count['tipo'], data=tipos_count, ax=ax[1,0])


sexo_count = siniestros_df.sexo.value_counts().reset_index()
ax[1,1].set_title('Cantidad de `genero` fallecidos')
sns.barplot(x=sexo_count['index'], y=sexo_count['sexo'], data=sexo_count, ax=ax[1,1])
```




    <AxesSubplot:title={'center':'Cantidad de `genero` fallecidos'}, xlabel='index', ylabel='sexo'>




![png](output_165_1.png)



```python

```


```python

```

<hr>
<div id='modelado'>
    <h2> Modelado </h2>
</div>
<hr>

El primer paso de nuestro modelado va a ser entrenar 5 modelos de regresión "simples", sin modificar sus hiperparámetros:

* LinearRegression
* KNeighborsRegressor
* DecisionTreeRegressor
* AdaBoostRegressor
* GradientBoostingRegressor

Luego de entrenar cada modelo, lo que vamos a realizar es un Grid Search + Cross Validation sobre cada modelo base, para encontrar la mejor performance de cada modelo y así quedarnos el mejor.


```python
data_model_df=pd.read_csv('dataset_for_model_VFinal.csv')
```


```python
from sklearn.ensemble import GradientBoostingRegressor, AdaBoostRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.metrics import mean_squared_error, r2_score
```


```python
X = data_model_df.drop('cantidad_accidentes', axis=1)
y = data_model_df.cantidad_accidentes
```


```python
print(X.shape)
print(y.shape)
```

    (53707, 89)
    (53707,)



```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
```


```python
print('Shapes en train')
print('X_train --> ',X_train.shape)
print('y_train --> ',y_train.shape,'\n')
print('Shapes en test')
print('X_test --> ',X_test.shape)
print('y_test --> ',y_test.shape)
```

    Shapes en train
    X_train -->  (40280, 89)
    y_train -->  (40280,) 
    
    Shapes en test
    X_test -->  (13427, 89)
    y_test -->  (13427,)



```python

```


```python
xgboost_simple = GradientBoostingRegressor()
adaboost_simple = AdaBoostRegressor()
linear_simple = LinearRegression()
knn_simple = KNeighborsRegressor()
tree_simple = DecisionTreeRegressor()
```


```python
simple_models = [knn_simple, linear_simple, tree_simple, xgboost_simple, adaboost_simple]
```


```python
simple_results = {}
```


```python
for model in simple_models:
    print('======'+str(model)+'======')
        
    print('Fiteando ', str(model), '...')
    model.fit(X_train, y_train)
    print(model, 'fiteado!')
    
    print('Realizando predicciones de ', str(model), '...')
    y_pred = model.predict(X_test)
    print('Predicciones para ', str(model), 'realizadas')
    
    mse = mean_squared_error(y_test, y_pred)
    r2score = r2_score(y_test, y_pred)
    
    model_scores = {'R^2 Score': r2score, 'MSE Score': mse}
    
    print('MSE de '+str(model)+' es de: ', mse)
    print('R^2 de '+str(model)+' es de: ', r2score)
    
    model_dict = {str(model): model_scores}
    
    simple_results.update(model_dict)
    
    #simple_results[str(model)]['R^2 Score'] = r2score
    #simple_results[str(model)]['MSE Score'] = mse
        
    print('\n-----------\n')
```

    ======KNeighborsRegressor()======
    Fiteando  KNeighborsRegressor() ...
    KNeighborsRegressor() fiteado!
    Realizando predicciones de  KNeighborsRegressor() ...
    Predicciones para  KNeighborsRegressor() realizadas
    MSE de KNeighborsRegressor() es de:  0.7255678856036345
    R^2 de KNeighborsRegressor() es de:  0.3022825736462387
    
    -----------
    
    ======LinearRegression()======
    Fiteando  LinearRegression() ...
    LinearRegression() fiteado!
    Realizando predicciones de  LinearRegression() ...
    Predicciones para  LinearRegression() realizadas
    MSE de LinearRegression() es de:  0.7884816199356867
    R^2 de LinearRegression() es de:  0.24178374276986314
    
    -----------
    
    ======DecisionTreeRegressor()======
    Fiteando  DecisionTreeRegressor() ...
    DecisionTreeRegressor() fiteado!
    Realizando predicciones de  DecisionTreeRegressor() ...
    Predicciones para  DecisionTreeRegressor() realizadas
    MSE de DecisionTreeRegressor() es de:  0.9046696953898861
    R^2 de DecisionTreeRegressor() es de:  0.13005547228355618
    
    -----------
    
    ======GradientBoostingRegressor()======
    Fiteando  GradientBoostingRegressor() ...
    GradientBoostingRegressor() fiteado!
    Realizando predicciones de  GradientBoostingRegressor() ...
    Predicciones para  GradientBoostingRegressor() realizadas
    MSE de GradientBoostingRegressor() es de:  0.670722906477934
    R^2 de GradientBoostingRegressor() es de:  0.3550223633244629
    
    -----------
    
    ======AdaBoostRegressor()======
    Fiteando  AdaBoostRegressor() ...
    AdaBoostRegressor() fiteado!
    Realizando predicciones de  AdaBoostRegressor() ...
    Predicciones para  AdaBoostRegressor() realizadas
    MSE de AdaBoostRegressor() es de:  1.107229046830434
    R^2 de AdaBoostRegressor() es de:  -0.06472876799936045
    
    -----------
    



```python
simple_models_df = pd.DataFrame(simple_results).transpose().sort_values(by='R^2 Score', ascending=False)
```


```python
simple_models_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>R^2 Score</th>
      <th>MSE Score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>GradientBoostingRegressor()</th>
      <td>0.355022</td>
      <td>0.670723</td>
    </tr>
    <tr>
      <th>KNeighborsRegressor()</th>
      <td>0.302283</td>
      <td>0.725568</td>
    </tr>
    <tr>
      <th>LinearRegression()</th>
      <td>0.241784</td>
      <td>0.788482</td>
    </tr>
    <tr>
      <th>DecisionTreeRegressor()</th>
      <td>0.130055</td>
      <td>0.904670</td>
    </tr>
    <tr>
      <th>AdaBoostRegressor()</th>
      <td>-0.064729</td>
      <td>1.107229</td>
    </tr>
  </tbody>
</table>
</div>




```python

```


```python
linear_params = {'fit_intercept': [True, False], 'normalize': [False, True]}
```


```python
knn_params = {'metric': ['minkowski', 'euclidean', 'chebyshev'],
             'n_neighbors': range(10,20),
             'weights': ['uniform', 'distance']}
```


```python
xgboost_params = {'learning_rate': [0.01, 0.1, 1.0],
                     'max_depth': [1, 3, 5],
                     'n_estimators': [100, 500, 750, 1000],
                 'max_features': [9, None]}
```


```python
adaboost_params = {'base_estimator': [None, tree_simple],
                'loss': ['linear', 'exponential'],
                     'n_estimators': [100, 500, 1000],
                  'learning_rate': [0.01, 0.1, 1.0]}
```


```python
tree_params = {
               'min_samples_split': range(2, 10),
               'max_depth': [1, 3, None]
                }
```


```python
models_params = {'LinearRegression()': linear_params,
                'KNeighborsRegressor()': knn_params,
                 'DecisionTreeRegressor()': tree_params,
                 'GradientBoostingRegressor()':xgboost_params,
                 'AdaBoostRegressor()': adaboost_params}
```


```python

```


```python
models_grid_dict = {}
```


```python
for model in simple_models:
    print('======'+str(model)+'======')
    
    folds = StratifiedKFold(n_splits=5, shuffle=True)
    
    grid_model = GridSearchCV(model, param_grid=models_params[str(model)], verbose=2, n_jobs=-1, scoring='r2', cv=folds)
        
    print('Fiteando ', str(model), '...')
    #display(model)
    #display(models_params[str(model)])
    grid_model.fit(X_train, y_train)
    print(model, 'fiteado!')
    
    best_estimator = grid_model.best_estimator_
    best_params = grid_model.best_params_
    
    print('Realizando predicciones de ', str(model), '...')
    y_pred = best_estimator.predict(X_test)
    print('Predicciones para ', str(model), 'realizadas')
    
    mse = mean_squared_error(y_test, y_pred)
    r2score = r2_score(y_test, y_pred)
    
    model_scores = {'R^2 Score': r2score, 'MSE Score': mse}
    
    model_results = {}
    model_results.update(model_scores)
    #display(model_results)
    #display(dict(best_params))
    model_results['Best params'] = (dict(best_params))
    #display(model_results)
    
    print('MSE de '+str(model)+' es de: ', mse)
    print('R^2 de '+str(model)+' es de: ', r2score)
    
   # models_grid_dict = {str(model): model_scores}
    models_grid_dict[str(model)] = model_results
    #models_grid_dict.update(model_results)
    #display(models_grid_dict)
    
    #simple_results[str(model)]['R^2 Score'] = r2score
    #simple_results[str(model)]['MSE Score'] = mse
        
    print('\n-----------\n')
```

    ======KNeighborsRegressor()======
    Fiteando  KNeighborsRegressor() ...
    Fitting 5 folds for each of 60 candidates, totalling 300 fits


    /Users/bpeco/opt/anaconda3/lib/python3.8/site-packages/sklearn/model_selection/_split.py:670: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      warnings.warn(("The least populated class in y has only %d"
    [Parallel(n_jobs=-1)]: Using backend LokyBackend with 8 concurrent workers.
    [Parallel(n_jobs=-1)]: Done  25 tasks      | elapsed:  4.6min
    [Parallel(n_jobs=-1)]: Done 146 tasks      | elapsed: 20.6min
    [Parallel(n_jobs=-1)]: Done 300 out of 300 | elapsed: 44.0min finished


    KNeighborsRegressor() fiteado!
    Realizando predicciones de  KNeighborsRegressor() ...
    Predicciones para  KNeighborsRegressor() realizadas
    MSE de KNeighborsRegressor() es de:  0.5707646167941679
    R^2 de KNeighborsRegressor() es de:  0.4511438179873285
    
    -----------
    
    ======LinearRegression()======
    Fiteando  LinearRegression() ...
    Fitting 5 folds for each of 4 candidates, totalling 20 fits


    /Users/bpeco/opt/anaconda3/lib/python3.8/site-packages/sklearn/model_selection/_split.py:670: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      warnings.warn(("The least populated class in y has only %d"
    [Parallel(n_jobs=-1)]: Using backend LokyBackend with 8 concurrent workers.
    [Parallel(n_jobs=-1)]: Done  16 out of  20 | elapsed:    1.0s remaining:    0.3s
    [Parallel(n_jobs=-1)]: Done  20 out of  20 | elapsed:    1.1s finished


    LinearRegression() fiteado!
    Realizando predicciones de  LinearRegression() ...
    Predicciones para  LinearRegression() realizadas
    MSE de LinearRegression() es de:  0.7884816199356867
    R^2 de LinearRegression() es de:  0.24178374276986314
    
    -----------
    
    ======DecisionTreeRegressor()======
    Fiteando  DecisionTreeRegressor() ...
    Fitting 5 folds for each of 24 candidates, totalling 120 fits


    /Users/bpeco/opt/anaconda3/lib/python3.8/site-packages/sklearn/model_selection/_split.py:670: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      warnings.warn(("The least populated class in y has only %d"
    [Parallel(n_jobs=-1)]: Using backend LokyBackend with 8 concurrent workers.
    [Parallel(n_jobs=-1)]: Done  34 tasks      | elapsed:    0.7s
    [Parallel(n_jobs=-1)]: Done 120 out of 120 | elapsed:    6.9s finished


    DecisionTreeRegressor() fiteado!
    Realizando predicciones de  DecisionTreeRegressor() ...
    Predicciones para  DecisionTreeRegressor() realizadas
    MSE de DecisionTreeRegressor() es de:  0.7989477304166125
    R^2 de DecisionTreeRegressor() es de:  0.23171936724611664
    
    -----------
    
    ======GradientBoostingRegressor()======
    Fiteando  GradientBoostingRegressor() ...
    Fitting 5 folds for each of 72 candidates, totalling 360 fits


    /Users/bpeco/opt/anaconda3/lib/python3.8/site-packages/sklearn/model_selection/_split.py:670: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      warnings.warn(("The least populated class in y has only %d"
    [Parallel(n_jobs=-1)]: Using backend LokyBackend with 8 concurrent workers.
    [Parallel(n_jobs=-1)]: Done  25 tasks      | elapsed:   10.1s
    [Parallel(n_jobs=-1)]: Done 146 tasks      | elapsed:  6.8min
    [Parallel(n_jobs=-1)]: Done 360 out of 360 | elapsed: 19.6min finished


    GradientBoostingRegressor() fiteado!
    Realizando predicciones de  GradientBoostingRegressor() ...
    Predicciones para  GradientBoostingRegressor() realizadas
    MSE de GradientBoostingRegressor() es de:  0.5163480649960794
    R^2 de GradientBoostingRegressor() es de:  0.5034716252469091
    
    -----------
    
    ======AdaBoostRegressor()======
    Fiteando  AdaBoostRegressor() ...
    Fitting 5 folds for each of 36 candidates, totalling 180 fits


    /Users/bpeco/opt/anaconda3/lib/python3.8/site-packages/sklearn/model_selection/_split.py:670: UserWarning: The least populated class in y has only 1 members, which is less than n_splits=5.
      warnings.warn(("The least populated class in y has only %d"
    [Parallel(n_jobs=-1)]: Using backend LokyBackend with 8 concurrent workers.
    [Parallel(n_jobs=-1)]: Done  25 tasks      | elapsed:  8.8min
    [Parallel(n_jobs=-1)]: Done 146 tasks      | elapsed: 73.0min
    [Parallel(n_jobs=-1)]: Done 180 out of 180 | elapsed: 110.5min finished


    AdaBoostRegressor() fiteado!
    Realizando predicciones de  AdaBoostRegressor() ...
    Predicciones para  AdaBoostRegressor() realizadas
    MSE de AdaBoostRegressor() es de:  0.7595144112608923
    R^2 de AdaBoostRegressor() es de:  0.269639063665737
    
    -----------
    



```python
models_grid_df = pd.DataFrame(models_grid_dict).transpose()
```


```python
models_grid_df.sort_values(by='R^2 Score', ascending=False, inplace=True)
```


```python
models_grid_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>R^2 Score</th>
      <th>MSE Score</th>
      <th>Best params</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>GradientBoostingRegressor()</th>
      <td>0.503472</td>
      <td>0.516348</td>
      <td>{'learning_rate': 0.1, 'max_depth': 5, 'max_fe...</td>
    </tr>
    <tr>
      <th>KNeighborsRegressor()</th>
      <td>0.451144</td>
      <td>0.570765</td>
      <td>{'metric': 'minkowski', 'n_neighbors': 19, 'we...</td>
    </tr>
    <tr>
      <th>AdaBoostRegressor()</th>
      <td>0.269639</td>
      <td>0.759514</td>
      <td>{'base_estimator': DecisionTreeRegressor(), 'l...</td>
    </tr>
    <tr>
      <th>LinearRegression()</th>
      <td>0.241784</td>
      <td>0.788482</td>
      <td>{'fit_intercept': True, 'normalize': False}</td>
    </tr>
    <tr>
      <th>DecisionTreeRegressor()</th>
      <td>0.231719</td>
      <td>0.798948</td>
      <td>{'max_depth': None, 'min_samples_split': 9}</td>
    </tr>
  </tbody>
</table>
</div>




```python

```

# poner un grafico/df sobre el mejor modelo comparando y_test e y_pred


```python
models_grid_df['Best params'].iloc[0]
```




    {'learning_rate': 0.1, 'max_depth': 5, 'max_features': 9, 'n_estimators': 1000}




```python
xgboost_FINAL = GradientBoostingRegressor(learning_rate=0.1, max_depth=5, max_features=9, n_estimators=1000)
```


```python
xgboost_FINAL.fit(X_train, y_train)
```




    GradientBoostingRegressor(max_depth=5, max_features=9, n_estimators=1000)




```python
y_pred_final = xgboost_FINAL.predict(X_test)
print('Predicciones para ', str(xgboost_FINAL), 'realizadas')
```

    Predicciones para  GradientBoostingRegressor(max_depth=5, max_features=9, n_estimators=1000) realizadas



```python
df_comparacion = pd.DataFrame(list(zip(y_test,y_pred_final.astype(int))), columns=["Test","Predic"])
```


```python
df_comparacion['diferencia'] = df_comparacion['Test']- df_comparacion['Predic']
```


```python
df_comparacion
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Test</th>
      <th>Predic</th>
      <th>diferencia</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>13422</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>13423</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>13424</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>13425</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>13426</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>13427 rows × 3 columns</p>
</div>




```python
plt.figure(figsize = (15,8))
df_comparacion[['diferencia']].sample(100).reset_index(drop=True).plot(style=['o','rx'])
```




    <AxesSubplot:>




    <Figure size 1080x576 with 0 Axes>



![png](output_205_2.png)



```python

```


```python
with open('best_xgboos_model_final.pkl', 'wb') as pickle_model:
    pickle.dump(xgboost_FINAL, pickle_model)
```


```python

```


```python

```
