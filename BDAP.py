from datetime import datetime,date
import json,serial,time,json,asyncio,os
from azure.iot.device.aio import IoTHubDeviceClient
from dotenv import load_dotenv
load_dotenv()

conn=os.environ['CONN']
device_client = IoTHubDeviceClient.create_from_connection_string(conn)

async def mensaje(mensagee):
    await device_client.connect()
    mesagejson=json.dumps(mensagee)
    await device_client.send_message(mesagejson)

def main():
    i=0
    while i<50:
        file=open("BD.txt",'a')
        lectura=arduino.readline().decode()
        hora=datetime.time(datetime.now())
        fecha=date.today()
        if len(lectura) != 0:
            divition=lectura.split("_")
            if divition[0]=="0":
                file.write(f"Fecha: {fecha}, Hora:{hora},Dispositivo: Bluetooth, Mensaje: {divition[1]}")
                mensagee={"Fecha":f"{fecha}","Hora":f"{hora}","Dispositivo":"Bluetooh","Mensaje":f"{divition[1]}"}
                i+=1
                asyncio.run(mensaje(mensagee))
                file.close()
            elif divition[0]=="1":
                file.write(f"Fecha: {fecha}, Hora:{hora},Dispositivo: Tarjeta, Mensaje: {divition[1]}")
                mensagee={"Fecha":f"{fecha}","Hora":f"{hora}","Dispositivo":"Tarjeta","Mensaje":f"{divition[1]}"}
                i+=1
                asyncio.run(mensaje(mensagee))
                file.close()
            elif divition[0]=="2":
                file.write(f"Fecha: {fecha}, Hora:{hora},Dispositivo: LLavero, Mensaje: {divition[1]}")
                mensagee={"Fecha":f"{fecha}","Hora":f"{hora}","Dispositivo":"Llavero","Mensaje":f"{divition[1]}"}
                asyncio.run(mensaje(mensagee))
                file.close()
                i+=1
    device_client.shutdown()
    arduino.close()
if __name__ == "__main__":
    file=open("BD.txt",'w+')
    file.close()
    arduino=serial.Serial('COM3',115200)
    time.sleep(1)
    main()
