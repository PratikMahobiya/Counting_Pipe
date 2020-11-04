import os
import cv2
import numpy as np
import datetime
from configparser import ConfigParser

#Get the configparser object----------------------------------------------
config_object = ConfigParser()

if not os.path.isfile("config.ini"):

	#Assume we need 2 sections in the config file, let's call them USERINFO and SERVERCONFIG
	config_object["DEFAULT"] = {
	    "dp"			: "1",
	    "min_dist"		: "40",
	    "param_1"		: "40",
	    "param_2"		: "20",
	    "min_radius"	: "5",
	    "max_radius"	: "18"
	    
	}

	config_object["INFORMATIONS"] = {
	    "dp = 1 								: The inverse ratio of resolution." : "",
		"min_dist = gray.rows / 16			: Minimum distance between detected centers." : "",
		"param_1 = 40						: Upper threshold for the internal Canny edge detector." : "",
		"param_2 = 20						: Threshold for center detection.":"",
		"min_radius = 5						: Minimum radius to be detected. If unknown, put zero as default." : "",
		"max_radius = 20						: Maximum radius to be detected. If unknown, put zero as default." : ""
	}

	#Write the above sections to config.ini file--------------------------------
	with open('config.ini', 'w') as conf:
	    config_object.write(conf)
else:
	pass


config_object.read("config.ini")

#Get the Values
Parameters = config_object["DEFAULT"]

dp 				= Parameters["dp"]
min_dist 		= Parameters["min_dist"]
param1 			= Parameters["param_1"]
param2 			= Parameters["param_2"]
min_radius 		= Parameters["min_radius"]
max_radius 		= Parameters["max_radius"]

def gen_frames(frame, Path_to_img):

	# print(dp,min_dist,param1,param2,min_radius,max_radius)

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray_blurred = cv2.blur(gray, (3, 3))
	rows = gray.shape[0]
	detected_circles = cv2.HoughCircles(gray_blurred,cv2.HOUGH_GRADIENT, dp = int(dp), minDist = rows / int(min_dist),
										param1 = int(param1), param2 = int(param2), minRadius = int(min_radius), maxRadius = int(max_radius))

	# If pipe were detected
	if detected_circles is not None:
		detected_circles = np.uint16(np.around(detected_circles))
		for pt in detected_circles[0, :]:
			a, b, r = pt[0], pt[1], pt[2]
			cv2.circle(frame, (a, b), r, (0, 255, 0), 2)
			cv2.circle(frame, (a, b), 1, (0, 0, 255), 3)
		now = datetime.datetime.now()
		filename = "{}.jpg".format(now.strftime("%Y-%m-%d_%H-%M-%S"))
		Img_path = os.path.sep.join((Path_to_img, filename))
		# print(Img_path)

		# save the file
		cv2.imwrite(Img_path, frame)

		# Number of Pipes	
		Pipe_count = detected_circles.shape
		count = Pipe_count[1]
		# print(count)

		return count, Img_path
	else:
		count = "Nothing is detected"
		Img_path = 0
		return count, Img_path