import json
import main as M
import logging

# Load the variable list and knowledge base
with open('Forward_Variable_list.json', 'r') as file:
    variable = json.load(file)

with open('Forward_KnowledgeBase.json', 'r') as file1:
    knowledge_base = json.load(file1)

logging.info("Forward chaining started")

def search_cvl(goal_variable):
    logging.info(f"Searching clause variable list for goal: {goal_variable}")
    matching_clauses = []
    for clause, variables in M.FORWARD_CLAUSE_VARIABLE_LIST.items():
        if goal_variable in variables:
            matching_clauses.append(clause)
    logging.info(f"Matching clauses found: {matching_clauses}")
    return matching_clauses

def clause_to_rule(clause):
    rule = (clause // 3) + 1
    logging.info(f"Clause {clause} corresponds to Rule {rule}")
    return rule

def update_VL(clause):
    logging.info(f"Updating variable list for clause: {clause}")
    variable_list = M.FORWARD_CLAUSE_VARIABLE_LIST[clause]
    for v in variable_list:
        if v in variable:
            if variable[v]["Userinput"] == "":
                user_answer = input(variable[v]["Question"])
                logging.info(f"User answer for {v}: {user_answer}")
                variable[v]["Userinput"] = user_answer.lower()
        else:
            logging.warning(f"Variable {v} not found in the variable list.")

def validate_Ri(rule):
    logging.info(f"Validating rule {rule}")
    symptoms = knowledge_base[str(rule)]["SYMPTOMS"]
    
    inputs_match = True
    for v, expected_answer in symptoms.items():
        user_input = variable.get(v, {}).get("Userinput", "").lower()
        if user_input != expected_answer.lower():
            logging.info(f"Validation failed for {v}. Expected: {expected_answer}, got: {user_input}")
            inputs_match = False
            break
    
    if inputs_match:
        conclusion = knowledge_base[str(rule)]["CONCLUSION"]
        logging.info(f"Rule {rule} validated. Conclusion: {conclusion}")
        recommendation = knowledge_base[str(rule)]["RECOMMENDATION"]
        return recommendation
    return None

def process(goal):
    matching_clauses = search_cvl(goal)
    
    while matching_clauses:
        clause = matching_clauses.pop(0)
        logging.info(f"Processing clause: {clause}")
        rule = clause_to_rule(clause)
        update_VL(clause)
        recommendation = validate_Ri(rule)
        if recommendation:
            logging.info(f"Final recommendation: {recommendation}")
            return recommendation
    return None
