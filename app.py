from dotenv import load_dotenv #Librería para poder usar el archivo .env para más seguridad de nuestras keys
from flask import Flask,render_template #Librerias importantes para nuestra app web 
import time,json,os
from azure.cosmos import CosmosClient
app=Flask(__name__)#Creamos objeto Flask al momento de ejecutar nuestro script, lo instanciamos en app
load_dotenv()#Cargamos los pares de claves que se tienen en el archivo .env
KEY=os.environ['KEY']#Se almacena en la variable string el valor del par CSTRING en .env
URL=os.environ['URL']
@app.route('/',methods=["GET"])
def main():
    client = CosmosClient(URL, credential=KEY)
    DATABASE_NAME = 'Telemetry'
    database = client.get_database_client(DATABASE_NAME)
    CONTAINER_NAME = 'Container'
    container = database.get_container_client(CONTAINER_NAME)
    for item in container.query_items(query='SELECT * FROM Container',enable_cross_partition_query=True):
        data=json.dumps(item, indent=True)
    jsondict=json.loads(data)
    variable=jsondict['Dispositivo']
    mensaje=jsondict["Mensaje"]
    return render_template('welcome.html',orden=variable,data=mensaje)#Esta función main devuelve un template, el cual es el archivo form.html que se encuentra en la carpeta templates
app.run(debug=True)#Ejecutamos nuestra aplicación con el parametro debug true para modo de desarrollo