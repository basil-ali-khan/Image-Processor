"""
REFERENCES:
https://github.com/accord-net/java/blob/master/Catalano.Image/src/Catalano/Imaging/Filters/Emboss.java
https://www.youtube.com/watch?v=YXPyB4XeYLA&t=10455s
https://sbme-tutorials.github.io/2018/cv/notes/4_week4.html#:~:text=and%20pepper%20noise.-,Edge%20detection%20kernels,algorithms%20will%20discussed%20in%20details.
https://datacarpentry.org/image-processing/06-blurring/#:~:text=When%20we%20blur%20an%20image,other%20tasks%20such%20as%20thresholding.


"""

from tkinter import *
from tkinter import filedialog 
from PIL import ImageTk, Image
import math

newimage = None
previous = None
def fileselect():
    global originalfile
    global newimage
    newimage = None
    originalfile = filedialog.askopenfilename(initialdir="/", title="Select a file", filetypes=((".PNG", "*.png"), (".JPG", "*.jpg"), ("All Files", '*.*')))
    if originalfile:
        viewbuttonO = Button(root, text="View Original", command=viewOriginal,bg="#08A045",padx=28, pady=5).place(x=10,y=125)
        viewbuttonE = Button(root, text="View Edited", state=DISABLED,bg="#08A045",padx=35,pady=5).place(x=150,y=125)
        undoButton = Button(root, text="Undo", state=DISABLED,bg="#08A045",padx=23, pady=5).place(x=3,y=163)
        saveButton = Button(root, text="Save Edited", state=DISABLED,bg="#08A045",padx=14, pady=5).place(x=90, y=163)
        flipVButton = Button(root, text="Flip Vertically", command=flippedV,bg="#08A045",padx=30, pady=5).place(x=150, y=5)
        flipHButton = Button(root, text="Flip Horizontally", command=flippedH,bg="#08A045",padx=20, pady=5).place(x=10, y=5)
        grayButton = Button(root, text="Grayscale Filter", command=grayscale,bg="#08A045",padx=23, pady=5).place(x=10, y=85)
        embossButton = Button(root, text="Emboss Filter", command=emboss,bg="#08A045",padx=10, pady=5).place(x=5, y=45)
        edgedetectButton = Button(root, text="Edge Detect Filter", command=edgedetect,bg="#08A045",padx=20, pady=5).place(x=150, y=85)
        blurButton = Button(root, text="Blur Filter", command=blur,bg="#08A045",padx=10, pady=5).place(x=115, y=45)
        coloursortButton = Button(root, text="Colour Sort", command=coloursort,bg="#08A045",padx=10, pady=5).place(x=205, y=45)

#helper functions
def viewOriginal():
    image = Image.open(originalfile)
    image.show()
def viewEdited():
    global newimage
    newimage.show()
def apply_kernel(image_part, kernel_part):
    ###initialising the new values of each of the colors in the pixel
    pixel_r = pixel_g = pixel_b = 0

    for m in range(len(image_part)):
        for n in range(len(image_part[0])):
            ###updating each of the color components of the image
            pixel_r += image_part[m][n][0] * kernel_part[m][n]
            pixel_g += image_part[m][n][1] * kernel_part[m][n]
            pixel_b += image_part[m][n][2] * kernel_part[m][n]
    ###ensuring that the color components remain within 0-255, which is the max range of colors
    pixel_r = max(0, min(255, int(pixel_r)))
    pixel_g = max(0, min(255, int(pixel_g)))
    pixel_b = max(0, min(255, int(pixel_b)))

    return (pixel_r, pixel_g, pixel_b, 255)


###This will push an item to the top of the stack
def push(stack, item):
    stack.append(item)


#The pop function removes the last item of the stack and also returns it.
def pop(stack):
    x = stack.pop(-1)
    return x


#The is_empty function returns True if the stack is empty, returns False otherwise
def is_empty(stack):
    if len(stack) == 0:
        return True
    return False


#Given a list, this function returns a flipped list, using a stack
def flip_list(lst):
    stack = []
    new_list = []
    for i in range(len(lst)):
        push(stack, lst[i])
    
    while not is_empty(stack):
        new_list.append(pop(stack))

    return new_list

###This helper function will be used in color-sorting, given a tuple in the form of (r,g,b,255), it returns the sum of the pixel's RGB components
def sum_of_pixels(tup):
    return tup[0] + tup[1] + tup[2]


###The merge sort algorithm will be used to sort the image pixels on the basis of the sum of their RGB components
def merge(left, right, lst):
    i = j = 0
    while i + j < len(lst):
        if j == len(right) or (i < len(left) and sum_of_pixels(left[i]) < sum_of_pixels(right[j])):
            lst[i + j] = left[i]
            i += 1
        else:
            lst[i + j] = right[j]
            j += 1

def merge_sort(image):
    if len(image) < 2:
        return image
    
    left = image[:(len(image) // 2)]
    right = image[(len(image) // 2):]

    merge_sort(left)
    merge_sort(right)

    #lst = []
    merge(left, right, image)



#creating the edited image
def create(image):    
    width = len(image[0])
    height = len(image)
    final_image = Image.new('RGB', (width, height))
    for y in range(height):
        for x in range(width):
            final_image.putpixel((x,y), image[y][x])
    return final_image


###convert image to a 2D list
def process(image):
    width, height = image.size
    image_list = []  ###2D list to be created from image for processing    
    ###iterating over rows
    for r in range(height):
        row = []

        ###iterating over columns
        for c in range(width):

            ###getting the pixel at the rth row and cth column and appending it to the new row
            pixel = image.getpixel((c,r))
            row.append(pixel)
        
        ###appending the new row the 2D list
        image_list.append(row)
    return image_list


#filter functions


#This function will flip the image using a stack
def flip_image(image):

    ###flip the rows first
    image = flip_list(image) 

    ###then flip each column 
    for i in range(len(image)):
        image[i] = flip_list(image[i])
          
    return image  


def grayscale_filter(image):
    ###this involves finding the average of the RGB values and then replacing the RGB components with the average
    grayed_image = []

    for r in range(len(image)):
        grayed_row = []
        for c in range(len(image[0])):
            ###accessing current pixel to be processed
            current_pixel = image[r][c]   

            ###Finding average
            average = math.floor((current_pixel[0] + current_pixel[1] + current_pixel[2]) / 3)

            ###Appending new pixel to the row
            grayed_row.append((average, average, average, 255))

        ###appending new row to the image
        grayed_image.append(grayed_row)

    return grayed_image


def emboss_filter(image):
    embossed_image = []
    kernel = [[-2, -1, 0], [-1, 1, 1], [0, 1, 2]]

    for row in range(len(image)):
        new_row = []
        for col in range(len(image[row])):

            current_pixel = image[row][col]

            ###setting the indexes of the part of image that needs to be convoluted
            up_index = row - 1
            down_index = row + 2
            left_index = col - 1
            right_index = col + 2

            if up_index < 0:
                up_index = 0
            if down_index > len(image):
                down_index = len(image)
            if left_index < 0:
                left_index = col
            if right_index > len(image[0]):
                right_index = len(image[0])

            ###part of image that will be taken for convolution in this iteration:
            image_part = [r[left_index:right_index] for r in image[up_index:down_index]]

            ###setting indexes of part of kernel that will be used
            kernel_up = 1 - (row - up_index)
            kernel_down = 1 + (down_index - row)
            kernel_left = 1 - (col - left_index)
            kernel_right = 1 + (right_index - col)

            ###part of kernel to be taken for convolution in ongoing iteration
            kernel_part = [s[kernel_left:kernel_right] for s in kernel[kernel_up:kernel_down]]

            ###new pixel generated after applying the kernel
            new_pixel = apply_kernel(image_part, kernel_part)


            new_row.append(new_pixel)

        embossed_image.append(new_row) 

    return embossed_image


def edge_detection_filter(image):
    '''
    In this filter, two kernels are applied, one is in the x-direction and the other is in the y-direction. The resultant of the results of the
    two are then the value of the final pixel.
    '''
    kernel_x = [[-1,0,1],[-1,0,1],[-1,0,1]]
    kernel_y = [[-1,-1,-1],[0,0,0],[1,1,1]]

    new_image = []

    for row in range(len(image)):
        new_row = []
        for col in range(len(image[0])):

            current_pixel = image[row][col]

            ###setting the indexes of the part of image that needs to be convoluted
            up_index = row - 1
            down_index = row + 2
            left_index = col - 1
            right_index = col + 2

            if up_index < 0:
                up_index = 0
            if down_index > len(image):
                down_index = len(image)
            if left_index < 0:
                left_index = col
            if right_index > len(image[0]):
                right_index = len(image[0])

            ###part of image that will be taken for convolution in this iteration:
            image_part = [r[left_index:right_index] for r in image[up_index:down_index]]

            ###setting indexes of part of kernel that will be used
            kernel_up = 1 - (row - up_index)
            kernel_down = 1 + (down_index - row)
            kernel_left = 1 - (col - left_index)
            kernel_right = 1 + (right_index - col)

            ###part of kernel_x to be applied in x-direction
            kernel_part_x = [s[kernel_left:kernel_right] for s in kernel_x[kernel_up:kernel_down]]
            
            ###part of kernel_y to be applied in y-direction
            kernel_part_y = [s[kernel_left:kernel_right] for s in kernel_y[kernel_up:kernel_down]]

            ###pixel returned after applying kernel_x
            new_pixel_x = apply_kernel(image_part, kernel_part_x)
            
            ###pixel returned after applying kernel_y
            new_pixel_y = apply_kernel(image_part, kernel_part_y)

            ###finding final pixel
            final_pixel = []
            for k in range(3):
                ###The resultant final pixel is the square root of the sum of the squares of the pixels returned after applying both kernels.
                component = math.floor(math.sqrt(new_pixel_x[k]**2 + new_pixel_y[k]**2))
                final_pixel.append(component)

            ###Appending 255 to complete the tuple for the 255 color image
            final_pixel.append(255)
            
            ###adding the pixel to the new row
            new_row.append(tuple(final_pixel))

        ###adding the new row the final image
        new_image.append(new_row)
        
    return new_image


def blur_filter(image):
    blurred_image = []
    kernel = [[1/16,1/8,1/16], [1/8,1/4,1/8], [1/16,1/8,1/16]]

    for row in range(len(image)):
        new_row = []
        for col in range(len(image[0])):

            current_pixel = image[row][col]

            ###setting the indexes of the part of image that needs to be convoluted
            up_index = row - 1
            down_index = row + 2
            left_index = col - 1
            right_index = col + 2

            if up_index < 0:
                up_index = 0
            if down_index > len(image):
                down_index = len(image)
            if left_index < 0:
                left_index = col
            if right_index > len(image[0]):
                right_index = len(image[0])

            ###part of image that will be taken for convolution in this iteration:
            image_part = [r[left_index:right_index] for r in image[up_index:down_index]]

            ###setting indexes of part of kernel that will be used
            kernel_up = 1 - (row - up_index)
            kernel_down = 1 + (down_index - row)
            kernel_left = 1 - (col - left_index)
            kernel_right = 1 + (right_index - col)

            kernel_part = [s[kernel_left:kernel_right] for s in kernel[kernel_up:kernel_down]]

            new_pixel = apply_kernel(image_part, kernel_part)
            new_row.append(new_pixel)
        
        blurred_image.append(new_row)
            
    return blurred_image


def mirror_image(image):
    mirrored_image = []
    for i in image:
        ###passing each row as parameter to the flip_list function, that returns that row as a flipped version of its original self using a stack
        mirrored_image.append(flip_list(i))

    return mirrored_image


def color_sorting_filter(image):
    width = len(image[0])
    height = len(image)

    sorted_image = []
    image_1D = []  ###converting 2D image list to 1D, to make sorting easier
    for r in range(height):
        for c in range(width):
            image_1D.append(image[r][c])

    merge_sort(image_1D)

    counter = 0
    for y in range(height):
        new_row = []

        for x in range(width):
            new_row.append(image_1D[counter])
            counter += 1
        
        sorted_image.append(new_row)

    return sorted_image


#button commands

def save():
    global newimage
    filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPG", "*.jpg")])
    if filename:
        newimage.save(filename)
    
    
def undo():
    global newimage
    global previous
    newimage = previous
    undoButton = Button(root, text="Undo", state=DISABLED,bg="#08A045",padx=23, pady=5).place(x=3,y=163)


def flippedH():
    global newimage
    global previous
    editedfile = newimage
    if editedfile != None:  
        image = editedfile
        previous = newimage
        undoButton = Button(root, text="Undo", command=undo,bg="#08A045",padx=23, pady=5).place(x=3,y=163)
    else:
        image = Image.open(originalfile)
    image = process(image)
    newimage = mirror_image(image)
    newimage = create(newimage)
    viewbuttonE = Button(root, text="View Edited", command=viewEdited,bg="#08A045",padx=35,pady=5).place(x=150,y=125)
    saveButton = Button(root, text="Save Edited", command=save,bg="#08A045",padx=14, pady=5).place(x=90, y=163)


def blur():
    global newimage
    global previous
    editedfile = newimage
    if editedfile != None:  
        image = editedfile
        previous = newimage
        undoButton = Button(root, text="Undo", command=undo,bg="#08A045",padx=23, pady=5).place(x=3,y=163)
    else:
        image = Image.open(originalfile)
    image = process(image)
    newimage = blur_filter(image)
    newimage = create(newimage)
    viewbuttonE = Button(root, text="View Edited", command=viewEdited,bg="#08A045",padx=35,pady=5).place(x=150,y=125)
    saveButton = Button(root, text="Save Edited", command=save,bg="#08A045",padx=14, pady=5).place(x=90, y=163)


def emboss():
    global newimage
    global previous
    editedfile = newimage
    if editedfile != None:  
        image = editedfile
        previous = newimage
        undoButton = Button(root, text="undo", command=undo,bg="#08A045",padx=23, pady=5).place(x=3,y=163)
    else:
        image = Image.open(originalfile)
    image = process(image)
    newimage = emboss_filter(image)
    newimage = create(newimage)
    viewbuttonE = Button(root, text="View Edited", command=viewEdited,bg="#08A045",padx=35,pady=5).place(x=150,y=125)
    saveButton = Button(root, text="Save Edited", command=save,bg="#08A045",padx=14, pady=5).place(x=90, y=163)


def edgedetect():
    global newimage
    global previous
    editedfile = newimage
    if editedfile != None:  
        image = editedfile
        previous = newimage
        undoButton = Button(root, text="undo", command=undo,bg="#08A045",padx=23, pady=5).place(x=3,y=163)
    else:
        image = Image.open(originalfile)
    image = process(image)
    newimage = edge_detection_filter(image)
    newimage = create(newimage)
    viewbuttonE = Button(root, text="View Edited", command=viewEdited,bg="#08A045",padx=35,pady=5).place(x=150,y=125)
    saveButton = Button(root, text="Save Edited", command=save,bg="#08A045",padx=14, pady=5).place(x=90, y=163)


def grayscale():
    global newimage
    global previous
    editedfile = newimage
    if editedfile != None:  
        image = editedfile
        previous = newimage
        undoButton = Button(root, text="undo", command=undo,bg="#08A045",padx=23, pady=5).place(x=3,y=163)
    else:
        image = Image.open(originalfile)
    image = process(image)
    newimage = grayscale_filter(image)
    newimage = create(newimage)
    viewbuttonE = Button(root, text="View Edited", command=viewEdited,bg="#08A045",padx=35,pady=5).place(x=150,y=125)
    saveButton = Button(root, text="Save Edited", command=save,bg="#08A045",padx=14, pady=5).place(x=90, y=163)


def flippedV():
    global newimage
    global previous
    editedfile = newimage
    if editedfile != None:  
        image = editedfile
        previous = newimage
        undoButton = Button(root, text="Undo", command=undo,bg="#08A045",padx=23, pady=5).place(x=3,y=163)
    else:
        image = Image.open(originalfile)
    image = process(image)
    newimage = flip_image(image)
    newimage = create(newimage)
    viewbuttonE = Button(root, text="View Edited", command=viewEdited,bg="#08A045",padx=35,pady=5).place(x=150,y=125)
    saveButton = Button(root, text="Save Edited", command=save,bg="#08A045",padx=14, pady=5).place(x=90, y=163)


def coloursort():
    global newimage
    global previous
    editedfile = newimage
    if editedfile != None:  
        image = editedfile
        previous = newimage
        undoButton = Button(root, text="Undo", command=undo,bg="#08A045",padx=23, pady=5).place(x=3,y=163)
    else:
        image = Image.open(originalfile)
    image = process(image)
    newimage = color_sorting_filter(image)
    newimage = create(newimage)
    viewbuttonE = Button(root, text="View Edited", command=viewEdited,bg="#08A045",padx=35,pady=5).place(x=150,y=125)
    saveButton = Button(root, text="Save Edited", command=save,bg="#08A045",padx=14, pady=5).place(x=90, y=163)

root = Tk()
root.geometry("300x200")
root.title("Photo Manipulation")
root.configure(bg="#D3F3EE")
browse = Button(root, text="Browse Images", command=fileselect, bg="#08A045", padx=10, pady=5).place(x=190, y=163)
viewbuttonO = Button(root, text="View Original", state=DISABLED, bg="#08A045",padx=28, pady=5).place(x=10,y=125)
viewbuttonE = Button(root, text="View Edited", state=DISABLED,bg="#08A045",padx=35,pady=5).place(x=150,y=125)
undoButton = Button(root, text="Undo", state=DISABLED,bg="#08A045",padx=23, pady=5).place(x=3,y=163)
saveButton = Button(root, text="Save Edited", state=DISABLED,bg="#08A045",padx=14, pady=5).place(x=90, y=163)
flipVButton = Button(root, text="Flip Vertically", state=DISABLED,bg="#08A045",padx=30, pady=5).place(x=150, y=5)
flipHButton = Button(root, text="Flip Horizontally", state=DISABLED,bg="#08A045",padx=20, pady=5).place(x=10, y=5)
grayButton = Button(root, text="Grayscale Filter", state=DISABLED,bg="#08A045",padx=23, pady=5).place(x=10, y=85)
embossButton = Button(root, text="Emboss Filter", state=DISABLED,bg="#08A045",padx=10, pady=5).place(x=5, y=45)
edgedetectButton = Button(root, text="Edge Detect Filter", state=DISABLED,bg="#08A045",padx=20, pady=5).place(x=150, y=85)
blurButton = Button(root, text="Blur Filter", state=DISABLED,bg="#08A045",padx=10, pady=5).place(x=115, y=45)
coloursortButton = Button(root, text="Colour Sort", state=DISABLED,bg="#08A045",padx=10, pady=5).place(x=205, y=45)

root.mainloop()

# name = filedialog.askopenfilename(initialdir="/", title="Select a file", filetypes=((".PNG", "*.png"), (".JPG", "*.jpg"), ("All Files", '*.*')))
# image = Image.open(name)
# image.show()