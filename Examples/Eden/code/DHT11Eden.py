import datetime
import time
import Adafruit_DHT 
from Adafruit_DHT.common import DHT11
import os
from gpiozero import LightSensor, LED
from ConnectIoT import ConnectIoT

# Connecting LDR to pin GPIO27
ldr=LightSensor(27)
led=LED(18)
ldr.when_dark=led.on
ldr.when_light=led.off


dht11 = Adafruit_DHT.DHT11
# DHT sensor
# connected to GPIO17.
pinDHT11 = 17


    
if __name__ == '__main__':

        contract = ConnectIoT(
                          os.environ.get('NEAR_CONTRACT_URL'),
                          os.environ.get('NEAR_ACCOUNT_ID'),
                          os.environ.get('NEAR_PRIVATE_KEY'))
        print('API URL: '+contract.contract_api_url)
        
        registry_name = 'EdenTest_1.0'
        device_name = 'DHT11 & LDR'

        new_registry=contract.create_registry(registry_name)
        new_device = contract.add_device_to_registry(
                registry_name, device_name, 'Device DHT11 & LDR for python lib test.')
       
        print("New Registry: "+registry_name+" created")
        print("New Device: "+device_name+", added to: "+registry_name)
        
while True:
        timenow = datetime.datetime.now()
        humidity, temperature = Adafruit_DHT.read_retry(dht11, pinDHT11)
        light=round(ldr.value*100,2)
    
        if humidity is not None and temperature is not None and light is not None:
            print('Temperature={0:0.1f}*C  Humidity={1:0.1f}%  Light={2:0.1f}%'.format(temperature, humidity,light))

            contract.set_device_data(registry_name, device_name, {
                'Date': timenow, 'Temperature C°': temperature, 'Humidity %': humidity,'Light %': light,})
            print(contract.get_device_data(registry_name, device_name))
                      
        else:
            print('Failed to get reading. Try again!') 
            if contract.delete_device_from_registry(registry_name, device_name):
                contract.delete_registry(registry_name)
                
                print('Device and Registry deleted!') 
                break
   
   
time.sleep(5)
