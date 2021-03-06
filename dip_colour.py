# -*- coding: utf-8 -*-
"""dip_colour.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1axHR-xtcyK2tylFC4TTtnTqr78uK6r2F

Use this to discard all changes and reset
"""

from google.colab import drive
drive.mount('/content/drive')

ls

#!kill -9 -1

"""Uncomment all 'deb-src' lines to allow apt to download source code for dependencies"""

with open('/etc/apt/sources.list') as f:
  txt = f.read()
with open('/etc/apt/sources.list.backup', 'w') as f:
  f.write(txt)
with open('/etc/apt/sources.list', 'w') as f:
  f.write(txt.replace('# deb-src','deb-src'))

"""Update apt 

Install dependencies for Caffe with CUDA

Install g++-5: this is a way to make g++, nvcc and boost work together
"""

!apt update
!apt build-dep caffe-cpu
!apt install g++-5

"""Download sources for boost

Unpack boost
"""

!wget https://dl.bintray.com/boostorg/release/1.67.0/source/boost_1_67_0.tar.bz2
!tar --bzip2 -xf boost_1_67_0.tar.bz2

"""Set g++-5 and gcc-5 as default compiles: we're gonna use them to compile both boost and Caffe """

!update-alternatives --remove-all gcc 
!update-alternatives --remove-all g++

!update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-5 20
!update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-5 20

!update-alternatives --install /usr/bin/cc cc /usr/bin/gcc 30
!update-alternatives --set cc /usr/bin/gcc

!update-alternatives --install /usr/bin/c++ c++ /usr/bin/g++ 30
!update-alternatives --set c++ /usr/bin/g++

"""Compile and install boost"""

!cd boost_1_67_0 && ./bootstrap.sh --exec-prefix=/usr/local --with-libraries=system,filesystem,regex,thread,python \
--with-python-version=2.7 --with-python-root=/usr
!cd boost_1_67_0 && ./b2 install

"""Clone Caffe from github, checkout SSD branch"""

!git clone https://github.com/weiliu89/caffe.git && cd caffe && git checkout ssd

"""Configure makefile:

- Set path to CUDA
- Set BLAS option
- Set opencv version 3
- Add Python layer (just in case)
- Add some unrecognized paths to hdf5 and numpy
"""

with open('caffe/Makefile.config.example') as f:
  config = f.read()
  
comment = ['CUDA_DIR := /usr/local/cuda', 
           'BLAS := open']
uncomment = ['# CUDA_DIR := /usr', 
             '# BLAS := atlas', 
             '# OPENCV_VERSION := 3', '# WITH_PYTHON_LAYER := 1'] #
replace = [('INCLUDE_DIRS := $(PYTHON_INCLUDE) /usr/local/include',
            'INCLUDE_DIRS := $(PYTHON_INCLUDE) /usr/local/include /usr/include/hdf5/serial /usr/local/lib/python2.7/dist-packages/numpy/core/include/'), 
           ('LIBRARY_DIRS := $(PYTHON_LIB) /usr/local/lib /usr/lib',
            'LIBRARY_DIRS := $(PYTHON_LIB) /usr/local/lib /usr/lib /usr/lib/x86_64-linux-gnu/hdf5/serial')]

for c in uncomment:
  config = config.replace(c, c[2:])
for c in comment:
  config = config.replace(c, '# '+c)
for c1,c2 in replace:
  config = config.replace(c1, c2)
  
with open('caffe/Makefile.config', 'w') as f:
  f.write(config)

"""Replace '-isystem' in Makefile by '-I' to prevent errors with locating stdlib: adopted from https://github.com/Martchus/tageditor/issues/22"""

with open('caffe/Makefile') as f:
  mfile = f.read()
  
with open('caffe/Makefile.backup', 'w') as f:
  f.write(mfile)
  
with open('caffe/Makefile', 'w') as f:
  f.write(mfile.replace('-isystem','-I'))

"""Magic thing to avoid errors with nan-related types: adopted from 

https://stackoverflow.com/questions/47200632/caffe-installation-gcc-error-namespace-std-has-no-member-isnan
"""

with open('/usr/include/x86_64-linux-gnu/c++/5/bits/c++config.h') as f:
  txt = f.read()
with open('/usr/include/x86_64-linux-gnu/c++/5/bits/c++config.h', 'w') as f:
  f.write(txt.replace('/* #undef _GLIBCXX_USE_C99_MATH */',
                      '/* #undef _GLIBCXX_USE_C99_MATH */\n#define  _GLIBCXX_USE_C99_MATH  1'))

"""Now actually make Caffe, python interface and tests"""

!cd caffe && make all -j4 && make pycaffe && make test -j8 && make distribute

"""Add path with installed libs (namely boost and caffe) to configs"""

!echo /usr/local/lib >> /etc/ld.so.conf && ldconfig
!echo /content/caffe/distribute/lib >> /etc/ld.so.conf && ldconfig

ls

"""We are ready to test Caffe!"""

ls

!python RippedImageRepair.py

cd dip_color

cd 'drive/My Drive/dip_color'

!cp -r caffe /content/drive/MyDrive/Content_for_colab



import matplotlib.pyplot as plt
import numpy as np
import cv2
import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage import color
from sklearn.cluster import KMeans
import os
from scipy.ndimage.interpolation import zoom
sys.path.insert(0, "/content/caffe/python")
import caffe

pts_in_hull = np.load('pts_in_hull.npy')


caffe.set_mode_cpu()
net = caffe.Net("proto.prototxt", "model.caffemodel", caffe.TEST)

if (len(net.params['pred_ab'][0].data[...].shape) == 4 and net.params['pred_ab'][0].data[...].shape[1] == 313):
    net.params['pred_ab'][0].data[:, :, 0, 0] =pts_in_hull.T

for layer in net._layer_names:
    if layer[-3:] == '_us':
        net.params[layer][0].data[:, 0, :, :] = np.array(((.25, .5, .25, 0), (.5, 1., .5, 0), (.25, .5, .25, 0), (0, 0, 0, 0)))[np.newaxis, :, :]

        
# im = cv2.cvtColor(cv2.imread("/stone.jpg", 1), cv2.COLOR_BGR2RGB)
im = cv2.cvtColor(cv2.imread("/didi.png", 1), cv2.COLOR_BGR2RGB)
img_rgb_fullres = im.copy()
Xfullres = img_rgb_fullres.shape[0]
Yfullres = img_rgb_fullres.shape[1]
img_lab_fullres = color.rgb2lab(img_rgb_fullres).transpose((2, 0, 1))
img_l_fullres = img_lab_fullres[[0], :, :]
img_ab_fullres = img_lab_fullres[1:, :, :]
im = cv2.resize(im, (256, 256))
img_rgb = im.copy()
img_lab = color.rgb2lab(img_rgb).transpose((2, 0, 1))
img_l = img_lab[[0], :, :]
img_ab =img_lab[1:, :, :]
img_lab_mc = img_lab / np.array((1., 1., 1.))[:, np.newaxis, np.newaxis]-np.array((50./ 1., 0./ 1.,0./1.))[:, np.newaxis, np.newaxis]
img_l_mc =img_lab_mc[[0], :, :]
 


input_mask = np.zeros((1,256,256)) 
input_ab = np.zeros((2,256,256)) 
input_ab_mc = (input_ab - 0.)/ 1.
input_mask_mult = input_mask*110.



net_input_prepped = np.concatenate((img_l_mc, input_ab_mc, input_mask_mult), axis=0)
net.blobs['data_l_ab_mask'].data[...] = net_input_prepped
net.forward()

def lab2rgb_transpose(img_l, img_ab):
    pred_lab = np.concatenate((img_l, img_ab), axis=0).transpose((1, 2, 0))
    pred_rgb = (np.clip(color.lab2rgb(pred_lab), 0, 1) * 255).astype('uint8')
    return pred_rgb

pred_lab = np.concatenate((img_l, net.blobs['pred_ab'].data[0, :, :, :]), axis=0).transpose((1, 2, 0))
output_rgb = (np.clip(color.lab2rgb(pred_lab), 0, 1) * 255).astype('uint8')

output_lab = color.rgb2lab(output_rgb).transpose((2, 0, 1))
output_ab = output_lab[1:, :, :]

zoom_factor = (1, 1.*img_l_fullres.shape[1] /output_ab.shape[1], 1. *img_l_fullres.shape[2]/output_ab.shape[2])
output_ab_fullres = zoom(output_ab, zoom_factor, order=1)

img_out_fullres= lab2rgb_transpose(img_l_fullres, output_ab_fullres)


plt.figure(figsize=(21,9))
plt.imshow(img_out_fullres)

