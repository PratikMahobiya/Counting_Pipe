from tkinter import *
import tkinter.font as tkFont
import cv2
import os
import threading
from PIL import Image, ImageTk
from tkinter import messagebox as mb
import time
from api import api

class Window:
    def __init__(self, Path_to_img):

        # Predefined data------------------------------------------------------------------------
        self.cam = None
        self.frame = None
        self.Path_to_img = Path_to_img

        # initialize the root window and image panel---------------------------------------------
        self.win = Tk()
        self.win.title('Aon Digicon')
        self.win.config(background = '#808080')
        self.win.geometry("{}x{}+10+10".format(self.win.winfo_screenwidth() - 50, self.win.winfo_screenheight() - 50))
        
        # Right Footer Frame having Buttons-------------------------------------------------------
        self.r_footer_frame = Frame(self.win, width=500, height = 150, bg = "#867979")
        self.r_footer_frame.place(x = self.win.winfo_screenwidth() - 650, y = self.win.winfo_screenheight() - 250)

        self.config_btn = Button(self.r_footer_frame, text="Configure_cam", command=self.config_cam)
        self.config_btn.place(x = 350, y = 10, width = 100, height = 30)

        fontStyle = tkFont.Font(size=12, weight="bold")
        self.cam_status = Label(self.r_footer_frame, text='Disconnected', font = fontStyle, relief=FLAT, bg = "red")
        self.cam_status.place(x = 50, y = 10, width = 150, height = 30)

        # Initialize Stop Event to stop the Camera-----------------------------------------------
        self.stopEvent = threading.Event()


        # Default Black Background img------------------------------------------------------------
        # dim = (self.win.winfo_screenwidth() - 750, self.win.winfo_screenwidth() - 900)
        dim = (616,466)
        Img = Image.new('RGB', dim, color = 'black')
        self.blk_img = ImageTk.PhotoImage(Img.resize(dim, Image.ANTIALIAS))
        self.panel = Label(self.win, image=self.blk_img)
        self.panel.place(x = 30,y = 30)

        fontStyle = tkFont.Font(family="Lucida Grande", size=30, weight="bold")
        self.Count = Label(self.win, text = "Not-Detected" ,font = fontStyle, relief=RIDGE, bg = "red")
        self.Count.place(x = self.win.winfo_screenwidth() - 650, y = self.win.winfo_screenheight() - 730, width = 540, height = 60)
        self.img_label = Label(self.win, image=self.blk_img)
        self.img_label.place(x = self.win.winfo_screenwidth() - 690, y = self.win.winfo_screenheight() - 660, width = 616, height = 400)

        # Set winndow Close events-----------------------------------------------------------------
        self.win.wm_protocol("WM_DELETE_WINDOW", self.onclose)

    def config_cam(self):
    	# Initialize Buttons-----------------------------------------------------------------------
    	fontStyle = tkFont.Font(size=12, weight="bold")
    	self.label1 = Label(self.win, text='Camera address:-', font = fontStyle, bg = '#808080')
    	self.label1.place(x = self.win.winfo_screenwidth() - 1300,y = self.win.winfo_screenheight() - 200, width = 150, height = 30)

    	self.conf_cam = Entry(font = fontStyle)
    	self.conf_cam.place(x = self.win.winfo_screenwidth() - 1100,y = self.win.winfo_screenheight() - 200, width = 300, height = 30)

    	self.connect_btn = Button(self.win, text="Connect", command=self.connect_cam)
    	self.connect_btn.place(x = self.win.winfo_screenwidth() - 900, y = self.win.winfo_screenheight() - 150, width = 100, height = 30)

    def connect_cam(self):
    	# Configure Camera-------------------------------------------------------------------------

    	# If Text Feild is empty-------------------------------------------------------------------
    	if len(self.conf_cam.get()) == 0:
    		text = "Enter Address"
    		self.cam_status.configure(text=text)
    		self.cam_status.text = text
    	else:
    		# If cam is None-----------------------------------------------------------------------
    		if self.cam is None:
    			cap = self.conf_cam.get()

    			# 0 is for Webcam (if Available)---------------------------------------------------
	    		if cap == "0":
	    			cap = int(cap)
	    		self.cam = cv2.VideoCapture(cap)

	    		# Check If Camera is Successfully Connected----------------------------------------
    			if self.cam.isOpened():
    				text = "Connected"
		    		self.cam_status.configure(text=text)
		    		self.cam_status.text = text

	    			self.Start_btn = Button(self.r_footer_frame, text="Start", command=self.onstart)
	    			self.Start_btn.place(x = 350, y = 45, width = 100, height = 30)

	    			self.label1.destroy()
		    		self.conf_cam.destroy()
		    		self.connect_btn.destroy()
	    		else:
	    			self.cam = None
	    			text = "Invalid Camera"
	    			self.cam_status.configure(text=text)
	    			self.cam_status.text = text

    		elif self.cam.isOpened() and self.stopEvent.is_set():
    			self.stopEvent.set()
    			self.cam.release()
    			cap = self.conf_cam.get()
	    		if cap == "0":
	    			cap = int(cap)
	    		self.cam = cv2.VideoCapture(cap)
	    		if self.cam.isOpened():
	    			text = "Connected"
		    		self.cam_status.configure(text=text)
		    		self.cam_status.text = text

	    			self.Start_btn = Button(self.r_footer_frame, text="Start", command=self.onstart)
	    			self.Start_btn.place(x = 350, y = 45, width = 100, height = 30)

	    			self.label1.destroy()
		    		self.conf_cam.destroy()
		    		self.connect_btn.destroy()
	    		else:
	    			self.cam = None
	    			text = "Invalid Camera"
	    			self.cam_status.configure(text=text)
	    			self.cam_status.text = text
    	
    def onstart(self):
    	# Start a thread for Camera----------------------------------------------------

    	# only one Thread is running at a time-----------------------------------------
    	# print(threading.active_count())
    	if threading.active_count() == 1:
    		self.config_btn.destroy()
	    	self.Snapshot_btn = Button(self.r_footer_frame, text="Snapshot!", command=self.takeSnapshot)
	    	self.Snapshot_btn.place(x = 350, y = 45, width = 100, height = 30)
	    	self.Stop_btn = Button(self.r_footer_frame, text="Stop", command=self.onstop)
	    	self.Stop_btn.place(x = 250, y = 45, width = 100, height = 30)
    		if not self.stopEvent.is_set():
    			self.thread = threading.Thread(target=self.videoLoop, args=())
    			self.thread.start()
    		elif self.stopEvent.is_set():
    			self.stopEvent.clear()
    			self.thread = threading.Thread(target=self.videoLoop, args=())
    			self.thread.start()

    # Stop all the running Events-------------------------------------------------------
    def onstop(self):
    	for widget in self.r_footer_frame.winfo_children():
    		if widget == self.Start_btn or widget == self.cam_status:
    			if self.cam.isOpened():
		    		text = "Connected"
	    			self.cam_status.configure(text=text)
	    			self.cam_status.text = text
    		else:
		    	widget.destroy()

    	if not self.stopEvent.is_set():
    		self.stopEvent.set()
    		self.panel.configure(image = self.blk_img)
    		self.panel.image = self.blk_img
    		self.img_label.configure(image = self.blk_img)
    		self.img_label.image = self.blk_img
    		self.Count.configure(text = "Not-Detected")
    		self.Count.text = "Not-Detected"
    		self.config_btn = Button(self.r_footer_frame, text="Configure_cam", command=self.config_cam)
    		self.config_btn.place(x = 350, y = 10, width = 100, height = 30)
    	else:
    		self.panel.configure(image = self.blk_img)
    		self.panel.image = self.blk_img
    		self.img_label.configure(image = self.blk_img)
    		self.img_label.image = self.blk_img
    		self.Count.configure(text = "Not-Detected")
    		self.Count.text = "Not-Detected"
    		self.config_btn = Button(self.r_footer_frame, text="Configure_cam", command=self.config_cam)
    		self.config_btn.place(x = 350, y = 10, width = 100, height = 30)

    # Confirmation a window----------------------------------------------------------
    def confirm(self):
        res = mb.askquestion('Exit Application', 'Do you really want to exit')
        if res == 'yes':
            self.win.quit()
        else:
        	self.cam = None
        	text = "Disconnected"
        	self.cam_status.configure(text=text)
        	self.cam_status.text = text
        	if not self.stopEvent.is_set():
        		self.stopEvent.set()
        		self.panel.configure(image = self.blk_img)
        		self.panel.image = self.blk_img
        		self.img_label.configure(image = self.blk_img)
        		self.img_label.image = self.blk_img
        		self.Count.configure(text = "Not-Detected")
        		self.Count.text = "Not-Detected"
        	else:
        		if not self.stopEvent.is_set():
	        		self.stopEvent.set()
	        		self.panel.configure(image = self.blk_img)
	        		self.panel.image = self.blk_img
	        		self.img_label.configure(image = self.blk_img)
	        		self.img_label.image = self.blk_img
	        		self.Count.configure(text = "Not-Detected")
	        		self.Count.text = "Not-Detected"

	# Close a Window-------------------------------------------------------------
    def onclose(self):
        print("[INFO] closing...")
        if self.cam is None:
            self.win.quit()
        else:
        	self.Start_btn.destroy()
        	self.onstop()
        	self.cam.release()
        	self.confirm()

    # Start a Camera------------------------------------------------------------
    def videoLoop(self):
        try:
            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                # grab the frame from the video stream and resize it to
                self.ret , self.frame = self.cam.read()

                dim = (self.win.winfo_screenwidth() - 750,self.win.winfo_screenwidth() - 900)
                self.frame = cv2.resize(self.frame, dim,  interpolation = cv2.INTER_AREA)
        
                # OpenCV represents images in BGR order; however PIL
                # represents images in RGB order, so we need to swap
                # the channels, then convert to PIL and ImageTk format
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)
                if not self.stopEvent.is_set():
	                self.panel.configure(image = image)
	                self.panel.image = image
        except RuntimeError as e:
            print("[INFO] caught a RuntimeError")
            self.panel.configure(image = self.blk_img)
            self.panel.image = self.blk_img

    # Take a Snap and detect circles--------------------------------------------
    def takeSnapshot(self):
        Count, Img = api.gen_frames(self.frame, self.Path_to_img)

        self.Count.configure(text = Count)
        self.Count.text = Count

        dim = (616,466)
        not_found_img = Image.new('RGB', dim, color = (73, 109, 137))
        img = ImageTk.PhotoImage(not_found_img.resize((616, 400), Image.ANTIALIAS))

        if Img != 0:
	        img = ImageTk.PhotoImage(Image.open(Img).resize((616, 400), Image.ANTIALIAS))

        self.img_label.configure(image = img)
        self.img_label.image = img