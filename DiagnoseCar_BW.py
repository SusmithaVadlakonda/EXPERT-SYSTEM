import json
import main as M
import logging
import os

with open('Backward_Variable_list.json','r')as file:
    variable = json.load(file)

with open('Backward_KnowledgeBase.json','r')as file1:
    knowledge_base = json.load(file1)

with open('Global_Variable.json','r')as file2:
    global_variable = json.load(file2)


def search_con(goal_variable):
    logging.info(f"Searching conclusion list for goal: {goal_variable}")
    matching_goals = []
    for key, value in M.CONCLUSION_LIST.items():
        if value == goal_variable:
            matching_goals.append(key)
    logging.info(f"Matching goals found: {matching_goals}")
    return matching_goals


def rule_to_clause(rule):
  
    return 8 * (rule - 1) + 1

def save_derived_backward_variables(variable_name, value):
    derived_file = 'derived_backward_variables.json'
    
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

def get_yes_or_no_input(question):
    while True:
        user_input = input(question).strip().lower()
        if user_input in ["yes", "no"]:
            return user_input
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def update_VL(clause):
    logging.info(f"Updating variable list for clause: {clause}")
    intermediate_conclude = ""
    variable_list = M.CLAUSE_VARIABLE_LIST[clause]
    for v in variable_list:
        if v in variable:
            if(variable[v]["Userinput"] == ""):
                user_answer = input(variable[v]["Question"])
                variable[v]["Userinput"] = user_answer
                save_derived_backward_variables(v, user_answer)
        else:
            # variable is not in variableList it is an intermediate rule

            conclusion = process(v)
            print(conclusion)
            if conclusion in global_variable:
                if global_variable[v]["value"] == "":
                    global_variable[v]["value"] = "yes"
                    save_derived_backward_variables(v, "yes")
                    logging.info(f"Updated global variable {v} to 'yes'")
            else:
                global_variable[v]["value"] = "no"
                # print(json.dumps(global_variable, indent=2))
                intermediate_conclude = "Cannot find problem"
                break
    # print("end update")
    return intermediate_conclude
    # print(json.dumps(variable, indent=2))


def validate_Ri(rule):
    logging.info(f"Validating rule {rule}")
    conclusion = ""
    for v, answer in knowledge_base[str(rule)]["SYMPTOMS"].items():
        # print(knowledge_base[str(rule)]["SYMPTOMS"].items())
        if v in variable and answer != variable[v]["Userinput"]:
             conclusion = None
             break
        elif v in global_variable and answer != global_variable[v]["value"]:
            conclusion = None
            break
    if conclusion == "":
        conclusion = knowledge_base[str(rule)]["CONCLUSION"]
        # print(conclusion)

    # print("Ending validation")
    return conclusion




def process(goal):
    conclusion = None
    matching_goals = search_con(goal)
    # print(matching_goals)
    while matching_goals :
        rule = matching_goals.pop(0)
        # print("Starting process rule:", rule)
        clause_number = rule_to_clause(rule)
        # print("Starting process clauseNum:", clause_number)

        intermediate_conclude = update_VL(clause_number)
        if intermediate_conclude == "Cannot find problem":
            break

        conclusion = validate_Ri(rule)
        if conclusion != None:
            break
    
    return conclusion
   
