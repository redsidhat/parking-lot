import sys
import json
import time 

class ParkingLot:

    def __init__(self):
        self.spaces = 0
        self.cars = {}
        self.state_file = "parking_lot_state.json"
        self.state = {} 

    def load_state(self):
        try:
            with open(self.state_file) as f:
                self.state = json.load(f)
        except FileNotFoundError:
            print("No statefile found. Create a parking lot first")

    def save_state(self):
        with open(self.state_file, "w") as f:
            json.dump(self.state, f)
            
    def create_parking_lot(self, size):
        self.state["spaces"] = int(size)
        print("Creating a parking lot with", size, "spaces.")
        self.state["slots"] = {str(i): None for i in range(1, int(size) + 1)}
        
        self.save_state()
        print("Created a parking lot with", size, "slots.")

    def park_car(self, car_number):
        self.load_state()
        # print(self.state)
        # Find the first empty slot
        if self.state["spaces"] == 0:
            print("Parking is curerntly full.")
            return #There is no need to loop through the file if ther are no spaces left 
        for slot_id, slot_data in self.state["slots"].items():
            # print(slot_data)
            if slot_data is None or slot_data["parking_status"] == 0:
                current_time = int(time.time())
                self.state["slots"][slot_id] = {
                    "car_number": car_number,
                    "parking_time": current_time,
                    "leaving_time": None,
                    "total_cost": None,
                    "parking_status": 1
                }
                self.state["spaces"] = self.state["spaces"]-1
                
                self.save_state()
                print("Allocated slot number:", slot_id)
                return


    def leave_parking_lot(self, car_number, hours):
        if car_number not in self.cars:
            print("Car with number", car_number, "not found.")
        else:
            cost = int(hours) * 10 # $10 per hour
            del self.cars[car_number]
            print("Car with number", car_number, "has left the parking lot after", hours, "hours. The cost is $", cost, ".")

    def display_parking_lot_status(self):
        self.load_state()
        print("Parking lot status:"
            "Total spaces:", self.spaces,
            "Available spaces:", self.spaces - len(self.cars))
        print("Occupied spaces:", len(self.cars))
        print("Cars parked:", ", ".join(self.cars.keys()))

def usage(accepted_arguments):
    print("Usage: python3 script_name.py [command]")
    print("Accepted commands:", ", ".join(accepted_arguments))

def main():
    # Define the list of accepted arguments
    accepted_arguments = ["create", "park", "leave", "status"]

    # Initialize the parking lot object
    parking_lot = ParkingLot()

    # Check if the user input matches the accepted arguments
    if len(sys.argv) > 1 and sys.argv[1] in accepted_arguments:
        if sys.argv[1] == "create" and len(sys.argv) == 3:
            parking_lot.create_parking_lot(sys.argv[2])
        elif sys.argv[1] == "park" and len(sys.argv) == 3:
            parking_lot.park_car(sys.argv[2])
        elif sys.argv[1] == "leave" and len(sys.argv) == 4:
            parking_lot.leave_parking_lot(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == "status":
            parking_lot.display_parking_lot_status()
        else:
            usage(accepted_arguments)
    else:
        usage(accepted_arguments)

if __name__ == "__main__":
    main()
