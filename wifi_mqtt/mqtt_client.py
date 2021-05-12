import paho.mqtt.client as paho
import time

import serial
serdev = '/dev/ttyACM1'
s = serial.Serial(serdev, 9600)

# https://os.mbed.com/teams/mqtt/wiki/Using-MQTT#python-client

# MQTT broker hosted on local machine
mqttc = paho.Client()

tilt_over_number=0
confirm_gesture_number=""
exceed_x_angle=['','','','','','','','','','','']
exceed_y_angle=['','','','','','','','','','','']
exceed_z_angle=['','','','','','','','','','','']
z_difference=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
packet_number=0
last_z=0
i=0

# Settings for connection
# TODO: revise host to your IP
host = "192.168.160.29"
topic = "Mbed"

# Callbacks
def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n")
    mode=str(msg.payload)[12:13]
    print("mode: "+mode+"\n")
    if (mode=='1'):
        global confirm_gesture_number
        confirm_gesture_number=str(msg.payload)[31:32]
        #print("---------------Confirmed gesture_number information--------------\n")
        #print("confirm_gesture_number="+confirm_gesture_number)
        #print("---------------------------------------------------------\n")
        time.sleep(1)
        s.write(bytes("/STOPTILT/run\n", 'UTF-8'))
        print("sendback /STOPTILT/run!!\n")
#--------------------------------------------
        print("---------------Confirmed gesture_number information--------------\n")
        print("confirm_gesture_number="+confirm_gesture_number)
        print("---------------------------------------------------------\n")
        if (confirm_gesture_number=='0'):
            print("RING:\n")
            print("          *       \n")
            print("       *     *    \n")
            print("     *         *  \n")
            print("    *           * \n")
            print("     *         *  \n")
            print("       *     *    \n")
            print("          *       \n")
        if(confirm_gesture_number=='1'):
            print("SLOPE:\n")
            print("        *        \n")
            print("       *         \n")
            print("      *          \n")
            print("     *           \n")
            print("    *            \n")
            print("   *             \n")
            print("  *              \n")
            print(" * * * * * * * * \n")
        if(confirm_gesture_number=='2'):
            print("HEART:\n")
            print("                 \n\r")
            print("   **    ***     \n\r")
            print(" *   ** *   *    \n\r")
            print(" *     *    *    \n\r")
            print("   *       *     \n\r")
            print("     *   *       \n\r")
            print("       *         \n\r")
            print("                 \n\r")
        
        print("The extracted features: ")
        for j in range(11):
            print("%d " % z_difference[j])
        print("\n")

        

    if (mode=='2'):
        global last_z
        global i
        if (last_z==0):
            last_z=(int)(str(msg.payload)[27:32])
        else:
            if (i<11):
                if ((int)(str(msg.payload)[27:32]) > last_z):
                    z_difference[i]=1
                    i=i+1
                else:
                    z_difference[i]=0
                    i=i+1
                last_z=(int)(str(msg.payload)[27:32])

    if (mode=='3'):
        i=0
        for j in range(11):
            z_difference[j]=-1

        
            
        

    



def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed OK")

def on_unsubscribe(mosq, obj, mid, granted_qos):
    print("Unsubscribed OK")

# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

# Connect and subscribe
print("Connecting to " + host + "/" + topic)
mqttc.connect(host, port=1883, keepalive=60)
mqttc.subscribe(topic, 0)

# Publish messages from Python
#num = 0
#while num != 5:
#    ret = mqttc.publish(topic, "Message from Python!\n", qos=0)
#    if (ret[0] != 0):
#            print("Publish failed")
#    mqttc.loop()
#    time.sleep(1.5)
#    num += 1

# Loop forever, receiving messages
mqttc.loop_forever()