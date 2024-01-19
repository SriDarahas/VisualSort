import pygame
import random # To generate a random list of array to sort
import math
pygame.init()

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 240, 240, 240
    GREEN = 0, 255, 0
    COLUMBIA_BLUE = 204, 221, 226
    BACKGROUND_COLOR = BLACK
    TITLE_COLOR = 0, 128, 128
    TEXT_COLOR = 204, 221, 226

    # GRADIENTS = [(137, 207, 240), (0, 150, 255), (25, 25, 112)]
    GRADIENTS = [(202, 210, 197), (132, 169, 140), (82, 121, 111)]

    FONT = pygame.font.SysFont('timesnewroman', 20)
    LARGE_FONT = pygame.font.SysFont('timesnewroman', 24)

    SIDE_PAD = 100 # Left and Right Padding on the screen. 50px on the left and 50px on the right.
    TOP_PAD = 150 # Top padding of the screen to leave something written on the screen.

    # Initializing Function for th DrawInformation Class.
    # Whenever we call DrawInformation Class we need to pass the arguments in the initializing function; here i.e. width, height, lst
    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        # Setting up the window using pygame.display.set_mode((tuples))
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        # block_width is width of a single bar which depends on the number of bars to be sorted in the list.
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))

        #block_height is the height of a single bar which depends on the range of numbers that we have on the list
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))

        # start_x is the starting position of the first bar; i.e. SIDE_PAD / 2
        self.start_x = self.SIDE_PAD // 2

def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst

def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'ASCENDING' if ascending else 'DESCENDING'}", 1, draw_info.TITLE_COLOR)
    draw_info.window.blit(title, ((draw_info.width / 2) - (title.get_width()/2), 10))

    controls = draw_info.FONT.render("R - Reset | A - Ascending | D - Descending | SPACE - Start Sorting", 1, draw_info.TEXT_COLOR)
    draw_info.window.blit(controls, ((draw_info.width / 2) - (controls.get_width()/2), 45))

    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | S - Selection Sort | M - Merge Sort | Q - Quick Sort", 1, draw_info.TEXT_COLOR)
    draw_info.window.blit(sorting, ((draw_info.width / 2) - (sorting.get_width()/2), 75))

    draw_list(draw_info)
    pygame.display.update()

# BUBBLE SORT IMPLEMENTATION
def bubble_sort(draw_info, ascending = True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            # Storing j and j+1 values respt of a for loop in num1 and num2 variables.
            num1 = lst[j]
            num2 = lst[j + 1]

            # Condition if we sorting in ascending order and
            # the value at index j is greater than j+1 then swap the values.
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j+1: draw_info.COLUMBIA_BLUE}, True)
                yield True
    
    return lst

# INSERTION SORT IMPLEMENTATION
def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i-1] > current and ascending
            descending_sort = i > 0 and lst[i-1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i-1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i-1: draw_info.GREEN, i:draw_info.COLUMBIA_BLUE}, True)
            yield True

    return lst

# SELECTION SORT IMPLEMENTATION
def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst

    # Condition if we are sorting in Ascending order
    if ascending == True:
        for i in range(len(lst)):
            min_idx = i
            for j in range(i+1, len(lst)):

                # Finding the minimum value in the remaining array
                if lst[min_idx] > lst[j]:
                    min_idx = j

            # After finding the minimum value element swap the element with the first element
            lst[i], lst[min_idx] = lst[min_idx], lst[i]
            draw_list(draw_info, {i: draw_info.GREEN, min_idx:draw_info.COLUMBIA_BLUE}, True)
            yield True

    # Condition if we are sorting in Descending order
    else:
        for i in range(len(lst)):
            max_idx = i
            for j in range(i+1, len(lst)):

                # Finding the minimum value in the remaining array
                if lst[max_idx] < lst[j]:
                    max_idx = j

            # After finding the maximum value element swap the element with the first element
            lst[i], lst[max_idx] = lst[max_idx], lst[i]
            draw_list(draw_info, {i: draw_info.GREEN, max_idx:draw_info.COLUMBIA_BLUE}, True)
            yield True

    return lst

def merge_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def merge(left, right, start, end):
        i = j = 0
        merged = []

        while i < len(left) and j < len(right):
            if (left[i] < right[j] and ascending) or (left[i] > right[j] and not ascending):
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        while i < len(left):
            merged.append(left[i])
            i += 1

        while j < len(right):
            merged.append(right[j])
            j += 1

        lst[start:end] = merged
        draw_list(draw_info, {k: draw_info.COLUMBIA_BLUE for k in range(start, end)}, True)
        yield True

    def merge_sort_recursive(start, end):
        if end - start > 1:
            mid = (start + end) // 2
            yield from merge_sort_recursive(start, mid)
            yield from merge_sort_recursive(mid, end)
            yield from merge(lst[start:mid], lst[mid:end], start, end)

    yield from merge_sort_recursive(0, len(lst))

    return lst

def quick_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def partition(low, high):
        pivot = lst[high]
        i = low - 1

        for j in range(low, high):
            if (lst[j] < pivot and ascending) or (lst[j] > pivot and not ascending):
                i += 1
                lst[i], lst[j] = lst[j], lst[i]
                draw_list(draw_info, {i: draw_info.COLUMBIA_BLUE, j: draw_info.COLUMBIA_BLUE}, True)
                yield True

        lst[i + 1], lst[high] = lst[high], lst[i + 1]
        draw_list(draw_info, {i + 1: draw_info.GREEN, high: draw_info.GREEN}, True)
        yield True

        return i + 1

    def quick_sort_recursive(low, high):
        if low < high:
            pi = yield from partition(low, high)

            yield from quick_sort_recursive(low, pi - 1)
            yield from quick_sort_recursive(pi + 1, high)

    yield from quick_sort_recursive(0, len(lst) - 1)

    return lst

def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        # Generating a rect that is only displaying the bars section and not the Top Text and Side Pads
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    # enumerate gives the index as well as the value of the particular element in the lst.
    for i, val in enumerate (lst):
        # Determing the X and Y coordinates of the bars given index i and value val
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        # Assigning the color of the individual bar in a alternate pattern. Light, Medium, Dark Gray colors alternately.
        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))
    
    if clear_bg:
        # Updating the display after clearing the background
        pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()

    n = 50 # Number of Random Numbers to be generated in the list
    min_val = 0
    max_val = 100
    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)

    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algorithm_name = "BUBBLE SORT"
    sorting_algorithm_generator = None

    while run:
        # clock is a variable that takes how fast we want to run this algorithm. For now we take it as 60 FPS.
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False

        else:
            draw(draw_info, sorting_algorithm_name, ascending)

        # Running and Quiting events in pygame. Create a loop for this.
        # It's going to handle the COLUMBIA_BLUE X on the screen. If this loop is not mentioned then pressing the COLUMBIA_BLUE X will not do anything.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            # pygame.K_(any_key) shows that if we press the mentioned key here 'r' then the event.type is going to be True.
            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)

                # If we press 'r' then it will reset the entire list with a new random list and
                # then we also need to pass the new random list to the draw_info class in order to function the rest of the code.
                draw_info.set_list(lst)
                sorting = False

            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)

            elif event.key == pygame.K_a and not sorting:
                ascending = True

            elif event.key == pygame.K_d and not sorting:
                ascending = False

            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algorithm_name = "BUBBLE SORT"

            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algorithm_name = "INSERTION SORT"

            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm = selection_sort
                sorting_algorithm_name = "SELECTION SORT"

            elif event.key == pygame.K_m and not sorting:
                sorting_algorithm = merge_sort
                sorting_algorithm_name = "MERGE SORT"

            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm = quick_sort
                sorting_algorithm_name = "QUICK SORT"

    pygame.quit()

if __name__ == "__main__":
    main()