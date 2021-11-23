#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

//KONFIGURASI SSID & PASSWORD DAN SETTING SERVER MQTT BROKER
const char* ssid          = "delameta";
const char* password      = "bilano1407";
//const char* mqtt_server   = "iwancilibur.ip-dynamic.com"; // MQTT Broker pubic (iwancilibur.ip-dynamic.com)
const char* mqtt_server   = "broker.hivemq.com"; // MQTT Broker pubic (iwancilibur.ip-dynamic.com)
      char* clientid      = "iwanciliburDevice02";

//INISIALISASI PIN
int LED_R=25;
int LED_G=26;
int LED_B=27;

#define DHTTYPE DHT11
#define DHTPIN  2
DHT dht(DHTPIN, DHTTYPE);

WiFiClient espClient;
PubSubClient client(espClient);

int waktu_sebelumnya = 0;

void setup() {
  Serial.begin(115200);
  setup_wifi();
  dht.begin();
  pinMode(LED_R, OUTPUT);     // Initialize the LED pin as an output
  pinMode(LED_G, OUTPUT);
  pinMode(LED_B, OUTPUT);
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}


void callback(char *Topic, byte *message, unsigned int length)
{
  Serial.print("Pesan yang di Terima: ");
  Serial.print(Topic);
  Serial.print(". isi pesan: ");
  
  String messageTemp;
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();
  
  //Jika topic "iwancilibur/LED_R" menerima pesan "on" maka Relay HIGH (Menyala), jika "off" maka Relay LOW (Mati)
  if (String(Topic) == "iwancilibur/LED_R") {
    Serial.print("Status :  ");
    if(messageTemp =="on"){ 
      digitalWrite(LED_R, HIGH);
      Serial.println("LAMPU 1 NYALA");
    }else if(messageTemp =="off"){
      digitalWrite(LED_R, LOW); 
      Serial.println("LAMPU 1 MATI");
  }
  }

  //Jika topic "iwancilibur/LED_G" menerima pesan "on" maka Relay HIGH (Menyala), jika "off" maka Relay LOW (Mati)
  if (String(Topic) == "iwancilibur/LED_G") {
    Serial.print("Status :  ");
    if(messageTemp =="on"){ 
      digitalWrite(LED_G, HIGH);
      Serial.println("LAMPU 2 NYALA");
    }else if(messageTemp =="off"){
      digitalWrite(LED_G, LOW); 
      Serial.println("LAMPU 2 MATI");
  }
  }

  //Jika topic "iwancilibur/LED_B" menerima pesan "on" maka Relay HIGH (Menyala), jika "off" maka Relay LOW (Mati)
  if (String(Topic) == "iwancilibur/LED_B") {
    Serial.print("Status :  ");
    if(messageTemp =="on"){ 
      digitalWrite(LED_B, HIGH);
      Serial.println("LAMPU 3 NYALA");
    }else if(messageTemp =="off"){
      digitalWrite(LED_B, LOW); 
      Serial.println("LAMPU 3 MATI");
  }
  }
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
    client.loop();
    //delay(100);

    unsigned long waktu_sekarang = millis();
    if(waktu_sekarang - waktu_sebelumnya >= 1000){
        waktu_sebelumnya = waktu_sekarang;
    //BACA DATA
    //float dataSUHU = dht.readTemperature();
    //float dataKELEMBABAN = dht.readHumidity();
    float dataSUHU = random(0,100);
    float dataKELEMBABAN = random(0,100);

    //POST TO SERIAL
    Serial.print("SUHU :");Serial.print(dataSUHU);
    Serial.print(" | KELEMBABAN :");Serial.print(dataKELEMBABAN);
    Serial.println(); //UNTUK ENTER
    
    //POST TO MQTT
    client.publish("iwancilibur/suhu", String(dataSUHU).c_str()); //Nama Topic harus Unix (tidak boleh sama)
    client.publish("iwancilibur/kelembaban", String(dataKELEMBABAN).c_str());//Nama Topic harus Unix (tidak boleh sama)
    }
    
}


void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Menghubungkan Ulang ke MQTT...");
    // AtsuhuPublisht to connect
    if (client.connect(clientid)) {
      Serial.println("connected");
      client.subscribe("iwancilibur/LED_R");
      client.subscribe("iwancilibur/LED_G");
      client.subscribe("iwancilibur/LED_B");
      // Once connected, publish an announcement...
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}
