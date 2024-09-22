import json
import main as M

# Load the variable list and knowledge base
with open('Forward_Variable_list.json', 'r') as file:
    variable = json.load(file)

with open('Forward_KnowledgeBase.json', 'r') as file1:
    knowledge_base = json.load(file1)

# Function to search for a clause variable list entry
def search_cvl(goal_variable):
    matching_clauses = []
    for clause, variables in M.FORWARD_CLAUSE_VARIABLE_LIST.items():
        if goal_variable in variables:
            matching_clauses.append(clause)
    print(f"Matching clauses for '{goal_variable}': {matching_clauses}")
    return matching_clauses

# Function to convert clause number to rule number
def clause_to_rule(clause):
    rule = (clause // 4) + 1  # Adjust if rules are numbered differently
    print(f"Clause {clause} corresponds to Rule {rule}")
    return rule

# Function to update the variable list
def update_VL(clause):
    print("Begin update")
    variable_list = M.FORWARD_CLAUSE_VARIABLE_LIST[clause]
    for v in variable_list:
        if v in variable:
            if variable[v]["Userinput"] == "":
                user_answer = input(variable[v]["Question"])
                variable[v]["Userinput"] = user_answer.lower()  # Standardize to lower case
        else:
            print(f"Variable {v} not found in variable list.")
    print("End update")


# Function to validate a rule
# def validate_Ri(rule):
#     print("Beginning validation")
#     conclusion = ""
#     symptoms = knowledge_base[str(rule)]["SYMPTOMS"]
    
#     for v, expected_answer in symptoms.items():
#         user_input = variable.get(v, {}).get("Userinput")
#         if user_input != expected_answer:
#             print(f"Validation failed for {v}: expected {expected_answer}, got {user_input}")
#             return None  # Return None if validation fails
    
#     conclusion = knowledge_base[str(rule)]["CONCLUSION"]
#     print(f"Rule validated. Conclusion: {conclusion}")
#     print("Ending validation")
#     return conclusion

def validate_Ri(rule):
    print("Beginning validation")
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
        print(f"Rule validated. Conclusion: {conclusion}")
        recommendation = knowledge_base[str(rule)]["RECOMMENDATION"]
        print(f"Recommended Repair: {recommendation}")  # Return the correct recommendation
        return recommendation
    else:
        conclusion = None
    
    print("Ending validation")
    # return conclusion

# Main process function
def process(goal):
    conclusion = None
    matching_clauses = search_cvl(goal)
    
    while matching_clauses:
        clause = matching_clauses.pop(0)
        print(f"Processing clause: {clause}")
        rule = clause_to_rule(clause)

        update_VL(clause)
        conclusion = validate_Ri(rule)
        if conclusion is not None:
            break
    
            print(f"Final conclusion: {conclusion}")
            return conclusion
        else:
            print("No valid conclusion found.")

    # return "No repair recommendation available for the diagnosed issue."  # Only reached if no valid recommendation is found