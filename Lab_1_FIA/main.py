from production import forward_chain
from backchain import backchain_to_goal_tree
import rules

possible_results = ["Kid", "Adult", "Middle_age", "Geezer", "Teen"]



def yes(ques):
    ans = raw_input(ques).lower()
    return ans[0] == 'y'


answers = []


def ask_questions(tree, name):
    if tree is None:
        return
    result = yes(tree.cargo.format(name) + '? y/n ')
    if result:
        answers.append(tree.cargo.format(name))
        ask_questions(tree.left, name)
    else:
        ask_questions(tree.right, name)


run_client = True
results = []
while run_client:
    answers = []
    print('Give name')
    name = raw_input('Name: ')
    type_of_chain = raw_input('Forward or Backward chain?(F/B):')
    if type_of_chain == "F":
        ask_questions(rules.tree, name)
        result = forward_chain(rules.RULES, answers)
        if len(result) != 0:
            results.append(result[-1])
            age = result[-1].split()[-1]
            if age in possible_results:
                print(result[-1])
            else:
                print("Unknown")
        else:
            print("Unknown")
    else:
        age = raw_input('Enter Age:')
        result = backchain_to_goal_tree(rules.RULES, name + ' is a ' + age)
        results.append(result)
        print (results)

        # print (backchain_to_goal_tree(rules.RULES, name + ' is a ' + age))


