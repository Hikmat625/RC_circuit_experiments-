import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt


comparator_value = 4
troyka = 17

dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
bits = len(dac)
levels = 2**bits
maxvoltage = 3.3
listofnums =[]
temp=0

def decimal2binary(dec):
      return[int(bin) for bin in bin(dec)[2:].zfill(bits)]

def dec2dac(dec):
    for i in range(bits):
        GPIO.output(dac[i], dec[i])

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(leds, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(comparator_value, GPIO.IN)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
comp = GPIO.input(comparator_value)

def adc():
    znach = [1, 0, 0, 0, 0, 0, 0, 0, 0]
    for sch in range(9):
        dec2dac(znach)
        time.sleep(0.007) #стоп должен стоять между подачей сигнала на компаратор и его считыванием
        comp = GPIO.input(comparator_value)
        if sch == 8:
            val = 0
            for i in range(8):
                val += (2 ** (7 - i)) * znach[i]
            n = int(val / 31)
            for i in range (8):
                if i <= n-1:
                    GPIO.output(leds[i], 1)
                else:
                    GPIO.output(leds[i], 0)
            print(val, znach, n)
        elif comp == 0:
            znach[sch] = 0
            znach[sch + 1] = 1
        elif comp == 1:
            znach[sch + 1] = 1
    return val        
try:
    vremya = time.time()
    while(temp<250):
        temp=adc()
        listofnums.append(temp)
        
    GPIO.output(troyka,0)
    while(temp>2):
        temp=adc()
        listofnums.append(temp)
    vremya2 = time.time()
    valuesstr = [str(item) for item in listofnums]
    with open("data.txt","w") as f:
        f.write("\n".join(valuesstr))
    with open("settings.txt","w") as z:
        z.write("period:8ms values on V=0,0012 mV")

    


finally:
    print(len(listofnums))
    print(vremya2-vremya2,vremya2,vremya)
    GPIO.cleanup()
    plt.plot(listofnums)
    plt.show() 