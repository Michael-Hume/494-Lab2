import matplotlib.pyplot as plt
import serial

userName = input("Please enter user name\n")
userAge = int(input("Please enter user age\n"))

# Open the baseline file for the user & read in the Heart Rate & Breathing Rate
inputFile = open("out_rest_2.txt")
inputFile.readline()
inputFile.readline()
rawBR = inputFile.readline().split(",")[:-1]
rawBR = [ int(x) for x in rawBR ]
inputFile.readline()
rawHR = inputFile.readline().split(",")[:-1]
rawHR = [ int(x) for x in rawHR ]

# Number of reading read in
sampleSize = len(rawHR)

# Length (time) of reading
sampleTime = len(rawHR)/200
#print("Sample Time:", sampleTime)

#Find average heart rate & breathing rate
avgHR = int(round(sum(rawHR)/len(rawHR)))
avgBR = int(round(sum(rawBR)/len(rawHR)))

#print("HR:", rawHR)
#print("BR:", rawBR)
#print ("Avg BR:", avgBR)
#print ("Avg HR:", avgHR)

# Remove outliers (high readings)
unfilteredHeartRate = []
for x in rawHR:
    if x >= avgHR*1.2:
        unfilteredHeartRate.append(avgHR)
    if not x > avgHR*1.2:
        unfilteredHeartRate.append(x)

unfilteredBreathingRate = rawBR
for x in rawBR:
    if x >= avgBR*1.2:
        unfilteredHeartRate.append(avgBR)
    if not x > avgBR*1.2:
        unfilteredHeartRate.append(x)

# * * * * * * * * * * * * * * * * * * *
# Add code to apply filter to data here
# * * * * * * * * * * * * * * * * * * *

heartRate = unfilteredHeartRate # Replace with filter code
breathingRate = unfilteredBreathingRate # Replace with filter code

# * * * * * * * * * * * * * * * * * * *

# Recalculate average heart rate & breathing rate
avgHR = int(round(sum(heartRate)/len(heartRate)))
avgBR = int(round(sum(breathingRate)/len(breathingRate)))
#print ("New Avg HR:", avgHR)
#print ("New Avg BR:", avgBR)

beats = 0
bmp = 0.00
breathes = 0
brpm = 0.00

# Plot the graphs of the Heart & Breathing Rates
#plt.plot(heartRate)
#plt.ylabel('Heart Rate')
#plt.show()
#plt.plot(breathingRate)
#plt.ylabel('Breathing Rate')
#plt.show()

# cutoff set by visually looking at graph after removing outliers
heartBeatCutOff = 0.73
breathCutOff = 0.9949

for i in range(len(heartRate)):
    # if the reading is less than the cutoff AND the previous reading and the next reading ar both higher, count it as a heart beat
    if heartRate[i] <= avgHR*heartBeatCutOff and heartRate[i-1] > heartRate[i] and heartRate[i+1] > heartRate[i]:
            beats += 1

breathIn = False
tempLow = avgBR
for i in range(len(breathingRate)):
    # if the reading is less than the cutoff a temporary low reading is recorded to find the lowest reading
    if breathingRate[i] < avgBR*breathCutOff:
        if breathingRate[i] < tempLow:
            tempLow = breathingRate[i]
            breathIn = True
    # Once the readings reach above the average, the breath is recorded
    if breathingRate[i] > avgBR and breathIn == True:
        breathes += 1
        breathIn = False
        tempLow = avgBR

# calculate beats per minute
bmp = int(round((beats/sampleTime)*60))
brmp = int(round((breathes/sampleTime)*60))
print("Beats:", beats)
print("Breathes:", breathes)
print("Breathes per minute:", brmp)
print("Beats per minute:", bmp)

# Calculate user zones
maxHeartRate = 220 - userAge
maximum_cutoff = int(round(maxHeartRate * .9))
hard_cutoff = int(round(maxHeartRate * .8))
moderate_cutoff = int(round(maxHeartRate * .7))
light_cutoff = int(round(maxHeartRate * .6))
veryLight_cutoff = int(round(maxHeartRate * .5))

if bmp >= maxHeartRate:
    print("User is beyond their max heart rate!")
elif bmp >= maximum_cutoff:
    print("User is in 'Maximum' zone")
elif bmp >= hard_cutoff:
    print("User is in 'Hard' zone")
elif bmp >= moderate_cutoff:
    print("User is in 'Moderate' zone")
elif bmp >= light_cutoff:
    print("User is in 'Light' zone")
elif bmp >= veryLight_cutoff:
    print("User is in 'Very Light' zone")
else:
    print("User is in 'Resting' zone")

# Begin collection following activity
input("Press Enter to begin next collection...")

s = serial.Serial("/dev/cu.HC-05-DevB")
data = []

fig = plt.figure()
#ax1 = fig.add_subplot(1,1,1)

print( s.readline() )

wbr = []
whb = []

def animate(i):
    global wbr, whb
    d1 = s.readline().decode('utf-8').strip()
    data.append( d1.split(';')[0].split(',') )

    br = []
    hb = []

    for eachLine in data:
        #print( eachLine[0] )
        br.append( int( eachLine[0].strip() ) )
        hb.append(int( eachLine[1].strip() ))

    #ax1.clear()

    brf = []
    hbf = []

    for i in range( 1, len(br)-1 ): brf.append( br[i-1:i+2] )
    for i in range( 1, len(hb)-1 ): hbf.append( hb[i-1:i+2] )

    wbr = [ sum(x)/3.0 for x in brf ]
    whb = [ sum(x)/3.0 for x in hbf ]

    start = len(whb) - 300
    end   = len(whb)

    #plt.axis( [start, end, 0, 1024] )

    if len(wbr) == 0:
        return

    print( "HB: ", whb[-1] )
    print( "BR: ", wbr[-1] )
    print()

    #ax1.plot(br, label='BR')
    #ax1.plot(whb, label='HB')

    #plt.ylabel("Pressure (Relative Resistance)")
    #plt.xlabel("Time (Ticks)")
    #plt.title("Pressure vs Time")
#   ax1.legend(bbox_to_anchor=(1, 1), bbox_transform=plt.gcf().transFigure)

try:
    #ani = animation.FuncAnimation(fig, animate, interval=3)
    #plt.show()
    while True: animate(0)

finally:
    #print(wmf)
    outputFileName = userName + "_activeReading.txt"
    fd = open(outputFileName, "w")

    fd.write("\nBR\n")
    for i in wbr:
        fd.write("%d," % i)

    fd.write("\nHB\n")
    for i in whb:
        fd.write("%d," % i)
