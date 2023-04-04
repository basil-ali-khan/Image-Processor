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
    for i in lst:
        push(stack, i)
    
    while not is_empty(stack):
        new_list.append(pop(stack))

    return new_list


###This function will flip the image using a stack
def flip_image(image):
    image = flip_list(image)
    for i in range(len(image)):
        image[i] = flip_list[i]
          
    return image    


###The following functions are each separate filters

def color_sorting_filter(image):
    pass

def emboss_filter(image):
    pass

def grayscale_filter(image):
    pass

def edge_detection_filter(image):
    pass

def blur_filter(image):
    pass

