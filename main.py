import DiagnoseCar_BW as BW
import RepairCar_FW as FW
import logging
import time
import psutil
import json
import os

# Setup logging configuration for both file and console
logging.basicConfig(filename='auto_repair_log.log', 
                    level=logging.INFO, 
                    format='%(asctime)s %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S',
                    force=True)


# Test log entry for verification
logging.info("PROGRAM START")

# Initialize derived variables dictionaries
derived_backward_vars = {}
derived_forward_vars = {}

# File paths for derived variables
backward_var_file = 'Derived_Backward_Variable_List.json'
forward_var_file = 'Derived_Forward_Variable_List.json'

# Helper function to write derived variables to files
def write_to_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Helper function to load derived variables from files
def load_from_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}



CONCLUSION_LIST = {
    1 : "AUTOREPAIR PROBLEM",
    2 : "STARTING PROBLEM",
    3 : "STARTING PROBLEM",
    4 : "STARTING PROBLEM",
    5 : "STARTING PROBLEM",
    6 : "ENGINE PROBLEM",
    7 : "ENGINE ISSUE",
    8 : "ENGINE ISSUE",
    9 : "ENGINE ISSUE",
    10 : "ENGINE ISSUE",
    11 : "ENGINE ISSUE",
    12 : "TRANSMISSION PROBLEM",
    13 : "TRANSMISSION ISSUE",
    14 : "TRANSMISSION ISSUE",
    15 : "TRANSMISSION ISSUE",
    16 : "TRANSMISSION ISSUE",
    17 : "BRAKE SYSTEM PROBLEM",
    18 : "BRAKE ISSUE",
    19 : "BRAKE ISSUE",
    20 : "BRAKE ISSUE",
    21 : "BRAKE ISSUE",
    22 : "STEER PROBLEM",
    23 : "STEER PROBLEM",
    24 : "STEER PROBLEM",
    25 : "STEER PROBLEM",
    26 : "STEER PROBLEM",
    27 : "STEER PROBLEM",
    28 : "EXHAUST PROBLEM",
    29 : "EXHAUST PROBLEM",
    30 : "EXHAUST PROBLEM"
}

CLAUSE_VARIABLE_LIST = {
    1 : ["GOT PROBLEM"],
    9 : ["HAVING DIFFICULTY", "DASHBOARD LIGHTS DIM"],
    17 : ["HAVING DIFFICULTY", "DASHBOARD LIGHTS DIM","CLICKING SOUND", "POWER"],
    25 : ["HAVING DIFFICULTY", "DASHBOARD LIGHTS DIM","CLICKING SOUND", "POWER"],
    33 : ["HAVING DIFFICULTY", "DASHBOARD LIGHTS DIM", "CLICKING SOUND", "STEERING WHEEL STIFF","NOISE WHEN TURNING"],
    41 : ["HAVING DIFFICULTY", "POOR ACCELERATION", "NOISE FROM ENGINE", "ENGINE LIGHT ON"],
    49 : ["ENGINE PROBLEM", "ENGINE OVERHEATING", "COOLANT LEVEL LOW"],
    57 : ["ENGINE PROBLEM", "ENGINE OVERHEATING", "COOLANT LEVEL LOW", "RADIATOR FAN WORKING"],
    65 : ["ENGINE PROBLEM", "ENGINE OVERHEATING", "ENGINE SHAKING", "SPARK PLUGS FOULED"],
    73 : ["ENGINE PROBLEM", "ENGINE OVERHEATING", "ENGINE SHAKING", "FUEL PRESSURE LOW"],
    81 : ["ENGINE PROBLEM", "ENGINE OVERHEATING", "ENGINE SHAKING", "FUEL PRESSURE LOW", "AIR FILTER DIRTY"],
    89 : ["HAVING DIFFICULTY", "POOR ACCELERATION", "NOISE FROM ENGINE", "CAR JERK WHEN ACCELERATING"],
    97 : ["TRANSMISSION PROBLEM", "TRANSMISSION FLUID LOW"],
    105 : ["TRANSMISSION PROBLEM", "TRANSMISSION FLUID LOW", "CAR JERK WHEN SHIFTING GEARS"],
    113 : ["TRANSMISSION PROBLEM", "TRANSMISSION FLUID LOW", "CAR JERK WHEN SHIFTING GEARS", "TRANSMISSION NOISE WHEN ACCELERATING"],
    121 : ["TRANSMISSION PROBLEM", "TRANSMISSION FLUID LOW", "CAR JERK WHEN SHIFTING GEARS","TRANSMISSION NOISE WHEN ACCELERATING", "FLUID LEAKS UNDER THE CAR", "FLUID COLOR IS RED"],
    129 : ["CAR IS HAVING DIFFICULTY", "CANNOT SLOWDOWN WHEN BRAKING"],
    137 : ["BRAKE SYSTEM PROBLEM", "BRAKE PEDAL FEEL SPONGY", "BRAKE FLUID LEVEL LOW"],
    145 : ["BRAKE SYSTEM PROBLEM", "BRAKE PEDAL FEEL SPONGY", "BRAKE FLUID LEVEL LOW"],
    153 : ["BRAKE SYSTEM PROBLEM", "BRAKE PEDAL FEEL SPONGY","BRAKE PEDAL HARD TO PRESS"],
    161 : ["BRAKE SYSTEM PROBLEM", "BRAKE PEDAL HARD TO PRESS", "CAR TAKES LONGER TO STOP"],
    169 : ["HAVING DIFFICULTY", "POOR ACCELERATION", "CANNOT SLOWDOWN WHEN BRAKING", "STEERING FEEL LOOSE", "CAR PULLS TO ONE SIDE WHILE DRIVING"],
    177 : ["HAVING DIFFICULTY", "POOR ACCELERATION","CANNOT SLOWDOWN WHEN BRAKING",  "STEERING FEEL LOOSE", "CAR PULLS TO ONE SIDE WHILE DRIVING", "STEERING WHEEL VIBRATES", "VIBRATION WORSENS WHEN BRAKING"],
    185 : ["HAVING DIFFICULTY", "POOR ACCELERATION","CANNOT SLOWDOWN WHEN BRAKING",  "STEERING FEEL LOOSE", "CAR PULLS TO ONE SIDE WHILE DRIVING","STEERING WHEEL VIBRATES", "VIBRATION WORSENS WHEN BRAKING"],
    193 : ["HAVING DIFFICULTY", "POOR ACCELERATION","CANNOT SLOWDOWN WHEN BRAKING",  "STEERING FEEL LOOSE", "CAR PULLS TO ONE SIDE WHILE DRIVING","STEERING WHEEL VIBRATES", "STEERING DIFFICULT TO TURN", "WHINING NOISE"],
    201 : ["HAVING DIFFICULTY", "POOR ACCELERATION","CANNOT SLOWDOWN WHEN BRAKING",  "STEERING FEEL LOOSE", "CAR PULLS TO ONE SIDE WHILE DRIVING","STEERING WHEEL VIBRATES", "STEERING DIFFICULT TO TURN", "WHINING NOISE"],
    209 : ["HAVING DIFFICULTY", "POOR ACCELERATION","CANNOT SLOWDOWN WHEN BRAKING",  "STEERING FEEL LOOSE", "CAR PULLS TO ONE SIDE WHILE DRIVING","STEERING WHEEL VIBRATES", "STEERING DIFFICULT TO TURN", "CLICKING NOISE"],
    217 : ["HAVING DIFFICULTY", "POOR ACCELERATION","CANNOT SLOWDOWN WHEN BRAKING",  "STEERING FEEL LOOSE", "UNUSUAL NOISE FROM EXHAUST", "NOISE COMING FROM UNDER CAR"],
    225 : ["HAVING DIFFICULTY", "POOR ACCELERATION","CANNOT SLOWDOWN WHEN BRAKING",  "STEERING FEEL LOOSE", "UNUSUAL NOISE FROM EXHAUST", "NOISE COMING FROM UNDER CAR", "EXHAUST SMELL INSIDE CAR"],
    233 : ["HAVING DIFFICULTY", "POOR ACCELERATION","CANNOT SLOWDOWN WHEN BRAKING",  "STEERING FEEL LOOSE", "UNUSUAL NOISE FROM EXHAUST", "EXCESSIVE SMOKE FROM EXHAUST", "BLACK SMOKE"]

}

FORWARD_CLAUSE_VARIABLE_LIST = {
    1: ["AUTOREPAIR PROBLEM"],
    4: ["ELECTRICAL SYSTEM PROBLEM"],
    7: ["STARTER PROBLEM"],
    10: ["BATTERY PROBLEM"],
    13: ["POWER STEERING PUMP FAILURE"],
    16: ["ENGINE PROBLEM"],
    19: ["COOLANT LEAK"],
    22: ["RADIATOR FAN MALFUNCTION"],
    25: ["ENGINE MISFIRE"],
    28: ["LOW FUEL PRESSURE"],
    31: ["AIR INTAKE SYSTEM PROBLEM"],
    34: ["TRANSMISSION PROBLEM"],
    37: ["TRANSMISSION FLUID PROBLEM"],
    40: ["TRANSMISSION SLIPPAGE PROBLEM"],
    43: ["DAMAGED TRANSMISSION MOUNTS"],
    46: ["TRANSMISSION FLUID LEAK"],
    49: ["BRAKE SYSTEM PROBLEM"],
    52: ["LOW BRAKE FLUID"],
    55: ["AIR IN BRAKE LINES"],
    58: ["VACUUM SYSTEM ISSUE"],
    61: ["WORN BRAKE PADS"],
    64: ["STEERING/SUSPENSION PROBLEM"],
    67: ["WARPED BRAKE ROTORS"],
    70: ["UNBALANCED TIRES"],
    73: ["LOW POWER STEERING FLUID"],
    76: ["BINDING STEERING COMPONENTS"],
    79: ["WORN CV JOINTS"],
    82: ["LOOSE OR BROKEN HEAT SHIELD"],
    85: ["EXHAUST LEAK"],
    88: ["COOLANT LEAKING INTO ENGINE"],
    91: ["ENGINE RUNNING TOO RICH"],
    94: ["ENGINE BURNING OIL"]
}

if __name__ == '__main__':
    # Load existing derived variables from files
    derived_backward_vars = load_from_file(backward_var_file)
    derived_forward_vars = load_from_file(forward_var_file)
    backward_conclusion = None
    logging.info("Starting backward chaining process")

    # Track time and memory
    start_time_program = time.perf_counter()  # Program start time
    start_memory = psutil.Process().memory_info().rss / (1024 * 1024)  # Memory at start in MB
    
    user_input = input("Does your car have a problem? ")
    logging.info(f"User input received: {user_input}")

    if user_input.lower() == "yes":
        goal_variable = input("Which part of your car has a problem? [starting problem, engine issue, transition problem, brake problem, steer problem, exhaust problem] ")
        logging.info(f"Goal variable selected: {goal_variable}")
        
        # Start time for backward chaining
        start_time_bw = time.perf_counter()

        # Handle different goal variables for backward chaining
        if goal_variable == "starting problem":
            logging.info("Defining goal variable as 'STARTING PROBLEM'")
            backward_conclusion, symptoms = BW.process("STARTING PROBLEM")
        elif goal_variable == "engine issue":
            logging.info("Defining goal variable as 'ENGINE ISSUE'")
            backward_conclusion, symptoms = BW.process("ENGINE ISSUE")
        elif goal_variable == "transition problem":
            logging.info("Defining goal variable as 'TRANSMISSION ISSUE'")
            backward_conclusion, symptoms = BW.process("TRANSMISSION ISSUE")
        elif goal_variable == "brake problem":
            logging.info("Defining goal variable as 'BRAKE ISSUE'")
            backward_conclusion, symptoms = BW.process("BRAKE ISSUE")
        elif goal_variable == "steer problem":
            logging.info("Defining goal variable as 'STEER PROBLEM'")
            backward_conclusion, symptoms = BW.process("STEER PROBLEM")
        elif goal_variable == "exhaust problem":
            logging.info("Defining goal variable as 'EXHAUST PROBLEM'")
            backward_conclusion, symptoms = BW.process("EXHAUST PROBLEM")
        # End time for backward chaining
        end_time_bw = time.perf_counter()

        # Dynamically generate derived backward variable
        derived_backward_vars[goal_variable] = {
            "derived_variable": backward_conclusion,
            "dependencies": symptoms
        }

        # Write updated derived backward variables to file
        write_to_file(backward_var_file, derived_backward_vars)

        # Print time for backward chaining to console
        print(f"Time Elapsed for Backward Chaining: {end_time_bw - start_time_bw:0.2f} seconds")
        logging.info(f"Time Elapsed for Backward Chaining: {end_time_bw - start_time_bw:0.2f} seconds")

        logging.info(f"Backward chaining concluded with result: {backward_conclusion}")

        # Now integrate forward chaining for repair recommendations
        if backward_conclusion:
            logging.info("Calling forward chaining process for repair recommendation")
            print(f"Problem diagnosed: {backward_conclusion}")
            print("Checking repair recommendations...")
            # Start time for forward chaining
            start_time_fw = time.perf_counter()

            repair_recommendation = FW.process(backward_conclusion.strip().upper())

            # End time for forward chaining
            end_time_fw = time.perf_counter()

            if repair_recommendation:
                logging.info(f"Repair recommendation received: {repair_recommendation}")
                print(f"Recommended Repair: {repair_recommendation}")
                print(f"Time Elapsed for Forward Chaining: {end_time_fw - start_time_fw:0.2f} seconds")
                logging.info(f"Time Elapsed for Forward Chaining: {end_time_fw - start_time_fw:0.2f} seconds")
                # Dynamically generate derived forward variable
                derived_forward_vars[backward_conclusion] = {
                    "derived_variable": repair_recommendation,
                    "dependencies": [backward_conclusion]
                }

                # Write updated derived forward variables to file
                write_to_file(forward_var_file, derived_forward_vars)
            else:
                logging.info("No repair recommendation available for the diagnosed issue.")
                print("No repair recommendation available for the diagnosed issue.")
        else:
            logging.info("No backward conclusion was made.")
            print("No backward conclusion was made.")
    else:
        logging.info("User confirmed car condition is good.")
        print("Your car condition is good")

    # End time for the program
    end_time_program = time.perf_counter()
    end_memory = psutil.Process().memory_info().rss / (1024 * 1024)  # Memory at end in MB

    # Print time and memory information to console
    print(f"Total Time Elapsed for Program: {end_time_program - start_time_program:0.2f} seconds")
    print(f"Memory consumed: {end_memory - start_memory:.2f} MB")

    # Log time and memory consumption
    logging.info(f"Total Time Elapsed for Program: {end_time_program - start_time_program:0.2f} seconds")
    logging.info(f"Memory consumed: {end_memory - start_memory:.2f} MB")
    
    # End of the program
    logging.info("PROGRAM END")
    logging.shutdown()

