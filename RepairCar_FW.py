import json
import main as M
import logging
import os
# Load the variable list and knowledge base
with open('Forward_Variable_list.json', 'r') as file:
    variable = json.load(file)

with open('Forward_KnowledgeBase.json', 'r') as file1:
    knowledge_base = json.load(file1)

logging.info("Forward chaining started")

# Function to search for a clause variable list entry
def search_cvl(goal_variable):
    logging.info(f"Searching clause variable list for goal: {goal_variable}")
    matching_clauses = []
    for clause, variables in M.FORWARD_CLAUSE_VARIABLE_LIST.items():
        if goal_variable in variables:
            matching_clauses.append(clause)
    # print(f"Matching clauses for '{goal_variable}': {matching_clauses}")
    return matching_clauses

# Function to convert clause number to rule number
def clause_to_rule(clause):
    rule = (clause // 3) + 1  # Adjust if rules are numbered differently
    logging.info(f"Clause {clause} corresponds to Rule {rule}")
    return rule

def save_derived_forward_variables(variable_name, value):
    derived_file = 'derived_forward_variables.json'
    
    # Check if the derived file exists; if not, create it
    if not os.path.exists(derived_file):
        with open(derived_file, 'w') as file:
            json.dump({}, file)  # Start with an empty JSON object
    
    # Load the existing derived variables from the file
    with open(derived_file, 'r') as file:
        derived_variables = json.load(file)
    
    # Update or add the new derived variable
    derived_variables[variable_name] = value
    
    # Save the updated derived variables back to the file
    with open(derived_file, 'w') as file:
        json.dump(derived_variables, file, indent=2)
    
    logging.info(f"Saved derived variable {variable_name}: {value} to {derived_file}")

# Function to prompt the user for a valid "yes" or "no" input
def get_yes_or_no_input(question):
    while True:
        user_input = input(question).strip().lower()
        if user_input in ["yes", "no"]:
            return user_input
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

# Function to update the variable list
def update_VL(clause):
    logging.info(f"Updating variable list for clause: {clause}")
    variable_list = M.FORWARD_CLAUSE_VARIABLE_LIST[clause]
    for v in variable_list:
        if v in variable:
            if variable[v]["Userinput"] == "":
                user_answer = input(variable[v]["Question"])
                variable[v]["Userinput"] = user_answer.lower()  # Standardize to lower case
                save_derived_forward_variables(v, user_answer.lower())  # Save derived variable

        else:
            print(f"Variable {v} not found in variable list.")



def validate_Ri(rule):
    logging.info(f"Validating rule {rule}")
    symptoms = knowledge_base[str(rule)]["SYMPTOMS"]
    
    inputs_match = True
    for v, expected_answer in symptoms.items():
        user_input = variable.get(v, {}).get("Userinput", "").lower()
        if user_input != expected_answer.lower():  # Ensure case-insensitive comparison
            print(f"Validation failed for {v}: expected {expected_answer}, got {user_input}")
            inputs_match = False
            break
    
    if inputs_match:
        conclusion = knowledge_base[str(rule)]["CONCLUSION"]
        # print(f"Rule validated. Conclusion: {conclusion}")
        recommendation = knowledge_base[str(rule)]["RECOMMENDATION"]
        print(f"Recommended Repair: {recommendation}")  # Return the correct recommendation
        return recommendation
    else:
        conclusion = None

# Main process function
def process(goal):
    conclusion = None
    matching_clauses = search_cvl(goal)
    
    while matching_clauses:
        clause = matching_clauses.pop(0)
        # print(f"Processing clause: {clause}")
        rule = clause_to_rule(clause)

        update_VL(clause)
        conclusion = validate_Ri(rule)
        if conclusion is not None:
            break
    
            print(f"Final conclusion: {conclusion}")
            return conclusion
        else:
            print("No valid conclusion found.")
