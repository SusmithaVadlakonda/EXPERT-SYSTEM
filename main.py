import DiagnoseCar_BW as BW
import RepairCar_FW as FW
import time
import psutil
import logging

# Setup logging configuration for both file and console
logging.basicConfig(filename='auto_repair_log.log', 
                    level=logging.INFO, 
                    format='%(asctime)s %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S',
                    force=True)

# Test log entry for verification
logging.info("PROGRAM START")



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
    129 : ["HAVING DIFFICULTY", "CANNOT SLOWDOWN WHEN BRAKING"],
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
    backward_conclusion = None
    start_time_bw = None
    end_time_bw = None
    start_memory = psutil.Process().memory_info().rss / (1024 * 1024)
    logging.info("Starting backward chaining process")
    
    user_input = input("Does your car have a problem?")
    logging.info(f"User input received: {user_input}")
    if user_input == "yes":
        goal_variable = input("Which part of your car has problem? please choice [starting problem, engine issue, transition problem,brake problem, steer problem, exhaust problem]")
        logging.info(f"Goal variable selected: {goal_variable}")
        
        # Handle different goal variables for backward chaining
        if goal_variable == "starting problem":
            logging.info("Defining goal variable as 'STARTING PROBLEM'")
            start_time_bw = time.perf_counter()
            backward_conclusion = BW.process("STARTING PROBLEM")
            end_time_bw = time.perf_counter()
        elif goal_variable == "engine issue":
            logging.info("Defining goal variable as 'ENGINE ISSUE'")
            start_time_bw = time.perf_counter()
            backward_conclusion = BW.process("ENGINE ISSUE")
            end_time_bw = time.perf_counter()
        elif goal_variable == "transition problem":
            logging.info("Defining goal variable as 'TRANSMISSION ISSUE'")
            start_time_bw = time.perf_counter()
            backward_conclusion = BW.process("TRANSMISSION ISSUE")
            end_time_bw = time.perf_counter()
        elif goal_variable == "brake problem":
            logging.info("Defining goal variable as 'BRAKE ISSUE'")
            start_time_bw = time.perf_counter()
            backward_conclusion = BW.process("BRAKE ISSUE")
            end_time_bw = time.perf_counter()
        elif goal_variable == "steer problem":
            logging.info("Defining goal variable as 'STEER PROBLEM'")
            start_time_bw = time.perf_counter()
            backward_conclusion = BW.process("STEER PROBLEM")
            end_time_bw = time.perf_counter()
        elif goal_variable == "exhaust problem":
            logging.info("Defining goal variable as 'EXHAUST PROBLEM'")
            start_time_bw = time.perf_counter()
            backward_conclusion = BW.process("EXHAUST PROBLEM")
            end_time_bw = time.perf_counter()
  

        # Now integrate forward chaining for repair recommendation
        if backward_conclusion:
            logging.info("Calling forward chaining process for repair recommendation")
            print(f"Problem diagnosed: {backward_conclusion}")
            print("Checking repair recommendations...")
            start_time_fw = time.perf_counter()
            repair_recommendation = FW.process(backward_conclusion.strip().upper())
            end_time_fw = time.perf_counter()
            if repair_recommendation:
                print(f"Recommended Repair: {repair_recommendation}")
                print(f"Time Elapsed for Forward chaining : {end_time_fw - start_time_fw:0.2f} Secs")
                
        elif backward_conclusion == None:
            print("No repair recommendation available for the diagnosed issue.")
    else:
        print("Your car condition is good")
    
    end_memory = psutil.Process().memory_info().rss / (1024 * 1024)  # Memory at end in MB
    
    print(f"Time Elapsed for Backward chaining : {end_time_bw - start_time_bw:0.2f} Secs")
   
    print(f"Memory consumed: {end_memory - start_memory:.2f} MB")







