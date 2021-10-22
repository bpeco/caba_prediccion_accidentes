{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "from flask import Flask, render_template, request\n",
    "import pickle\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "from datetime import datetime, date\n",
    "import geopandas as gpd\n",
    "import matplotlib.pyplot as plt\n",
    "#%matplotlib inline"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "with open('model/best_xgboos_model_final.pkl', 'rb') as f:\n",
    "    model = pickle.load(f)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "app = Flask(__name__, template_folder='templates')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Importamos DF Barrios\n",
    "barrios = gpd.read_file(\"barrios.csv\")\n",
    "\n",
    "\n",
    "def from_wkt(dataframe, wkt_column):\n",
    "    import shapely.wkt\n",
    "    dataframe[\"coordenadas\"]= dataframe[wkt_column].apply(shapely.wkt.loads)\n",
    "    geo_barrios = gpd.GeoDataFrame(dataframe, geometry='coordenadas')\n",
    "    return geo_barrios\n",
    "\n",
    "# change geometry\n",
    "barrios = from_wkt(barrios, \"WKT\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "geopandas.geodataframe.GeoDataFrame"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import shapely.wkt\n",
    "barrios[\"WKT\"] = barrios[\"WKT\"].apply(shapely.wkt.loads) \n",
    "barrios = gpd.GeoDataFrame(barrios, geometry='WKT')\n",
    "type(barrios)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "barrios['color'] = '#CECECE'"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "#barrios.plot(color=barrios['color'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "def obtener_estacion(fecha):\n",
    "    if isinstance(fecha, datetime):\n",
    "        fecha = fecha.date()\n",
    "        \n",
    "    #print(fecha.day==29)\n",
    "    #print(fecha.month==2)\n",
    "    if fecha.day == 29 and fecha.month == 2:\n",
    "        #print(fecha)\n",
    "        fecha = fecha - timedelta(1)\n",
    "        #print(fecha)\n",
    "        \n",
    "    fecha = fecha.replace(year=Y) #reemplaza cualquier año por el 2015 (o lo definido en la variable Y)\n",
    "    return next(estacion for estacion, (empieza, termina) in estaciones\n",
    "                if empieza <= fecha <= termina)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "Y = 2021\n",
    "estaciones = [('verano', (date(Y,  1,  1),  date(Y,  3, 20))),\n",
    "       ('otoño', (date(Y,  3, 21),  date(Y,  6, 20))),\n",
    "       ('invierno', (date(Y,  6, 21),  date(Y,  9, 22))),\n",
    "       ('primavera', (date(Y,  9, 23),  date(Y, 12, 20))),\n",
    "       ('verano', (date(Y, 12, 21),  date(Y, 12, 31)))]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [],
   "source": [
    "map_weather_spanish={\n",
    "'Nublado': 'Cloudy',\n",
    "'Llovizna': 'Drizzle',\n",
    "'Normal': 'Fair',\n",
    "'Nieblina': 'Fog',\n",
    "'Lluvia': 'Rain',\n",
    "'Tormenta': 'Storm',\n",
    "'Ceniza Volcánica': 'Volcanic Ash',\n",
    "'Viento': 'Windy'\n",
    "}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [],
   "source": [
    "def col_fds_dummie(fecha):\n",
    "    if fecha.strftime('%A') in ['Saturday', 'Sunday']:\n",
    "        dummie_fds = '1'\n",
    "    else:\n",
    "        dummie_fds = '0'\n",
    "    \n",
    "    return 'fin_de_semana_dummie_'+dummie_fds"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [],
   "source": [
    "def barrio_jpg(barrios_df, barrio):\n",
    "    #print(barrio)\n",
    "    n=0\n",
    "    for index, row in barrios_df.iterrows():\n",
    "        if row['barrio'] == barrio:\n",
    "            barrios_df.loc[n, 'color']='#FF7070'\n",
    "        n+=1\n",
    "    fig, axes=plt.subplots()\n",
    "    barrios_df.plot(color=barrios_df['color'], ax=axes)\n",
    "    axes.get_xaxis().set_ticks([])\n",
    "    axes.get_yaxis().set_ticks([])\n",
    "    plt.axis('off')\n",
    "    plt.savefig('static/caba_new.jpg')\n",
    "    #print(barrio+'.jpg', ' guardado exitosamente')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [],
   "source": [
    "def analyze_results(results):\n",
    "    all_columns = ['solo_hora_0','solo_hora_1','solo_hora_10','solo_hora_11','solo_hora_12','solo_hora_13','solo_hora_14','solo_hora_15','solo_hora_16','solo_hora_17','solo_hora_18','solo_hora_19','solo_hora_2','solo_hora_20','solo_hora_21','solo_hora_22','solo_hora_23','solo_hora_3','solo_hora_4','solo_hora_5','solo_hora_6','solo_hora_7','solo_hora_8','solo_hora_9','Barrio_AGRONOMIA','Barrio_ALMAGRO','Barrio_BALVANERA','Barrio_BARRACAS','Barrio_BELGRANO','Barrio_BOCA','Barrio_BOEDO','Barrio_CABALLITO','Barrio_CHACARITA','Barrio_COGHLAN','Barrio_COLEGIALES','Barrio_CONSTITUCION','Barrio_FLORES','Barrio_FLORESTA','Barrio_LINIERS','Barrio_MATADEROS','Barrio_MONSERRAT','Barrio_MONTE CASTRO','Barrio_NUEVA POMPEYA','Barrio_NUÃ‘EZ','Barrio_NUÑEZ','Barrio_PALERMO','Barrio_PARQUE AVELLANEDA','Barrio_PARQUE CHACABUCO','Barrio_PARQUE CHAS','Barrio_PARQUE PATRICIOS','Barrio_PATERNAL','Barrio_PUERTO MADERO','Barrio_RECOLETA','Barrio_RETIRO','Barrio_SAAVEDRA','Barrio_SAN CRISTOBAL','Barrio_SAN NICOLAS','Barrio_SAN TELMO','Barrio_VELEZ SARSFIELD','Barrio_VERSALLES','Barrio_VILLA CRESPO','Barrio_VILLA DEL PARQUE','Barrio_VILLA DEVOTO','Barrio_VILLA GRAL. MITRE','Barrio_VILLA LUGANO','Barrio_VILLA LURO','Barrio_VILLA ORTUZAR','Barrio_VILLA PUEYRREDON','Barrio_VILLA REAL','Barrio_VILLA RIACHUELO','Barrio_VILLA SANTA RITA','Barrio_VILLA SOLDATI','Barrio_VILLA URQUIZA','estacion_invierno','estacion_otoño','estacion_primavera','estacion_verano','fin_de_semana_dummie_0','fin_de_semana_dummie_1','FERIADO_0.0','FERIADO_1.0','Condition_Cloudy','Condition_Drizzle','Condition_Fair','Condition_Fog','Condition_Rain','Condition_Storm','Condition_Windy', 'Condition_Volcanic Ash']\n",
    "    prediction = pd.DataFrame(columns=all_columns)\n",
    "    \n",
    "\n",
    "    \n",
    "    col_barrio = 'Barrio_'+results['barrio']\n",
    "    col_clima = 'Condition_'+map_weather_spanish[results['clima']]\n",
    "    fecha = pd.to_datetime(results['fecha'])\n",
    "    col_hora = 'solo_hora_'+str(fecha.hour)\n",
    "    col_estacion = 'estacion_'+obtener_estacion(fecha)\n",
    "    col_fds = col_fds_dummie(fecha)\n",
    "    col_feriado = 'FERIADO_0.0'\n",
    "    \n",
    "    cols_predictions = [col_barrio, col_clima, col_estacion, col_fds, col_feriado, col_hora]\n",
    "    \n",
    "    prediction_df_columns = list(prediction.columns)\n",
    "    rest_columns = []\n",
    "    for pred_col in prediction_df_columns:\n",
    "        if pred_col not in cols_predictions:\n",
    "            rest_columns.append(pred_col)\n",
    "            \n",
    "    \n",
    "    for col in cols_predictions:\n",
    "        prediction.loc[1, col] = 1\n",
    "\n",
    "    for col in rest_columns:\n",
    "        prediction.loc[1, col] = 0\n",
    "    \n",
    "    \n",
    "    return prediction"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route('/', methods=['GET', 'POST'])\n",
    "def main():\n",
    "    if request.method == 'GET':\n",
    "        return(render_template('main.html'))\n",
    "    \n",
    "    if request.method == 'POST':\n",
    "        fecha = request.form['fecha']\n",
    "        barrio = request.form['barrio']\n",
    "        clima = request.form['clima']\n",
    "        #humidity = flask.request.form['humidity']\n",
    "        #windspeed = flask.request.form['windspeed']\n",
    "        #input_variables = pd.DataFrame([[fecha]],\n",
    "                                     #  columns=['fecha'],\n",
    "                                      # dtype=str)\n",
    "        \n",
    "        results = {'fecha': fecha, 'barrio': barrio, 'clima': clima}\n",
    "        \n",
    "        prediction = analyze_results(results)\n",
    "        \n",
    "        pred_model = model.predict(prediction)[0]\n",
    "        display(pred_model)\n",
    "        \n",
    "        #display(barrios)\n",
    "        barrio_jpg(barrios, barrio)\n",
    "        barrios['color'] = '#CECECE'\n",
    "        \n",
    "        print('\\n\\n======PREDICCION REALIZADA======\\n\\n')\n",
    "        if pred_model >= 1:\n",
    "            print('En ',barrio, 'podrían ocurrir', str(pred_model), 'accidentes... Cuidado!')\n",
    "        else:\n",
    "            print('En ',barrio, 'no deberían ocurrir accidentes. Relax!')\n",
    "        \n",
    "        \n",
    "        return render_template('main.html',\n",
    "                                     original_input={'Barrio':barrio,\n",
    "                                                     'Estado del clima':clima,\n",
    "                                                    'Fecha y Hora': fecha},\n",
    "                                     result=int(pred_model),\n",
    "                                     )\n",
    "    \n",
    "    #pred_model#(fecha, barrio, clima)#flask.render_template('main.html',\n",
    "                               #      original_input={'Temperature':temperature,\n",
    "                               #                      'Humidity':humidity,\n",
    "                               #                      'Windspeed':windspeed},\n",
    "                               #      result=prediction,\n",
    "                               #      )\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app \"__main__\" (lazy loading)\n",
      " * Environment: production\n",
      "\u001b[31m   WARNING: This is a development server. Do not use it in a production deployment.\u001b[0m\n",
      "\u001b[2m   Use a production WSGI server instead.\u001b[0m\n",
      " * Debug mode: off\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)\n",
      "127.0.0.1 - - [16/Oct/2021 00:19:48] \"\u001b[37mGET / HTTP/1.1\u001b[0m\" 200 -\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "1.1699985011267042"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "127.0.0.1 - - [16/Oct/2021 00:19:59] \"\u001b[37mPOST / HTTP/1.1\u001b[0m\" 200 -\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "\n",
      "======PREDICCION REALIZADA======\n",
      "\n",
      "\n",
      "En  PALERMO podrían ocurrir 1.1699985011267042 accidentes... Cuidado!\n"
     ]
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "if __name__ == '__main__':\n",
    "    app.run()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
