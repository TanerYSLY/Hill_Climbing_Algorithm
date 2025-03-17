import random 
import os

#the locations are specified using rows and columns that is why there are the parameters of this method

class Space: #this is our problem space we are trying to optimize the distance on this space
    def __init__(self,height,width,num_hospitals): #initialize the space with height, width and number of hospitals
        self.height = height
        self.width = width
        self.num_hospitals = num_hospitals
        self.houses = set() #houses are stored in a set because we don't want duplicates
        self.hospitals = set() #hospitals are stored in a set   
        
    def add_house(self,row,col): #add a house to the space, houses are stored as a tuple of row and column
        #row and columns are the coordinates of the house
        self.houses.add((row,col)) #add the house to the set of houses

    #if a house or hospital is already there we cannot place a hospital or house there
    # so we need to find the available space

    def available_space(self):
        candidates = set((row,col) for row in range(self.height) for col in range(self.width)) #all the possible coordinates
        for house in self.houses: #remove the houses from the candidates
            candidates.remove(house) #if a house is already there we cannot place a house there
        for hospital in self.hospitals: #remove the hospitals from the candidates
            candidates.remove(hospital) #if a hospital is already there we cannot place a hospital there
        return candidates #return the available space

    #now we need to calculate the cost of the current configuration
    #we need to calculate the distance of each house from the nearest hospital
    #and sum all the distances

    def get_cost(self,hospitals):
        cost = 0
        for house in self.houses:
            cost += min(abs(house[0] - hospital[0]) + abs(house[1] - hospital[1]) for hospital in hospitals)
            #abs : absolute value 
            # sum row and column distance of each house from the nearest hospital and add it to the cost
        return cost
    
    def get_neighbors(self,row,col): #get the neighbors of a cell

        candidates = [
            (row-1,col), # columns remains and row decreases and that is a neighbor of the cell
            (row+1,col),
            (row,col-1),
            (row,col+1)
        ]

        neighbors = [] #initialize the neighbors list

        for r,c in candidates:
            if (r,c) in self.houses or (r,c) in self.hospitals:
                continue
            if 0 <= r < self.height and 0 <= c < self.width:
                neighbors.append((r,c)) #if the neighbor is not a house or hospital and it is in the space add it to the neighbors
        return neighbors #return the neighbors

    def output_image(self, filename):  # output the image of the space
        from PIL import Image, ImageDraw, ImageFont  # import the necessary libraries
        cell_size = 100  # size of the cell
        cell_border = 2  # border of the cell
        cost_size = 40  # size of the cost
        padding = 10  # padding of the image
    
        img = Image.new("RGBA",  # create a new image
                        (self.width * cell_size, self.height * cell_size + cost_size + padding * 2),  # size of the image
                        "white"  # background color
                        )
    
        base_path = os.path.dirname(__file__)
        house_path = os.path.join(base_path, "assets/images/House.png")
        hospital_path = os.path.join(base_path, "assets/images/Hospital.png")
        font_path = os.path.join(base_path, "assets/fonts/arial.ttf")
    
        house = Image.open(house_path)\
            .resize((cell_size, cell_size))  # open the image of the house and resize it to the cell size
        hospital = Image.open(hospital_path) \
            .resize((cell_size, cell_size))  # open the image of the hospital and resize it to the cell size
        fonts = ImageFont.truetype(font_path, 30)  # font of the text
        draw = ImageDraw.Draw(img)
    
        for i in range(self.height):
            for j in range(self.width):
                rect = [
                    (j * cell_size + cell_border, i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)
                ]
                draw.rectangle(rect, fill="black")
    
                if (i, j) in self.houses:
                    img.paste(house, (j * cell_size, i * cell_size), house)
                if (i, j) in self.hospitals:
                    img.paste(hospital, (j * cell_size, i * cell_size), hospital)
    
        # Define colors for different paths
        colors = ["yellow", "blue", "green", "orange", "purple", "pink", "cyan", "magenta"]
    
        # Draw paths from houses to the nearest hospitals
        for index, house in enumerate(self.houses):
            color = colors[index % len(colors)]
            house_center = (house[1] * cell_size + cell_size // 2, house[0] * cell_size + cell_size // 2)
            nearest_hospital = min(self.hospitals, key=lambda h: abs(house[0] - h[0]) + abs(house[1] - h[1]))
            hospital_center = (nearest_hospital[1] * cell_size + cell_size // 2, nearest_hospital[0] * cell_size + cell_size // 2)
    
            # Draw horizontal line
            intermediate_point = (hospital_center[0], house_center[1])
            draw.line([house_center, intermediate_point], fill=color, width=5)
            # Draw vertical line
            draw.line([intermediate_point, hospital_center], fill=color, width=5)
    
            # Draw arrows and distances
            current_position = house_center
            distance = 0
    
            # Horizontal segment
            while current_position[0] != intermediate_point[0]:
                distance += 1
                next_position = (current_position[0] + (1 if intermediate_point[0] > current_position[0] else -1) * cell_size, current_position[1])
                draw.line([current_position, next_position], fill=color, width=5)
                current_position = next_position
    
            # Vertical segment
            while current_position[1] != hospital_center[1]:
                distance += 1
                next_position = (current_position[0], current_position[1] + (1 if hospital_center[1] > current_position[1] else -1) * cell_size)
                draw.line([current_position, next_position], fill=color, width=5)
                current_position = next_position
    
            # Draw distance on top of the house
            draw.text((house_center[0] - cell_size // 4, house_center[1] - cell_size // 2), str(distance), fill=color, font=fonts)
    
        draw.rectangle(
            (0, self.height * cell_size, self.width * cell_size,
             self.height * cell_size + cost_size + padding * 2),
            "black"
        )
    
        draw.text(
            (padding, self.height * cell_size + padding),
            f"Cost: {self.get_cost(self.hospitals)}",
            font=fonts,
            fill="white"
        )
    
        img.save(filename)
    
    def hill_climb(self,Maximum = None,image_prefix = None,log = False):
        #Maximum is the maximum number of iterations
        #there will be multiple images to trac them we will use same image prefix
        #log refers to the optimization progress
        #if log is true we will print the progress
        count = 0
        self.hospitals = set()

        for i in range(self.num_hospitals):
            self.hospitals.add(random.choice(list(self.available_space()))) #randomly choose the hospitals from the available space
            #convert the available space to a list and choose a random element from the list
            """
            If you try to call available_space() without self, Python controls whether there can be a 
            global or local function with that name.
	        However, since available_space is only defined in the class, you can't access it without using self.
            """
        if log: #if log is true
            print("Initial state: Cost", self.get_cost(self.hospitals)),
        if image_prefix:
            self.output_image(f"{image_prefix}{str(count).zfill(3)}.png") #output the image of the space
            #zfill adds zeros to the left of the string to make it 3 characters long    
            # this method requires the filename as a parameter. There will be multiple images so we need to name them dynamically
            # if we keep the same name then new images will overwrite the old ones and and of the optimization 
            # we will only have the last image

        while Maximum is None or count < Maximum: #if the maximum is not specified or the count is less than the maximum
            count += 1
            best_neighbors = []
            best_neighbor_cost = None  

            for hospital in self.hospitals: #we will get the location of the hospitals
                for replacement in self.get_neighbors(*hospital): #we're looking for possible replacements in this loop
                    #possible replacements are the neighbors of the hospital
                    neighbor = self.hospitals.copy()
                    #we will copy the current hospitals to the neighbor
                    neighbor.remove(hospital)
                    #remove the current hospital that is now in the loop
                    neighbor.add(replacement)
                    # add the neighbor location to the neighbor instead 
                    # of the current hospital
                
                    cost = self.get_cost(neighbor)
                    if best_neighbor_cost is None or cost < best_neighbor_cost: # i want to cost to be minimum
                        best_neighbor_cost = cost
                        best_neighbors = [neighbor] #it is a list because there can be multiple neighbors with the same cost
                    elif best_neighbor_cost == cost:
                        best_neighbors.append(neighbor)    

            if best_neighbor_cost >= self.get_cost(self.hospitals):
                # the best neighbor solition is not better than the current solution
                # then the algorithm will return the current solution and stop
                return self.hospitals
            else:
                # if the best neighbor solution is better than the current solution
                # then the algorithm will update the current solution with the best neighbor solution
                if log:
                    print(f"Found Better Neighbor: cost {best_neighbor_cost}")
                self.hospitals = random.choice(best_neighbors)

            if image_prefix:
                self.output_image(f"{image_prefix}{str(count).zfill(3)}.png")        

s = Space(height=6, width=12, num_hospitals=2) #create a space with height 6, width 12 and 2 hospitals

for i in range(5): #add 5 houses to the space
    s.add_house(random.randrange(s.height), random.randrange(s.width))
                #random coordinate on the problem space
    """
    random.randrange(stop)
    random.randrange(start, stop[, step])

    Return a randomly selected element from range(start, stop, step).
    This is roughly equivalent to choice(range(start, stop, step)) but supports arbitrarily 
    large ranges and is optimized for common cases.
    """            

hospitals = s.hill_climb(image_prefix = "hospitals",log = True) #optimize the space and output the images


