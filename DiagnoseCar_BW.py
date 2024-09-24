import json
import main as M
import logging

with open('Backward_Variable_list.json','r')as file:
    variable = json.load(file)

with open('Backward_KnowledgeBase.json','r')as file1:
    knowledge_base = json.load(file1)

with open('Global_Variable.json','r')as file2:
    global_variable = json.load(file2)

logging.info("Backward chaining started")

def search_con(goal_variable):
    logging.info(f"Searching conclusion list for goal: {goal_variable}")
    matching_goals = []
    for key, value in M.CONCLUSION_LIST.items():
        if value == goal_variable:
            matching_goals.append(key)
    logging.info(f"Matching goals found: {matching_goals}")
    return matching_goals

def rule_to_clause(rule):
    clause = 8 * (rule - 1) + 1
    logging.info(f"Rule {rule} corresponds to Clause {clause}")
    return clause

def update_VL(clause):
    logging.info(f"Updating variable list for clause: {clause}")
    intermediate_conclude = ""
    variable_list = M.CLAUSE_VARIABLE_LIST[clause]
    user_responses = {}
    for v in variable_list:
        if v in variable:
            if variable[v]["Userinput"] == "":
                user_answer = input(variable[v]["Question"])
                logging.info(f"User answer for {v}: {user_answer}")
                variable[v]["Userinput"] = user_answer
                user_responses[v] = user_answer.lower()
        else:
            conclusion = process(v)
            if conclusion in global_variable:
                global_variable[v]["value"] = "yes"
                logging.info(f"Updated global variable {v} to 'yes'")
            else:
                global_variable[v]["value"] = "no"
                intermediate_conclude = "Cannot find problem"
                logging.warning("Cannot find problem for intermediate variable")
                break
    return user_responses 

def validate_Ri(rule):
    logging.info(f"Validating rule {rule}")
    for v, answer in knowledge_base[str(rule)]["SYMPTOMS"].items():
        if v in variable and answer != variable[v]["Userinput"]:
            return None
        elif v in global_variable and answer != global_variable[v]["value"]:
            return None
    conclusion = knowledge_base[str(rule)]["CONCLUSION"]
    logging.info(f"Validation success for rule {rule}. Conclusion: {conclusion}")
    return conclusion

def process(goal):
    matching_goals = search_con(goal)
    while matching_goals:
        rule = matching_goals.pop(0)
        clause_number = rule_to_clause(rule)
        user_responses = update_VL(clause_number)
        intermediate_conclude = update_VL(clause_number)
        if intermediate_conclude == "Cannot find problem":
            break
        conclusion = validate_Ri(rule)
        if conclusion:
            return conclusion, user_responses  # Return the conclusion and the symptoms collected
    return None, {}