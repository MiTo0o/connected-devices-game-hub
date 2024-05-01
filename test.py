import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing to all topics of interest here
    client.subscribe("topic/test")

def on_message(client, userdata, msg):
    print(f"Received message on {msg.topic}: {msg.payload.decode()}")

# Setup the MQTT client on Device 2
client2 = mqtt.Client()
client2.on_connect = on_connect
client2.on_message = on_message

# Connect to the broker running on Device 1
client2.connect("10.219.17.163", 1883, 60)  # Replace 'ip_of_device_1' with the actual IP address of Device 1
client2.loop_forever()

# Example of publishing a message
client2.publish("topic/test", "Hello from Device 2!")
print ("this is running")