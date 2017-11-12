from Tkinter import *
import tkFileDialog
import cv2
import numpy as np
import argparse
import dlib
import Image
import ImageTk

import matplotlib.pyplot as plt
from skimage import exposure
from skimage.restoration import denoise_bilateral

def autoenhancing():
    global panelA,panelB
    path = tkFileDialog.askopenfilename()
    print("AUTO ENHANCE")
    astro = cv2.imread(path)
    astro = cv2.cvtColor(astro, cv2.COLOR_BGR2GRAY)
    img=astro

    p2, p98 = np.percentile(img, (2, 98))
    img_rescale = exposure.rescale_intensity(img, in_range=(p2, p98))

    img=img_rescale

    adapteq = exposure.equalize_adapthist(img, clip_limit=0.03)
		
    img=adapteq
    denoised = denoise_bilateral(img, sigma_color=0.1,sigma_spatial=15, multichannel=False)
    img=denoised
    for i in range(len(img)):
        for j in range(len(img[0])):
            img[i][j]=255*img[i][j]
            
	# convert the images to PIL format...    
    pic1 = Image.fromarray(astro)
    pic = Image.fromarray(img)
	# ...and then to ImageTk format
    image = ImageTk.PhotoImage(pic1)
    edged = ImageTk.PhotoImage(pic)
		


		
    if panelA is None or panelB is None:
		# the first panel will store our original image
        panelA = Label(image=image)
        panelA.image = image
        panelA.pack(side="left", padx=10, pady=10)
 
		# while the second panel will store the edge map
        panelB = Label(image=edged)
        panelB.image = edged
        panelB.pack(side="right", padx=10, pady=10)
 
		# otherwise, update the image panels
    else:
		# update the pannels
        panelA.configure(image=image)
        panelB.configure(image=edged)
        panelA.image = image
        panelB.image = edged
			


def red_eye():
    global panelA,panelB
    path = tkFileDialog.askopenfilename()

    print("RED EYE")
    if(len(path)>0):
        cap = cv2.imread(path)
        pic = Image.open(path)
        pic1= Image.open(path)
        width,height=pic.size
        PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(PREDICTOR_PATH)

        rects = detector(cap)

        for m in range(len(rects)):
        	counter=0
            l_l=width
            l_r=0
            l_t=0
            l_b=height

            r_l=width
            r_r=0	
            r_t=0
            r_b=height
            for i in  predictor(cap, rects[m]).parts() :
                counter=counter+1
                if((counter>36)and(counter<43)):
                    if(l_l>i.x):
                        l_l=i.x
                    if(l_r<i.x):
                        l_r=i.x
                    if(l_t<i.y):
                        l_t=i.y
                    if(l_b>i.y):
                        l_b=i.y
		
                elif((counter>42)and(counter<49)):
                    if(r_l>i.x):
                        r_l=i.x
                    if(r_r<i.x):
                        r_r=i.x     
                    if(r_t<i.y):
                        r_t=i.y
                    if(r_b>i.y):
                        r_b=i.y
        
            for x in range(l_l, l_r):
                for y in range(l_b, l_t):
                    if((len(pic.getpixel((x,y))))==3):
                        r,g,b = pic.getpixel( (x,y) )
                        if((r>1.5*g)and(r>1.5*b)):
                            if(g<b):
                                r=g
                            else:
                                r=b
                        pic.putpixel((x,y),(r,g,b))
               	    else:
                        r,g,b,a = pic.getpixel( (x,y) )
                        if((r>1.5*g)and(r>1.5*b)):
                            if(g<b):
                                r=g
                            else:
                                r=b
                        pic.putpixel((x,y),(r,g,b,a))


            for x in range(r_l, r_r):
                for y in range(r_b, r_t):
                    if((len(pic.getpixel((x,y))))==3):
                        r,g,b = pic.getpixel( (x,y) )
                        if((r>1.5*g)and(r>1.5*b)):
                            if(g<b):
                                r=g
                            else:
                                r=b
                        pic.putpixel((x,y),(r,g,b))
               	    else:
               	        r,g,b,a = pic.getpixel( (x,y) )
                        if(( r>1.5*g)and(r>1.5*b)):
                            if(g<b):
                                r=g
                            else:
                                r=b
                        pic.putpixel((x,y),(r,g,b,a))  


            print('sagar')

        image = ImageTk.PhotoImage(pic1)
        edged = ImageTk.PhotoImage(pic)

		
        if panelA is None or panelB is None:
			# the first panel will store our original image
            panelA = Label(image=image)
            panelA.image = image
            panelA.pack(side="left", padx=10, pady=10)
 
			# while the second panel will store the edge map
            panelB = Label(image=edged)
            panelB.image = edged
            panelB.pack(side="right", padx=10, pady=10)
 
		# otherwise, update the image panels
        else:
			# update the pannels
            panelA.configure(image=image)
            panelB.configure(image=edged)
            panelA.image = image
            panelB.image = edged
		

 
# create a button, then when pressed, will trigger a file chooser
# dialog and allow the user to select an input image; then add the
# button the GUI

root = Tk()
btn = Button(root, text="AutoEnhance", command=autoenhancing, bg="black", fg="white")
btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
btn = Button(root, text="RedEye", command=red_eye, bg="red")
btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")


panelA = None
panelB = None
label = Label(root)
label.pack()

# kick off the GUI
root.mainloop()	

