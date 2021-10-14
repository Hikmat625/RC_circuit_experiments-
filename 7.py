##############################################################################
#               importing needed modules                                     #  
##############################################################################
import RPi.GPIO as gpio
import time
import matplotlib.pyplot as plt
##############################################################################
#                              constants                                     #
##############################################################################
i=0
dac=[26,19,14,6,5,11,9,10]
leds=[21,20,16,12,7,8,25,24]
bits = 8
levels = 2**bits
troyka = 17
comparator = 4
test=[1,1,1,1,1,1,1,1]
values = []
temp = 0
##############################################################################
#               seting up gpio pins                                          #
##############################################################################
gpio.setmode(gpio.BCM)
gpio.setup(dac,gpio.OUT,initial = gpio.LOW)
gpio.setup(troyka,gpio.OUT,initial = gpio.HIGH)
gpio.setup(leds,gpio.OUT,initial=gpio.LOW)
gpio.setup(comparator,gpio.IN)
##############################################################################
#                        defining functions                                  #
##############################################################################
def adc():
    test=[1,0,0,0,0,0,0,0]
    for i in range(7):
        #print(test)
        gpio.output(dac,test)
        time.sleep(0.001)
        cv=gpio.input(comparator)
        if(cv==0):
            test[i]=0
            test[i+1]=1
        else:
            test[i+1]=1
        #print(test)
    b=0
    for i in range(8):
        b=b+2**(7-i)*test[i]
    return b

def dec2bin(dec):
    return[int(i)for i in bin(dec)[2:].zfill(bits)]        
try:
    gpio.output(troyka,1)
    vremya = time.time()
    while(temp<254):
        temp=adc()
        values.append(temp)
        gpio.output(leds,dec2bin(temp))       #this while loop uses analog to digital converter to get value on condensator
        print("condensator is charging")
    print("condesator reached its max voltage")
    time.sleep(0.1)
    gpio.output(troyka,0)
    while(temp>1):
        temp=adc()
        values.append(temp)                    #this while loop uses analog to digital converter to get value on condensator
        gpio.output(leds,dec2bin(temp))
        print("condensator is decharging")
    vremya2 = time.time()
    valuesstr = [str(item) for item in values]
##############################################################################
#               writing getted data to data.txt                              #
##############################################################################    
    with open("data.txt","w") as f:
        f.write("\n".join(valuesstr))
finally:
##############################################################################
#                      builing graph                                         #
##############################################################################
    gpio.cleanup()
    plt.plot(values)
    plt.show()  
    with open("settings.txt","w") as z:
        z.write("period:8ms values on V=0,0012 mV")
    print("experiment is finished")