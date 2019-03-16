import serial

s = serial.Serial("/dev/cu.HC-05-DevB")
data = []

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

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

    if len(wbr) == 0: return

    print( "HB: ", whb[-1] )
    print( "BR: ", wbr[-1] )
    print()

    #ax1.plot(br, label='BR')
    #ax1.plot(whb, label='HB')

    #plt.ylabel("Pressure (Relative Resistance)")
    #plt.xlabel("Time (Ticks)")
    #plt.title("Pressure vs Time")    
    #ax1.legend(bbox_to_anchor=(1, 1), bbox_transform=plt.gcf().transFigure)

try:
    #ani = animation.FuncAnimation(fig, animate, interval=3)
    #plt.show()
    while True: animate(0)

finally:
    #print(wmf)
    fd = open("out.txt", "w")

    fd.write("\nBR\n")
    for i in wbr: fd.write("%d," % i)

    fd.write("\nHB\n")
    for i in whb: fd.write("%d," % i)
