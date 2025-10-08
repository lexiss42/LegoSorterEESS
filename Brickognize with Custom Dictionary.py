import cv2
import requests
import json
import time

#public variables
brick_counter = 0

categories = {
    "Standard Bricks and Plates": 1,
    "Tiles and Slopes": 2,
    "Minifigures, Animals, and Figures": 3,
    "Technic and Mechanical Parts": 4,
    "Vehicles and Transportation": 5,
    "Windows, Doors, and Architectural Elements": 6,
    "Specialized and Miscellaneous Parts": 7,
    "BIONICLE and Hero Factory": 8,
    "Miscellaneous and Promotional Items": 9,
    "Unrecognized (DUPLO)": 10
}

category_mapping = {
    # Standard Bricks and Plates
    "Brick": 1, "Brick, Braille": 1, "Brick, Decorated": 1, "Brick, Modified": 1, "Brick, Modified, Decorated": 1,
    "Brick, Promotional": 1, "Brick, Round": 1, "Brick, Round, Decorated": 1, "Plate": 1, "Plate, Decorated": 1,
    "Plate, Modified": 1, "Plate, Modified, Decorated": 1, "Plate, Round": 1, "Plate, Round, Decorated": 1,

    # Tiles and Slopes
    "Tile": 2, "Tile, Decorated": 2, "Tile, Modified": 2, "Tile, Modified, Decorated": 2, "Tile, Promotional": 2,
    "Tile, Round": 2, "Tile, Round, Decorated": 2, "Slope": 2, "Slope, Curved": 2, "Slope, Curved, Decorated": 2,
    "Slope, Decorated": 2, "Slope, Inverted": 2, "Slope, Inverted, Decorated": 2,

    # Minifigures, Animals, and Figures
    "Minifigure, Body Part": 3, "Minifigure, Body Wear": 3, "Minifigure, Hair": 3, "Minifigure, Head": 3,
    "Minifigure, Head, Modified": 3, "Minifigure, Headgear": 3, "Minifigure, Headgear Accessory": 3,
    "Minifigure, Legs": 3, "Minifigure, Legs, Decorated": 3, "Minifigure, Legs, Modified": 3,
    "Minifigure, Legs, Modified, Decorated": 3, "Minifigure, Shield": 3, "Minifigure, Torso": 3,
    "Minifigure, Torso Assembly": 3, "Minifigure, Torso Assembly, Decor.": 3, "Minifigure, Utensil": 3,
    "Minifigure, Utensil, Decorated": 3, "Minifigure, Weapon": 3, "Animal, Accessory": 3, "Animal, Air": 3,
    "Animal, Body Part": 3, "Animal, Body Part, Decorated": 3, "Animal, Dinosaur": 3, "Animal, Land": 3,
    "Animal, Water": 3, "Micro Doll, Body Part": 3, "Mini Doll, Body Part": 3, "Mini Doll, Body Wear": 3,
    "Mini Doll, Hair": 3, "Mini Doll, Head": 3, "Mini Doll, Head, Modified": 3, "Mini Doll, Headgear": 3,
    "Mini Doll, Legs": 3, "Mini Doll, Torso": 3, "Mini Doll, Utensil": 3,

    # Technic and Mechanical Parts
    "Technic": 4, "Technic, Axle": 4, "Technic, Brick": 4, "Technic, Connector": 4, "Technic, Disk": 4,
    "Technic, Figure Accessory": 4, "Technic, Flex Cable": 4, "Technic, Gear": 4, "Technic, Liftarm": 4,
    "Technic, Liftarm, Decorated": 4, "Technic, Link": 4, "Technic, Panel": 4, "Technic, Panel, Decorated": 4,
    "Technic, Pin": 4, "Technic, Plate": 4, "Technic, Shock Absorber": 4, "Technic, Steering": 4,

    # Vehicles and Transportation
    "Vehicle": 5, "Vehicle, Base": 5, "Vehicle, Mudguard": 5, "Vehicle, Mudguard, Decorated": 5, "Wheel": 5,
    "Wheel & Tire Assembly": 5, "Wheel, Accessory": 5, "Wheel, Tire & Tread": 5, "Train": 5, "Train, Track": 5,
    "Aircraft": 5, "Aircraft, Decorated": 5, "Boat": 5,

    # Windows, Doors, and Architectural Elements
    "Window": 6, "Window, Decorated": 6, "Window, Glass & Shutter": 6, "Window, Glass & Shutter, Decorated": 6,
    "Door": 6, "Door, Decorated": 6, "Door, Frame": 6, "Arch": 6, "Arch, Decorated": 6, "Panel": 6,
    "Panel, Decorated": 6,

    # Specialized and Miscellaneous Parts
    "Antenna": 7, "Arm": 7, "Ball": 7, "Bar": 7, "Baseplate": 7, "Baseplate, Raised": 7, "Baseplate, Road": 7,
    "Bracket": 7, "Chain": 7, "Classic": 7, "Clikits": 7, "Clikits, Icon": 7, "Clikits, Icon Accent": 7, "Cloth": 7,
    "Cockpit": 7, "Cone": 7, "Cone, Decorated": 7, "Container": 7, "Container, Decorated": 7, "Conveyor": 7,
    "Crane": 7, "Cylinder": 7, "Cylinder, Decorated": 7, "Dish": 7, "Dish, Decorated": 7, "Electric": 7,
    "Electric, Battery Box": 7, "Electric, Light & Sound": 7, "Electric, Motor": 7, "Electric, Programmable": 7,
    "Electric, Train": 7, "Electric, Wire & Connector": 7, "Electronics": 7, "Energy Effect": 7, "Explore": 7,
    "Fabuland": 7, "Felt": 7, "Fence": 7, "Flag": 7, "Flag, Decorated": 7, "Foam": 7, "Food & Drink": 7, "Friends": 7,
    "Galidor": 7, "Garage": 7, "Hero Factory": 7, "Hinge": 7, "Hinge, Decorated": 7, "HO 1:87 Vehicles": 7,
    "Homemaker": 7, "Hook": 7, "Hose": 7, "Hose, Pneumatic 4mm D.": 7, "Hose, Ribbed 7mm D.": 7, "Hose, Rigid 3mm D.": 7,
    "Hose, Soft 3mm D.": 7, "Hose, Soft Axle": 7, "Human Jewelry": 7, "Human Tool": 7, "Jumbo Bricks": 7, "Ladder": 7,
    "Large Figure Part": 7, "Magnet": 7, "Minitalia": 7, "Modulex": 7, "Modulex, Brick": 7, "Modulex, Tile, Decorated": 7,
    "Modulex, Window": 7, "Monorail": 7, "Motor, Non-Electric": 7, "Paper": 7, "Plant": 7, "Plant, Tree": 7, "Plastic": 7,
    "Pneumatic": 7, "Primo": 7, "Projectile Launcher": 7, "Propeller": 7, "Quatro": 7, "Riding Cycle": 7, "Ring": 7,
    "Road Sign": 7, "Road Sign, Decorated": 7, "Rock": 7, "Roof": 7, "Rubber Band & Belt": 7, "Scala": 7,
    "Scala, Figure Accessory": 7, "Slide": 7, "Soft Bricks": 7, "Special Assembly": 7, "Sports": 7, "Spring": 7,
    "Stairs": 7, "Sticker Sheet": 7, "Stickered Assembly": 7, "String & Net": 7, "String Reel / Winch": 7, "Support": 7,
    "Tail": 7, "Tail, Decorated": 7, "Tap": 7, "Throwing Disk": 7, "Town Plan": 7, "Track System": 7, "Turntable": 7,
    "Windscreen": 7, "Windscreen, Decorated": 7, "Wing": 7, "Znap": 7,

    # BIONICLE and Hero Factory
    "BIONICLE": 8, "BIONICLE, Kanohi Mask": 8, "Hero Factory": 8,

    # Miscellaneous and Promotional Items
    "(Other)": 9, "Aircraft, Decorated": 9, "Animal, Accessory": 9, "Animal, Air": 9, "Animal, Body Part": 9,
    "Animal, Body Part, Decorated": 9, "Animal, Dinosaur": 9, "Animal, Land": 9, "Animal, Water": 9, "Antenna": 9,
    "Arch": 9, "Arch, Decorated": 9, "Arm": 9, "Ball": 9, "Bar": 9, "Baseplate": 9, "Baseplate, Raised": 9,
    "Baseplate, Road": 9, "Belville": 9, "Belville, Figure Accessory": 9, "BIONICLE": 9, "BIONICLE, Kanohi Mask": 9,
    "Boat": 9, "Bracket": 9, "Brick": 9, "Brick, Braille": 9, "Brick, Decorated": 9, "Brick, Modified": 9,
    "Brick, Modified, Decorated": 9, "Brick, Promotional": 9, "Brick, Round": 9, "Brick, Round, Decorated": 9,
    "Cardboard Sleeve": 9, "Chain": 9, "Classic": 9, "Clikits": 9, "Clikits, Icon": 9, "Clikits, Icon Accent": 9,
    "Cloth": 9, "Cockpit": 9, "Cone": 9, "Cone, Decorated": 9, "Container": 9, "Container, Decorated": 9, "Conveyor": 9,
    "Crane": 9, "Cylinder": 9, "Cylinder, Decorated": 9, "Dish": 9, "Dish, Decorated": 9, "Door": 9, "Door, Decorated": 9,
    "Door, Frame": 9, "Electric": 9, "Electric, Battery Box": 9, "Electric, Light & Sound": 9, "Electric, Motor": 9,
    "Electric, Programmable": 9, "Electric, Train": 9, "Electric, Wire & Connector": 9, "Electronics": 9,
    "Energy Effect": 9, "Explore": 9, "Fabuland": 9, "Felt": 9, "Fence": 9, "Flag": 9, "Flag, Decorated": 9, "Foam": 9,
    "Food & Drink": 9, "Friends": 9, "Galidor": 9, "Garage": 9, "Hero Factory": 9, "Hinge": 9, "Hinge, Decorated": 9,
    "HO 1:87 Vehicles": 9, "Homemaker": 9, "Hook": 9, "Hose": 9, "Hose, Pneumatic 4mm D.": 9, "Hose, Ribbed 7mm D.": 9,
    "Hose, Rigid 3mm D.": 9, "Hose, Soft 3mm D.": 9, "Hose, Soft Axle": 9, "Human Jewelry": 9, "Human Tool": 9,
    "Jumbo Bricks": 9, "Ladder": 9, "Large Figure Part": 9, "Magnet": 9, "Minitalia": 9, "Modulex": 9, "Modulex, Brick": 9,
    "Modulex, Tile, Decorated": 9, "Modulex, Window": 9, "Monorail": 9, "Motor, Non-Electric": 9, "Paper": 9, "Plant": 9,
    "Plant, Tree": 9, "Plastic": 9, "Pneumatic": 9, "Primo": 9, "Projectile Launcher": 9, "Propeller": 9, "Quatro": 9,
    "Riding Cycle": 9, "Ring": 9, "Road Sign": 9, "Road Sign, Decorated": 9, "Rock": 9, "Roof": 9, "Rubber Band & Belt": 9,
    "Scala": 9, "Scala, Figure Accessory": 9, "Slide": 9, "Soft Bricks": 9, "Special Assembly": 9, "Sports": 9, "Spring": 9,
    "Stairs": 9, "Sticker Sheet": 9, "Stickered Assembly": 9, "String & Net": 9, "String Reel / Winch": 9, "Support": 9,
    "Tail": 9, "Tail, Decorated": 9, "Tap": 9, "Throwing Disk": 9, "Town Plan": 9, "Track System": 9, "Turntable": 9,
    "Windscreen": 9,
}

def get_category_number(category_name):
    category_number = category_mapping.get(category_name)
    print(f"Category name: {category_name}, Category number: {category_number}")  # Debugging line
    return category_number


def capture_image(cap, filename='lego_piece.jpg'):
    ret, frame = cap.read()
    cap.release()

    if brick_counter == 0:
        cv2.imwrite(filename, frame)
        cv2.imshow('Captured Image', frame)
        cv2.waitKey(0)  # Wait for a key press to close the window
        cv2.destroyAllWindows()

    return filename


def recognize_lego_piece(image_path):
    url = 'https://api.brickognize.com/predict'  # Updated API endpoint
    files = {'query_image': (image_path, open(image_path, 'rb'), 'image/jpeg')}
    headers = {'accept': 'application/json'}
    response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        result = response.json()
        print('Full response:', result)
        if 'items' in result and len(result['items']) > 0:
            category_name = result['items'][0]['category']
            category_number = get_category_number(category_name)
            return category_number
        else:
            return 9  # Default to Miscellaneous and Promotional Items if no items found
    else:
        print('Error:', response.status_code, response.text)
        return 10


def sort_piece(category_number):
    # Implement your sorting logic here
    # For example, control motors or actuators to direct the piece to the correct bin
    print(f"Sorting piece into category number: {category_number}")


def main():
    cap = cv2.VideoCapture(0)  # Open defualt video capture device. 0 is the default camera]

    # If camera cannot be opened, run this code.
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Run image recognition in a loop for now
    while True:
        image_path = capture_image(cap) # Run capture image method

        if image_path:
            category_number = recognize_lego_piece(image_path)
            sort_piece(category_number)

            global brick_counter  # Increment the brick counter
            brick_counter += 1
            print(f"Total bricks logged: {brick_counter}", flush=True)
        time.sleep(1)  # Add a delay to avoid overwhelming the API


if __name__ == '__main__':
    main()
