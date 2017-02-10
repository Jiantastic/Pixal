


# Import PWM and Pin Libraries
from machine import Pin, PWM
dCycleX = 60
dCycleY = 60
dCycleStep = 6
max = 4          #Maximum iteration times

#Initialise angle as 0 -> duty(30) and Pin allocation
servoX = PWM(Pin(15), freq=50, duty=dCycleX)
servoY = PWM(Pin(13), freq=50, duty=dCycleY)

#2 for loops to loop over every pixel
def motorMovement():
    # get CURRENT_STATE, move according to matrix size
    global dCycleX
    global dCycleY
    for i in range(0,max):
        servoX.duty(dCycleX)
        dCycleX = (dCycleY+dCycleStep) # if i<max else (dCycleX)
        time.sleep(1)
        #insert code to read and send temp data and send to broker
        for j in range(0,max):
            servoY.duty(dCycleY)
            dCycleY = (dCycleY+dCycleStep) # if j<max else (dCycleY)
            time.sleep(1)
            #insert code to read and send temp data and send to broker

#-----------------------------------------------------------------------------------------

motorMovement()
