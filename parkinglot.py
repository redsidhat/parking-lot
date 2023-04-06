import sys
import json

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
            self.state = {"slots": {}}

    def save_state(self):
        with open(self.state_file, "w") as f:
            json.dump(self.state, f)
            
    def create_parking_lot(self, size):
        self.spaces = int(size)
        print("Creating a parking lot with", size, "spaces.")
        self.state["slots"] = {str(i): None for i in range(1, int(size) + 1)}
        self.save_state()
        print("Created a parking lot with", size, "slots.")

    def park_car(self, car_number):
        if len(self.cars) >= self.spaces:
            print("No available parking spaces.")
        else:
            self.cars[car_number] = None
            print("Parking car with number", car_number, ".")

    def leave_parking_lot(self, car_number, hours):
        if car_number not in self.cars:
            print("Car with number", car_number, "not found.")
        else:
            cost = int(hours) * 10 # $10 per hour
            del self.cars[car_number]
            print("Car with number", car_number, "has left the parking lot after", hours, "hours. The cost is $", cost, ".")

    def display_parking_lot_status(self):
        print("Parking lot status:")
        print("Total spaces:", self.spaces)
        print("Available spaces:", self.spaces - len(self.cars))
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
