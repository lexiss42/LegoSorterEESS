import cv2
import requests
import time
import json
import arduino

brick_counter = 0
current_position = 1

#default catagorisation setting
#name is input, checks part name then returns category
def get_category_number(name):
    category_7 = ['Antenna', 'Arm', 'Ball', 'Bar', 'Baseplate', 'Baseplate, Raised', 'Baseplate, Road', 'Bracket',
                  'Chain', 'Classic', 'Clikits', 'Clikits, Icon', 'Clikits, Icon Accent', 'Cloth', 'Cockpit', 'Cone',
                  'Cone, Decorated', 'Container', 'Container, Decorated', 'Conveyor', 'Crane', 'Cylinder',
                  'Cylinder, Decorated', 'Dish', 'Dish, Decorated', 'Electronics', 'Energy Effect', 'Explore',
                  'Fabuland', 'Felt', 'Fence', 'Flag', 'Flag, Decorated', 'Foam', 'Food & Drink', 'Friends', 'Galidor',
                  'Garage', 'Hero Factory', 'Hinge', 'Hinge, Decorated', 'HO 1:87 Vehicles', 'Homemaker', 'Hook',
                  'Human Jewelry', 'Human Tool', 'Jumbo Bricks', 'Ladder', 'Large Figure Part', 'Magnet', 'Minitalia',
                  'Monorail', 'Paper', 'Plant', 'Plant, Tree', 'Plastic', 'Pneumatic', 'Primo', 'Projectile Launcher',
                  'Propeller', 'Quatro', 'Riding Cycle', 'Ring', 'Road Sign', 'Road Sign, Decorated', 'Rock', 'Roof',
                  'Rubber Band & Belt', 'Scala', 'Scala, Figure Accessory', 'Slide', 'Soft Bricks', 'Special Assembly',
                  'Sports', 'Spring', 'Stairs', 'Sticker Sheet', 'Stickered Assembly', 'String & Net',
                  'String Reel / Winch', 'Support', 'Tail', 'Tail, Decorated', 'Tap', 'Throwing Disk', 'Town Plan',
                  'Track System', 'Turntable', 'Windscreen', 'Windscreen, Decorated', 'Wing', 'Znap']
    category_number = None
    if ('Brick' in name or 'Plate' in name) and name != 'Modulex, Brick' and \
            name != 'Technic, Plate' and name != 'Technic, Brick':
        category_number = 1
    elif ('Tile' in name or 'Slope' in name) and name != 'Modulex, Tile, Decorated':
        category_number = 2
    elif 'Minifigure' in name or 'Animal' in name or 'Doll' in name:
        category_number = 3
    elif 'Technic' in name:
        category_number = 4
    elif 'Vehicle' in name or 'Wheel' in name or 'Aircraft' in name or \
            name == 'Boat' or name == 'Train' or name == 'Train, Track':
        category_number = 5
    elif 'Window' in name or 'Door' in name or 'Arch' in name or 'Panel' in name:
        category_number = 6
    elif 'Electric' in name or 'Hose' in name or 'Modulex' in name or name in category_7:
        category_number = 7
    elif 'BIONICLE' in name:
        category_number = 8
    else:
        category_number = 9
    return category_number

#captures image but does not save the image files
def capture_image(cap):
    ret, frame = cap.read()
    cap.release()
    _, img = cv2.imencode('.jpg', frame)  # convert to image instead of saving to file

    debug = True
    if debug:
        cv2.imshow('Captured Image', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return img

#recognition function
def recognize_lego_piece(image):
    url = 'https://api.brickognize.com/predict'
    #files = {'query_image': ('', image.tobytes(), 'image/jpeg')}
    #open the images of the piece
    files = {'query_image': ('', open("./lego_piece_test.jpg", 'rb'), 'image/jpeg')}
    headers = {'accept': 'application/json'}
    response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        result = response.json()
        #print('Full response:', result)
        """
if item found:
{'listing_id': 'res-1f9b04ec618f45e8',
'bounding_box': {
    'left': 247.8058319091797, 
    'upper': 149.2323760986328, 
    'right': 475.60260009765625, 
    'lower': 381.690185546875,
    'image_width': 640.0,
    'image_height': 480.0,
    'score': 0.7187007665634155},

    'items': [
        {'id': '11213', 
        'name': 'Plate, Round 6 x 6 with Hole', 
        'img_url': 'https://storage.googleapis.com/brickognize-static/thumbnails-v2.17/part/11213/0.webp', 
        'external_sites': [
            {'name': 'bricklink', 
             'url': 'https://www.bricklink.com/v2/catalog/catalogitem.page?P=11213'}
        ],  
        'category': 'Plate, Round', 
        'type': 'part', 
        'score': 0.8847686}, 
        {'id': '22888', 
         'name': 'Plate, Round Half 4 x 8', 
         'img_url': 'https://storage.googleapis.com/brickognize-static/thumbnails-v2.17/part/22888/0.webp', 
         'external_sites': [
             {'name': 'bricklink', 
              'url': 'https://www.bricklink.com/v2/catalog/catalogitem.page?P=22888'
             }
         ], 
         'category': 'Plate, Round', 
         'type': 'part', 
         'score': 0.50046384
         }
    ]
}
        """
        """
if no item found:
{
'listing_id': 'res-1b2099d9316d4215', 
'bounding_box': {
    'left': 0.0, 
    'upper': 0.0, 
    'right': 0.0, 
    'lower': 0.0, 
    'image_width': 0.0, 
    'image_height': 0.0, 
    'score': 0.0
}, 
'items': []
}
        """
        if 'items' in result and len(result['items']) > 0:
            category_name = result['items'][0]['category']
            part_id = result['items'][0]['id']
            part_name = result['items'][0]['name']
            category_number = get_category_number(category_name)
            print("Part:", part_name)
            print('Part ID:', str(part_id))
            print('Category:', category_name)
            print('Category Number:', str(category_number))
            return category_number
        else:
            return None
    else:
        print('Error:', response.status_code, 'Text:', response.text, "JSON:", response.json)
        return None

#Sort piece - needs to send command to stepper motor
def sort_piece(category_number):
    global current_position
    #makes sure category is a valid category - later turn this into layer checking.
    if category_number > 12:
        print("Invalid Category")
        return;
    movement = category_number-current_position
    arduino.send_command(movement);


def main():
    global brick_counter
    global current_position
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    run = True
    while run:  # allows more control over breaking the loop than `while True:`
        image = capture_image(cap)
        if image is None:
            run = False
            break
        category_number = recognize_lego_piece(image)
        brick_counter += 1
        if category_number is not None:
            sort_piece(category_number) 
            current_position = category_number
        else:
            print("Could not sort")


if __name__ == '__main__':
    main()
