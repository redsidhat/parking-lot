import sys

def create_parking_lot(size):
    print("Creating a parking lot with", size, "spaces.")

def park_car(car_number):
    print("Parking car with number", car_number, ".")

def leave_parking_lot(car_number, hours):
    print("Car with number", car_number, "has left the parking lot after", hours, "hours.")

def display_parking_lot_status():
    print("Displaying parking lot status.")

def usage(accepted_arguments):
    print("Usage: python3 script_name.py [command]")
    print("Accepted commands:", ", ".join(accepted_arguments))

def main():
    # Define the list of accepted arguments
    accepted_arguments = ["create", "park", "leave", "status"]

    # Check if the user input matches the accepted arguments
    if len(sys.argv) > 1 and sys.argv[1] in accepted_arguments:
        if sys.argv[1] == "create" and len(sys.argv) == 3:
            create_parking_lot(sys.argv[2])
        elif sys.argv[1] == "park" and len(sys.argv) == 3:
            park_car(sys.argv[2])
        elif sys.argv[1] == "leave" and len(sys.argv) == 4:
            leave_parking_lot(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == "status":
            display_parking_lot_status()
        else:
            usage(accepted_arguments)
    else:
        usage(accepted_arguments)

if __name__ == "__main__":
    main()
