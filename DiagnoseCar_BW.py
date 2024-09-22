import json
import main as M

with open('Backward_Variable_list.json','r')as file:
    variable = json.load(file)

with open('Backward_KnowledgeBase.json','r')as file1:
    knowledge_base = json.load(file1)

with open('Global_Variable.json','r')as file2:
    global_variable = json.load(file2)


def search_con(goal_variable):
    matching_goals = []
    for key, value in M.CONCLUSION_LIST.items():
        if value == goal_variable:
            matching_goals.append(key)
    return matching_goals


def rule_to_clause(rule):
    return 8 * (rule - 1) + 1


def update_VL(clause):
    print("Begin update")
    intermediate_conclude = ""
    variable_list = M.CLAUSE_VARIABLE_LIST[clause]
    for v in variable_list:
        if v in variable:
            if(variable[v]["Userinput"] == ""):
                user_answer = input(variable[v]["Question"])
                variable[v]["Userinput"] = user_answer
        else:
            # variable is not in variableList it is an intermediate rule
            conclusion = process(v)
            if conclusion in global_variable:
                if global_variable[v]["value"] == "":
                    global_variable[v]["value"] = "yes"
                    print(json.dumps(global_variable, indent = 2))
            else:
                global_variable[v]["value"] = "no"
                print(json.dumps(global_variable, indent=2))
                intermediate_conclude = "Cannot find problem"
                break
    print("end update")
    return intermediate_conclude
    # print(json.dumps(variable, indent=2))


def validate_Ri(rule):
    print("Begining validation")
    conclusion = ""
    for v, answer in knowledge_base[str(rule)]["SYMPTOMS"].items():
        print(knowledge_base[str(rule)]["SYMPTOMS"].items())
        if v in variable and answer != variable[v]["Userinput"]:
             conclusion = None
             break
        elif v in global_variable and answer != global_variable[v]["value"]:
            conclusion = None
            break
    if conclusion == "":
        conclusion = knowledge_base[str(rule)]["CONCLUSION"]
        print(conclusion)

    print("Ending validation")
    return conclusion




def process(goal):
    conclusion = None
    matching_goals = search_con(goal)
    print(matching_goals)
    while matching_goals :
        rule = matching_goals.pop(0)
        print(rule)
        clause_number = rule_to_clause(rule)
        print(clause_number)

        intermediate_conclude = update_VL(clause_number)
        if intermediate_conclude == "Cannot find problem":
            break

        conclusion = validate_Ri(rule)
        if conclusion != None:
            break
    print(intermediate_conclude)
    print(conclusion)
    return conclusion
    # print(json.dumps(variable, indent = 2))
