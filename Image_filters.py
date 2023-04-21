from PIL import Image
def main():
    ###takes input of the path from the user
    try:
        image_path = input('Please input the path of your image.8').strip()
        image = Image.open(image_path)
    except:
        print('Path does not exist')
    ###stores the number of rows and columns in the image
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


    ###this list consists of the operations that can be performed on the image
    operations = ['flip image', 'color sorting filter', 'emboss filter','grayscale filter', 'edge detection filter', 'blur filter']

    ###Provides user with a list of options
    print('From the given list of operations, choose the number corresponding to the operation you want to perform.')
    for i in range(len(operations)):
        print(f'{i+1} : {operations[i]}')
    

    ###Takes option from user, validates input
    option = input('Type your option.')
    while not option.isdigit() or int(option) < 1 or int(option) > len(operations):
        option = input('Incorrect option. Please try again!')

    option = int(option)

    if option == 1:
        new_image = flip_image(image_list)

    elif option == 2:
        new_image = color_sorting_filter(image_list)

    elif option == 3:
        new_image = emboss_filter(image_list)

    elif option == 4:
        new_image = grayscale_filter(image_list)

    elif option == 5:
        new_image = edge_detection_filter(image_list)

    elif option == 6:
        new_image = blur_filter(image_list)

    new_width = len(new_image[0])
    new_height = len(new_image)

    ###creating the edited image
    final_image = Image.new('RGB', (new_width, new_height))

    for y in range(height):
        for x in range(width):
            final_image.putpixel((x,y), new_image[y][x])

    ###show the new image
    final_image.show()

###digital image processing 
image = [[23,45,78], [43,76,90], [80,56,43], [32,54,67]]
###The push function pushes an item onto the stack's end
def push(stack, item):
    stack.append(item)


###The pop function removes the last item of the stack and also returns it.
def pop(stack):
    x = stack.pop(-1)
    return x


###The is_empty function returns True if the stack is empty, returns False otherwise
def is_empty(stack):
    if len(stack) == 0:
        return True
    return False


###Given a list, this function returns a flipped list, using a stack
def flip_list(lst):
    stack = []
    new_list = []
    for i in range(len(lst)):
        push(stack, lst[i])
    
    while not is_empty(stack):
        new_list.append(pop(stack))

    return new_list


###This function will flip the image using a stack
def flip_image(image):

    ###flip the rows first
    image = flip_list(image) 

    ###then flip each column 
    for i in range(len(image)):
        image[i] = flip_list(image[i])
          
    return image    


###The following functions are each separate filters

def color_sorting_filter(image):
    pass

def apply_kernel(image_part, kernel_part):
    ###initialising the new values of each of the colors in the pixel
    pixel_r = pixel_g = pixel_b = 0

    for m in range(len(image_part)):
        for n in range(len(image_part[0])):
            ###updating each of the color components of the image
            pixel_r += image_part[m][n][0] * kernel_part[m][n]
            pixel_g += image_part[m][n][1] * kernel_part[m][n]
            pixel_b += image_part[m][n][2] * kernel_part[m][n]

    ###ensuring that the color components remain within 255, which is the max range of colors
    pixel_r = min(255, pixel_r)
    pixel_g = min(255, pixel_g)
    pixel_b = min(255, pixel_b)

    return (pixel_r, pixel_g, pixel_b, 255)

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

            kernel_part = [s[kernel_left:kernel_right] for s in kernel[kernel_up:kernel_down]]

            new_pixel = apply_kernel(image_part, kernel_part)
            new_row.append(new_pixel)
        
        embossed_image.append(new_row)
            #print(image_part)
            #print(kernel_part)
            #print('\n\n')
    return embossed_image


def grayscale_filter(image):
    pass

def edge_detection_filter(image):
    pass

def blur_filter(image):
    pass

def grayscale_to_color(image):
    pass

#print(flip_image(image))

main()