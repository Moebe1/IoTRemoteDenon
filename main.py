# import machine
# i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
#
# print('Scan i2c bus...')
# devices = i2c.scan()
#
# if len(devices) == 0:
#   print("No i2c device !")
# else:
#   print('i2c devices found:',len(devices))
#
# for device in devices:
#     print("Decimal address: ",device," | Hexa address: ",hex(device))

import machine, ssd1306
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 60, i2c, 0x3c)
oled.fill(0)
oled.text("Denon IoT Remote", 0, 0)
oled.show()

def sub_cb(topic, msg):
    print((topic, msg))
    if topic == b'notification' and msg == b'received':
        print('ESP received hello message')


def wait_pin_change(button):
    # wait for pin to change value
    # it needs to be stable for a continuous 20ms
    cur_value = button.value()
    active = 0
    while active < 20:
        if button.value() != cur_value:
            active += 1
        else:
            active = 0
        delayTimer = machine.WDT(timeout=10)
        delayTimer.feed()


def connect_and_subscribe():
    global client_id, mqtt_server, topic_sub
    client = MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub)
    print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
    return client


def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()


def publish_volume(val):
    print('Publishing')
    msg = b'%d' % val
    client.publish(topic_pub, msg)
    print('Published:', msg)
    gc.collect


r = RotaryIRQ(pin_num_clk=12, pin_num_dt=13, min_val=0, max_val=70, reverse=True, range_mode=RotaryIRQ.RANGE_BOUNDED)
button = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
lastval = r.value()

print("Button: ", button.value())
try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

while True:
    chk = False
    val = r.value()
    pVal = button.value()
    # print('pVal:',pVal)
    if lastval != val:
        lastval = val
        print('result =', val)
        disP = str(val)
        oled.fill(0)
        oled.text(disP,0,0)
        oled.show()
        gc.collect()
    while pVal == 0:
        msg = b'%d' % val
        client.publish(topic_pub, msg)
        time.sleep_ms(200)
        pVal = 1

