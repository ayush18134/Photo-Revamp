INTRODUCTION

After a century of black and white cameras, the
first coloured cameras were invented and
brought into public use around the 1950s, yet
black and white cameras were prominent until the
late 20th century. This has left us with a hundred
and fifty years of grayscale photographs. Some of
these photographs capture important historical
events like “The Solvay Conference of 1927”.
Colourization is also done for personal old
photographs to relive the memories of old time.
This created a demand for specialized designers
that colourized images manually in tools like
gimp, for which designers have to be paid and
significant time in order of hours is required,
therefore it was not accessible to the common
public economically. After computers became fast
and accessible, many researchers have come up
with automated solutions as opposed to manual
colourization. For revamping an old ripped off
photo, we have to first remove the ripped off
portion of the image and then colourize it. For
removing the noise due to the ripped off section,
there are certain deep learning algorithms but
these models require a lot of computation power
and are not cost efficient. The best possible
method to do this task is to use the method of
bilinear interpolation. For the colourization of the
black and white image, there are many different
methods available. Out of all the methods, Neural
networks give us the best desired output. Some of
the most popular works using neural networks are
Iizuka, Serra and Ishikawa (2016, p. 1) and
Zhang, Isola and Efros (2016, p.649). The most
successful of these neural networks are
Convolutional Neural Networks (CNN) which
have become the starting point of image
processing in most of the machine learning
models with images as input. For our project, we have used the model given by zhang to colourize
the black and white image.

METHODS

    A. Stitching/Restoration of image
  This process uses the input coordinates
  given by the user and then interpolate the
  pixels present at these coordinates to get
  the stitched output. Though, interpolating
  only one pixel at time may produce better
  result but it’s becomes time consuming for
  restoring the high resolution images.
  Hence, we optimized our algorithm to
  stitch/interpolate 9 or more at once. As
  expected, this made the task a faster.
    
    B. Colorization of black and white images
  We used the technique given by Zhang to
  colourize black and white images. We
  know that an image can be represented in
  both RGB and LAB colour models. We
  will make use of the LAB colour model
  for the training and testing purpose.
  
  ● For getting our result, we will
    convert the image to LAB format
    and then use the L component as
    input to our model. The model will
    predict the AB components. After
    combination of all the 3
    components, we can get our final
    output.
    
  ● For training, we will use a dataset
    of coloured images. We will
    convert the coloured images from
    RGB to LAB and then do
    supervised learning in which L will
    be the training input and AB will
    be the labels. After training our
    model will be ready to convert the
    black and white images to the
    coloured version. The neural
    network used was the one proposed
    by Zhang.
 
CONCLUSIONS

We have proposed an application that can
handle complex image processing tasks of
restoring and colorizing an old black and
white image with minimal user
intervention. Generally, these tasks are
done by professionals or photo editing labs
and it is a very time consuming task even
for the professionals. Therefore, the
proposed application will empower the
user to do restoration and colorization of
any image very quickly and even without
any prior knowledge of image processing.
Moreover, such software will also be an
useful application for revamping historical
paintings and photographs.

Model used- Since the size of model is very large, I could not upload it on github. Here is the link to download it
http://colorization.eecs.berkeley.edu/siggraph/models/model.caffemodel

REFERENCE

[1] Zhang, R., Zhu, J.Y., Isola, P., Geng,
X., Lin, A.S., Yu, T. and Efros, A.A.,
2017. Real-time user-guided image
colorization with learned deep priors.
arXiv preprint arXiv:1705.02999.

[2] Colorizing B&W Photos with Neural
Networks

Special thanks to Jun-Yan Zhu
