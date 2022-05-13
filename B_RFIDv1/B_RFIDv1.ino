#include <SPI.h>      // incluye libreria bus SPI
#include <MFRC522.h>      // incluye libreria especifica para MFRC522
#include "BluetoothSerial.h"
#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

BluetoothSerial SerialBT;

#define RST_PIN  4      // constante para referenciar pin de reset
#define SS_PIN  5      // constante para referenciar pin de slave select


MFRC522 mfrc522(SS_PIN, RST_PIN); // crea objeto mfrc522 enviando pines de slave select y reset

byte LecturaUID[4];         // crea array para almacenar el UID leido
byte Llavero[4]= {0x53, 0x80, 0xA2, 0x0B} ;    // ***Aquí se cambian los UID, se ponen en hexadecimales***
byte Tarjeta[4]= {0xC3, 0x1E, 0x71, 0x11} ;    // ***Aquí se cambian los UID, se ponen en hexadecimales***

void setup() {
  Serial.begin(115200);     // inicializa comunicacion por monitor serie a 9600 bps
  SPI.begin();        // inicializa bus SPI
  mfrc522.PCD_Init();     // inicializa modulo lector
  SerialBT.begin("ESP32test"); //Bluetooth device name
}

void loop() {
  if ( ! mfrc522.PICC_IsNewCardPresent())   // si no hay una tarjeta presente
    //(Aquí leé el bluetooth)
     if (Serial.available()) {
      SerialBT.write(Serial.read());
      }
    if (SerialBT.available()) {
      Serial.write(SerialBT.read());
      }
  delay(20);
    
  if ( ! mfrc522.PICC_ReadCardSerial())     // si no puede obtener datos de la tarjeta
    return;           // retorna al loop esperando por otra tarjeta
    
    //Serial.print("1_");       // muestra texto UID:
    for (byte i = 0; i < mfrc522.uid.size; i++) { // bucle recorre de a un byte por vez el UID
      if (mfrc522.uid.uidByte[i] < 0x10){   // si el byte leido es menor a 0x10
        Serial.print("");       // imprime espacio en blanco y numero cero
        }
        else{           // sino
          Serial.print("");        // imprime un espacio en blanco
          }
          //Serial.print(mfrc522.uid.uidByte[i], HEX);    // imprime el byte del UID leido en hexadecimal
          LecturaUID[i]=mfrc522.uid.uidByte[i];     // almacena en array el byte del UID leido      
          }             
                    
          if(comparaUID(LecturaUID, Tarjeta)) {   // llama a funcion comparaUID con Usuario1
            Serial.write("1_Tarjeta detectada\n");
          }
          if(comparaUID(LecturaUID, Llavero)){ // llama a funcion comparaUID con Usuario2
            Serial.write("2_Llavero detectado\n");
          }
          else{        // si retorna falso
            Serial.println(" No te conozco");    // muestra texto equivalente a acceso denegado
                  mfrc522.PICC_HaltA();     // detiene comunicacion con tarjeta   
          }             
}
boolean comparaUID(byte lectura[],byte usuario[]) // funcion comparaUID
{
  for (byte i=0; i < mfrc522.uid.size; i++){    // bucle recorre de a un byte por vez el UID
  if(lectura[i] != usuario[i])        // si byte de UID leido es distinto a usuario
    return(false);          // retorna falso
  }
  return(true);           // si los 4 bytes coinciden retorna verdadero
}
