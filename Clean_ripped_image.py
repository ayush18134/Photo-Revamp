import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata
from copy import deepcopy
from skimage import io, color
import cv2

gray = cv2.imread("final.png")

type_interp = 2 #Bilinear
new = deepcopy(gray)

def interpolate(x,y):
    neigh=3

    #Neighbour Coordinates
    A = np.array( [[x-neigh , y-neigh , (x-neigh) * (y-neigh) , 1] ,    # coordinate matrix
                   [x+neigh , y-neigh , (x+neigh) * (y-neigh) , 1] ,
                   [x-neigh , y+neigh , (x-neigh) * (y+neigh) , 1] ,
                   [x+neigh , y+neigh , (x+neigh) * (y+neigh) , 1] ] )
    try:
        Qr = np.array( [[gray[x-neigh ][ y-neigh][0]] ,                 # pixel value
                       [gray[x+neigh ][ y-neigh][0]] ,
                       [gray[x-neigh ][ y+neigh][0]] ,
                       [gray[x+neigh ][ y+neigh][0]] ] )
        Qg = np.array( [[gray[x-neigh ][ y-neigh][1]] ,                 # pixel value
                       [gray[x+neigh ][ y-neigh][1]] ,
                       [gray[x-neigh ][ y+neigh][1]] ,
                       [gray[x+neigh ][ y+neigh][1]] ] )
        Qb = np.array( [[gray[x-neigh ][ y-neigh][2]] ,                 # pixel value
                       [gray[x+neigh ][ y-neigh][2]] ,
                       [gray[x-neigh ][ y+neigh][2]] ,
                       [gray[x+neigh ][ y+neigh][2]] ] )


        A_inv = np.linalg.inv(A)                                            # pseudo inverse of A
        input_vec = np.array([x , y , x * y , 1])                           # coordinates x , y in vector

        coeffr = np.dot(A_inv , Qr)                                           # coeff matrix
        coeffg = np.dot(A_inv , Qg) 
        coeffb = np.dot(A_inv , Qb) 

        red= np.dot(input_vec,coeffr)
        green= np.dot(input_vec,coeffg)
        blue= np.dot(input_vec,coeffb)
        gray[x][y]=[red,green,blue]
    except:
        Q = np.array( [[gray[x-neigh ][ y-neigh]] ,                 # pixel value
                       [gray[x+neigh ][ y-neigh]] ,
                       [gray[x-neigh ][ y+neigh]] ,
                       [gray[x+neigh ][ y+neigh]] ] )


        A_inv = np.linalg.inv(A)                                            # pseudo inverse of A
        input_vec = np.array([x , y , x * y , 1])                           # coordinates x , y in vector

        coeffr = np.dot(A_inv , Q)                                           # coeff matrix
        
        gray[x][y]= np.dot(input_vec,coeffr)
        
#    gray[x][y]=0


def click_event(event, x, y, flags, params): 
  
    # checking for mouse movement
    if event == cv2.EVENT_MOUSEMOVE: 

        interpolate(y,x)
        interpolate(y+1,x+1)
        interpolate(y-1,x+1)
        interpolate(y+1,x-1)
        interpolate(y-1,x-1)
        interpolate(y+1,x)
        interpolate(y,x+1)
        interpolate(y-1,x)
        interpolate(y,x-1)
        
        cv2.imshow('image', gray) 


cv2.imshow('image', gray) 
cv2.setMouseCallback('image', click_event)

# wait for a key to be pressed to exit 
cv2.waitKey(0) 
cv2.imwrite('clean.png', gray)
# close the window 
cv2.destroyAllWindows() 

