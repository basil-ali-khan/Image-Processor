# DSA-Spring-2023-Project
Image Processor

Idea
This project will involve accessing images in python, and then applying various
filters to them or rotating them.

Why Is This Novel?
1. We are using stacks to rotate images, rather than using the conventional
method of iterating over the nested list of pixels in backward direction 2. We
will create our own kernels for the filters rather than the built-in convolution
functions of python.

Data Structure Used
1. Nested Lists
2. Stacks

Algorithm Used
Merge Sort

Application Details

The project will involve flipping and mirroring an image using stack and applying various
filters to the image.
1. For the flipping and mirroring part, we will use the push and pop operations of the stack
to flip the sequence of pixels in an image.
2. For the filters part, our project will involve a combination of filters that can
be applied to the image.
i. Color Sorting Filter: Merge sort will be used to sort pixels based on
their red, green and blue values. This will help create a gradient image.
ii. Emboss Filter: Give an image a 3D look by applying an emboss filter
that highlights the edges and contours of the image.
iii. Grayscale Filter: Convert a color image to a grayscale image by setting
the red, green, and blue values of each pixel to the average of their original
values.
iv. Edge Detection Filter: Detect the edges in an image by finding the
pixels with the highest contrast between neighboring pixels.
v. Blur Filter: Blur an image by averaging the values of neighboring pixels
to create a soft, blurred effect.
3. User can input whether he wants to rotate the image or apply a filter. In the
case of a filter, the user can select which filter(s) he wants to apply.

User Interface will be created for users to browse images, apply filters, view edited images and undo changes.
