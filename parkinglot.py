import sys
import json
import time 

class ParkingLot:

    def __init__(self):
        self.spaces = 0
        self.hourly_cost = 10
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
        # Find the first empty slot
        if self.state["spaces"] == 0:
            print("Parking is curerntly full.")
            return #There is no need to loop through the file if ther are no spaces left 
        for slot_id, slot_data in self.state["slots"].items():
            if slot_data is None:
                current_time = int(time.time())
                self.state["slots"][slot_id] = {
                    "car_number": car_number,
                    # "parking_time": current_time
                }
                self.state["spaces"] = self.state["spaces"]-1
                
                self.save_state()
                print("Allocated slot number:", slot_id)
                return


    def leave_parking_lot(self, car_number, hours):
        self.load_state()
        # print(car_number)
        car_parking_map={}
        # print(self.state["slots"].items())
        car_parking_map = {value["car_number"]: key for key, value in self.state["slots"].items() if value is not None}
        if car_number in car_parking_map:
            # parked_since=self.state["slots"][car_parking_map[car_number]]["parking_time"] #its a choice between spending one more local variable vs hurting the next person to read this
            # current_time = int(time.time())
            # parked_hours = (current_time-parked_since)/3600 
            # parked_hours_round_up = int(parked_hours)+int(parked_hours % 1 != 0) #or use a math lib 
            cost = max(10, 10 + (hours - 2) * 10) #Cars can't literaly leave within a second after parking.
            print("Registration Number", car_number,"from Slot",car_parking_map[car_number], "has left with Charge", cost)
            self.state["slots"][car_parking_map[car_number]] = None # Marking the slot empty
            self.state["spaces"] = self.state["spaces"]+1
            self.save_state()
        else:
            print("Registration Number",car_number,"not found")


    def display_parking_lot_status(self):
        self.load_state()
        # print("Parking lot status:"
        #     "\nTotal spaces:", len(self.state["slots"]),
        #     "\nAvailable spaces:", self.state["spaces"],
        print("\nSlot No. Registration No.")

        #Making the null finding faster
        non_null_dict = {key: value["car_number"] for key, value in self.state["slots"].items() if value is not None}
        for key, value in non_null_dict.items():
            print(key, "          ", value) #behold the beauty of spaces


        
def usage(accepted_arguments):
    print("Usage: python3 script_name.py [command]")
    print("Accepted commands:", ", ".join(accepted_arguments))
 
def main(file):
    # Define the list of accepted arguments
    accepted_arguments = ["create", "park", "leave", "status"]

    # Initialize the parking lot object
    parking_lot = ParkingLot()

    # Open the file for reading
    with open(file, 'r') as f:
        # Read each line of the file
        for line in f:
            # Split the line into a list of arguments
            args = line.strip().split()

            # Check if the user input matches the accepted arguments
            if len(args) > 0 and args[0] in accepted_arguments:
                if args[0] == "create" and len(args) == 2:
                    parking_lot.create_parking_lot(args[1])

                elif args[0] == "park" and len(args) == 2:
                    parking_lot.park_car(args[1])

                elif args[0] == "leave" and len(args) == 3:
                    parking_lot.leave_parking_lot(args[1], int(args[2]))

                elif args[0] == "status":
                    parking_lot.display_parking_lot_status()

                else:
                    usage(accepted_arguments)
            else:
                usage(accepted_arguments)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Usage: python parking_lot.py <file>")