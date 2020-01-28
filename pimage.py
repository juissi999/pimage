import socket
import time
import random
import sys
from PIL import Image

# This is what separates pixel beign shown or not,
# currently only values above this are shown and
# below are not shown at all
THRESHOLD = 250

def load(imagefile):
	
	img = Image.open(imagefile)
	pixels = img.load()

	x,y = img.size

	dp = []
	for xx in range(0,x):
		for yy in range(0, y):
			val = pixels[xx, yy]

			if val < THRESHOLD:
				dp.append([xx,yy])

	return dp

def send(dp1, HOST, dur):
	# resolution 65500 x 1500
	# target reso 160x100

	#origo_x = 0
	#origo_y = 1450
	#end_x = 65500
	#end_y = 0
	#res_x = 160
	#res_y = 100

	origo_x = 20000
	origo_y = 1000
	end_x = 45500
	end_y = 500
	res_x = 160
	res_y = 100
	x_scale = (end_x-origo_x)/res_x
	y_scale = (end_y-origo_y)/res_y
	ports = range(origo_x, end_x, x_scale)
	msglens = range(origo_y, end_y, y_scale)

	# make UDP-socket
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setblocking(0)

	# send packages
	print("SENDING PACKAGES..")
	endtime = time.time()+dur
	pkgcount = 0
	while (time.time() < endtime):
		
		i = random.choice(dp1)
		x = ports[i[0]]
		y = msglens[i[1]]

		xp = random.randint(x, x+x_scale)
		yp = random.randint(y+y_scale, y)
		s.sendto("n"*yp, (HOST, xp)) #n*yp
		#s.sendto("n"*yp, socket.MSG_DONTWAIT, (HOST, xp)) #n*yp
		print("sending x:" + str(xp) + " y:" + str(yp))
		pkgcount = pkgcount + 1

	print("CLOSING.. PACKETS SENT " + str(pkgcount))

	# close socket
	s.close()

# check arguments
if (len(sys.argv) < 4):
	print("Give 3 arguments: imagefile, host address and duration[s]")
else:
	imagefile = sys.argv[1]
	HOST = sys.argv[2]
	dp = load(imagefile)
	duration = float(sys.argv[3]) #s
	send(dp, HOST, duration)