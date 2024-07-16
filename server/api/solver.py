'''
- represent the game as a game tree
- identify all subgames
- for each subgame find the nash
- keep going backward to find the SPNE
- figure out how to get it to work for multiple SPNE

// one step at a time keep relaxing assumptions
- start off with 2 player perfect information finite info sets single PSNE payoff
- bring in PSNE strategy profile (full - along with unreachable strategies)
- bring in multiple PSNE - make arr an array of arrays where each array is one SPNE
- bring in imperfect information
- bring in pure Nash
- bring in multiple players
- bring in MSNE
- bring in nature
- bring in infinite info sets i.e continuous games
- bring in PBE
'''

class Node:
    def __init__(
            self, 
            node_number: int, 
            player: int = None,
            children: list[list["Node"]] = [], # interpret as all possible children
            actions: tuple[str] = [],
            action: list[str] = None,
            payoffs: list[int] = []
        ):
        
        self.node_number = node_number
        self.player = player
        self.children = children
        self.actions = actions
        self.action = action
        self.payoffs = payoffs

def all_perms(max_ls):
    if len(max_ls) == 1:
        return list(map(lambda x: [x], list(range(max_ls[0] + 1))))
    prev = all_perms(max_ls[1:])
    cr = []
    for i in range(max_ls[0] + 1):
        for j in range(len(prev)):
            cr.append([i, *prev[j]])
    return cr

################################# SPNE #################################

def subnash(node: "Node"):
    ch = node.children
    maxp = [len(i)-1 for i in ch]
    perms = all_perms(maxp)

    # outer iteration - each perm
    for p in range(len(perms)):
        internal_sub: list["Node"] = []
        actions = []
        players = []
        node_numbers = []
        max_payoffs = []

        sub_node: "Node" = ()
        max_payoff = [float("-inf") for i in node.children[0][0].payoffs]
        
        # inner iteration gets all possible spne in that perm
        for i in range(len(perms[p])):
            np = node.children[i][perms[p][i]].payoffs[node.player]
            if np < max_payoff[node.player]:
                continue
            elif np > max_payoff[node.player]:
                internal_sub = []
                actions = []
                max_payoffs = []
                players = []
                node_numbers = []
                
            sub_node = node.children[i][perms[p][i]]
            actions.append(node.actions[i])
            max_payoff = sub_node.payoffs
            max_payoffs.append(max_payoff)
            players.append(node.player)
            node_numbers.append(node.node_number)
    
            internal_sub.append(sub_node)

        # this yields all spne of that perm
        yield actions, max_payoffs, players, node_numbers, internal_sub, perms[p]

def spne(arr: list, node: "Node"):
    children = node.children
    main_arr = []
    for i in range(len(children)):
        if children[i][0].payoffs == []:
            ret, ret_arr = spne(arr, children[i][0]) # recursively make all pre-terminal nodes
            children[i] = ret # automatically propagates to node.children
        else:
            ret_arr = [[{
                "payoff": children[i][0].payoffs,
                "num": children[i][0].node_number
            }]] # to get the lengths of node.children and main_arr same
        main_arr.append(ret_arr)

    sub_nodes: list["Node"] = []
    final_arr = []
    for actions, payoffs, players, nums, n, perm in subnash(node):
        sub_nodes.extend(n)

        sub_arr = []

        for i in range(len(perm)):
            sub_arr.extend(main_arr[i][perm[i]])

        another_arr = []
        for i in range(len(actions)):
            another_arr.append([*sub_arr, {
                "action": actions[i],
                "payoff": payoffs[i],
                "player": players[i],
                "num": nums[i],
                "destination": n[i].node_number
            }])

        final_arr.extend(another_arr)

    return sub_nodes, final_arr

################################# Nash Equilibrium #################################

def get_strategies(n0, strategy_sets):
    # identify all information sets first
    # then define a strategy as an action for each information set - find all strategies
    
    # base case
    if n0.payoffs != []:
        return {}

    # induction hypothesis
    interm = {}
    for i in range(len(n0.children)):
        strategy_sets = get_strategies(n0.children[i][0], strategy_sets)
        for j in strategy_sets.keys():
            m = []
            for k in range(len(strategy_sets[j])):
                if j in interm.keys():
                    for l in range(len(interm[j])):
                        m.append([*interm[j][l], *strategy_sets[j][k]])
                else:
                    m.append(strategy_sets[j][k])
            interm[j] = m

    # induction step
    strategy_sets = interm
    k = []
    player = n0.player
    for i in range(len(n0.actions)):
        if player in strategy_sets.keys():
            for j in range(len(strategy_sets[player])):
                k.append([*strategy_sets[player][j], {
                    "node": n0.node_number,
                    "action": n0.actions[i],
                    "index": i
                }])
        else:
            k.append([{
                "node": n0.node_number,
                "action": n0.actions[i],
                "index": i
            }])
    strategy_sets[player] = k

    return strategy_sets

def get_matrix(n0):
    strategy_sets = get_strategies(n0, {})
    
    nplayers = max(strategy_sets.keys()) + 1
    indices = all_perms([len(strategy_sets[i]) - 1 for i in range(nplayers)])

    import numpy as np
    arr = np.ndarray(tuple([len(strategy_sets[i]) for i in range(nplayers)]), np.ndarray)

    for i in range(len(indices)):
        # get strategy profile
        k = []
        for j in range(len(indices[i])):
            k.extend(strategy_sets[j][indices[i][j]])

        # get payoffs
        node = n0
        while node.payoffs == []:
            for m in range(len(k)):
                if k[m]["node"] == node.node_number:
                    node = node.children[k[m]["index"]][0]
                    break
        
        arr[*indices[i]] = {
            "strategy_profile": k,
            "payoff": node.payoffs
        }

    return arr, nplayers, strategy_sets

def nash_eq(n0):
    arr, nplayers, strategy_sets = get_matrix(n0)
    best_responses = []

    for l in range(nplayers):
        indices = all_perms([len(strategy_sets[i]) - 1 for i in range(nplayers) if i != l])

        # set up indices to hold all other players' strategies constant
        for j in range(len(indices)):
            indices[j].insert(l, slice(None))

            max_payoff_arr = [{"payoff": [float("-inf") for _ in range(nplayers)]}]

            for k in range(len(arr[*indices[j]])):
                sub_dict = arr[*indices[j]][k]
                if sub_dict["payoff"][l] > max_payoff_arr[0]["payoff"][l]:
                    max_payoff_arr = [sub_dict]
                elif sub_dict["payoff"][l] == max_payoff_arr[0]["payoff"][l]:
                    max_payoff_arr.append(sub_dict)

            best_responses.extend(max_payoff_arr)

    final_responses = []

    # see if a strategy profile is a best response as many times as there are players
    for i in range(len(best_responses)):
        if best_responses.count(best_responses[i]) >= nplayers and best_responses[i] not in final_responses:
            final_responses.append(best_responses[i])
    
    return final_responses

################################# Main #################################

def main(n0):
    n, arr = spne([], n0)
    payoffs = []
    s = []

    for k in range(len(arr)):
        nplayers = 0
        for i in range(len(arr[k])-1, -1, -1):
            if "action" in arr[k][i].keys():
                if arr[k][i]["player"] > nplayers:
                    nplayers = arr[k][i]["player"]
        sp = [[] for _ in range(nplayers + 1)]
        payoffs.append(arr[k][-1]['payoff'])
        
        for i in range(len(arr[k])-1, -1, -1):
            if "action" in arr[k][i].keys():
                # sp[arr[k][i]["player"]].append({arr[k][i]['num']: arr[k][i]["action"]})
                sp[arr[k][i]["player"]].append(arr[k][i])
        s.append(sp)
    
    return {
        "payoffs": payoffs,
        "profile": s
    }


################################# trial runs #################################

# n0 = Node(node_number=0, player=0, children=[], actions=("S", "C"))

# n1 = Node(node_number=1, player=1, children=[], actions=("S", "C"))
# n0.children.append([n1])

# n2 = Node(node_number=2, player=1, children=[], actions=("S", "C"))
# n0.children.append([n2])

# n3 = Node(node_number=3, payoffs=(2,1))
# n1.children.append([n3])

# n4 = Node(node_number=4, payoffs=(0,0))
# n1.children.append([n4])

# n5 = Node(node_number=5, payoffs=(0,0))
# n2.children.append([n5])

# n6 = Node(node_number=6, payoffs=(1,2))
# n2.children.append([n6])


# n0 = Node(node_number=0, player=0, children=[], actions=(0, 1, 2))

# n1 = Node(node_number=1, player=1, children=[], actions=("A", "R"))
# n0.children.append([n1])

# n2 = Node(node_number=2, player=1, children=[], actions=("A", "R"))
# n0.children.append([n2])

# n3 = Node(node_number=3, player=1, children=[], actions=("A", "R"))
# n0.children.append([n3])

# n4 = Node(node_number=4, payoffs=(2,0))
# n1.children.append([n4])

# n5 = Node(node_number=5, payoffs=(0,0))
# n1.children.append([n5])

# n6 = Node(node_number=6, payoffs=(1,1))
# n2.children.append([n6])

# n7 = Node(node_number=7, payoffs=(0,0))
# n2.children.append([n7])

# n8 = Node(node_number=8, payoffs=(0,2))
# n3.children.append([n8])

# n9 = Node(node_number=9, payoffs=(0,0))
# n3.children.append([n9])


# n0 = Node(node_number=0, player=0, children=[], actions=('G', 'H'))

# n1 = Node(node_number=1, player=1, children=[], actions=("C", "D"))
# n0.children.append([n1])

# n2 = Node(node_number=2, player=1, children=[], actions=("E", "F"))
# n0.children.append([n2])

# n3 = Node(node_number=3, payoffs=(2,2))
# n1.children.append([n3])

# n4 = Node(node_number=4, player=0, children=[], actions=("A", "B"))
# n1.children.append([n4])

# n5 = Node(node_number=5, payoffs=(1,1))
# n2.children.append([n5])

# n6 = Node(node_number=6, payoffs=(2,1))
# n2.children.append([n6])

# n7 = Node(node_number=7, payoffs=(3,2))
# n4.children.append([n7])

# n8 = Node(node_number=8, payoffs=(3,3))
# n4.children.append([n8])


# n0 = Node(node_number=0, player=0, children=[], actions=("U", "D"))
    
# n1 = Node(node_number=1, payoffs=(2,2))
# n0.children.append([n1])

# n2 = Node(node_number=2, player=1, children=[], actions=("L", "R"))
# n0.children.append([n2])

# n3 = Node(node_number=3, payoffs=(3,1))
# n2.children.append([n3])

# n4 = Node(node_number=4, payoffs=(0,0))
# n2.children.append([n4])

# pprint.pp(nash_eq(n0))