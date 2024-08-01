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
            imperfect_to: list[int] = [],
            payoffs: list[int] = []
        ):
        
        self.node_number = node_number
        self.player = player
        self.children = children
        self.actions = actions
        self.action = action
        self.imperfect_to = imperfect_to
        self.payoffs = payoffs

def all_perms(max_ls):
    if len(max_ls) == 0:
        return []
    elif len(max_ls) == 1:
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
            node_numbers.append([node.node_number, *node.imperfect_to])
    
            internal_sub.append(sub_node)

        # this yields all spne of that perm
        yield actions, max_payoffs, players, node_numbers, internal_sub, perms[p]

def valid_subgame(node: "Node"):
    if len(node.imperfect_to) != 0:
        return False
    
    all_imperfects = []
    all_nodes = []

    def get_nodes(node: "Node"):

        all_nodes.append(node.node_number)
        all_imperfects.extend(node.imperfect_to)

        for i in range(len(node.children)):
            get_nodes(node.children[i][0])
    
    get_nodes(node)
    
    for i in range(len(all_imperfects)):
        if all_imperfects[i] not in all_nodes:
            return False
    
    return True

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
                "num": [children[i][0].node_number]
            }]] # to get the lengths of node.children and main_arr same
        
        main_arr.append(ret_arr)

    sub_nodes: list["Node"] = []
    final_arr = []

    # node doesn't start a subgame - thus, return
    if not valid_subgame(node):
        perms = all_perms([len(main_arr[i])-1 for i in range(len(main_arr))])
        for perm in perms:
            sub_arr = []

            for i in range(len(perm)):
                sub_arr.extend(main_arr[i][perm[i]])

            another_arr = []
            another_arr.append([*sub_arr])

            final_arr.extend(another_arr)
        
        return [node], final_arr

    # chck if all children are perfect subgames
    flag = True
    for i in range(len(children)):
        if children[i][0].payoffs == []:
            if not valid_subgame(children[i][0]):
                flag = False
                break

    # there exists a child which isn't a perfect subgame - thus, nash
    if not flag:
        for perm, nash in nash_eq(node):
            for j in range(len(nash)):
                sub_nodes.append(nash[j]["payoff_node"])
            
            sub_arr = []
            for i in range(len(perm)):
                sub_arr.extend(main_arr[i][perm[i]])

            another_arr = []
            for i in range(len(nash)):
                inner_arr = []
                for k in range(len(nash[i]["strategy_profile"])):
                    inner_arr.append({
                        "action": nash[i]["strategy_profile"][k]["action"],
                        "payoff": nash[i]["payoff"],
                        "player": nash[i]["strategy_profile"][k]["player"],
                        "num": nash[i]["strategy_profile"][k]["num"],
                    })
                another_arr.append([*sub_arr, *inner_arr])
            final_arr.extend(another_arr)
        
        return sub_nodes, final_arr

    # all children are perfect subgames - thus, spne
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
            }])

        final_arr.extend(another_arr)

    return sub_nodes, final_arr

################################# Nash Equilibrium #################################

removed = []

def get_strategies(n0, strategy_sets):
    # base case
    if n0.payoffs != []:
        return {}

    # induction hypothesis
    interm = {}
    for i in range(len(n0.children)):

        if n0.children[i][0].node_number not in removed:
            for j in range(len(n0.children[i][0].imperfect_to)):
                removed.append(n0.children[i][0].imperfect_to[j])

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
    if n0.node_number in removed:
        return interm
    
    strategy_sets = interm
    k = []
    player = n0.player
    for i in range(len(n0.actions)):
        if player in strategy_sets.keys():
            for j in range(len(strategy_sets[player])):
                k.append([*strategy_sets[player][j], {
                    "num": [n0.node_number, *n0.imperfect_to],
                    "action": n0.actions[i],
                    "index": i,
                    "player": player
                }])
        else:
            k.append([{
                "num": [n0.node_number, *n0.imperfect_to],
                "action": n0.actions[i],
                "index": i,
                "player": player
            }])
    strategy_sets[player] = k

    return strategy_sets

def get_matrix(n0):
    strategy_sets = get_strategies(n0, {})

    nplayers = max(strategy_sets.keys()) + 1
    indices = all_perms([len(strategy_sets[i]) - 1 for i in range(nplayers)])

    # will contain all possible matrices
    big_arr = []

    # contains the max index of each perm.
    # ex: if the root's child's 1st child has 2 perms, the root's child's 1st index will be 1
    # format: {node_number: [(action index, max_index)]}
    children_n_map = {}
    def get_children_n(node):
        if node.payoffs == []:
            for m in range(len(node.children)):
                if node.children[m][0].payoffs != []:
                    if children_n_map.get(node.node_number) is None:
                        children_n_map[node.node_number] = [(m, len(node.children[m]) - 1)]
                    else:
                        children_n_map[node.node_number].append((m, len(node.children[m]) - 1))
                get_children_n(node.children[m][0])
    
    get_children_n(n0)

    # will contain the possible perms for each pre terminal node
    ret_perms = [{k: [(v[w][0], None) for w in range(len(v))] for k, v in children_n_map.items()}]

    ch = n0.children

    # gets the possible perms of all the children of the node
    def find_total(node):
        if node.payoffs != []:
            return []
        total = []
        for i in range(len(node.children)):
            if node.children[i][0].payoffs != []:
                total.append(len(node.children[i]) - 1)
            else:
                total.extend(find_total(node.children[i][0]))
        return total

    # index all perms using just the root node's direct children
    final_perms = {}
    for i in range(len(ch)):
        subnode = ch[i][0]
        if subnode.payoffs != []:
            final_perms[subnode.node_number] = [[]]
            continue
        final_perms[subnode.node_number] = all_perms(find_total(subnode))
    
    for k, v in children_n_map.items():
        each_list = list(map(lambda x: x[1], v))
        each_perms = all_perms(each_list)

        # get a copy of the current ret_perms
        # defined like this to avoid making a reference to ret_perms
        current_perms = [{k: v.copy() for k, v in ret_perms[o].items()} for o in range(len(ret_perms))]
        ret_perms = []
        for i in range(len(each_perms)):

            # get a copy of the current current_perms
            # needed to do this since ret_perms are updated every inner iteration but
            # we need the old ret_perms for all inner iterations, hence current_perms
            inside_perm = [{k: v.copy() for k, v in current_perms[o].items()} for o in range(len(current_perms))]

            for j in range(len(inside_perm)):
                inside_perm[j][k] = [(v[w][0], b) for w, b in zip(range(len(v)), each_perms[i])]
            ret_perms.extend(inside_perm)

    import numpy as np

    # populating big_arr
    for r in range(len(ret_perms)):
        big_arr.append([])
        sub_arr = np.ndarray(tuple([len(strategy_sets[i]) for i in range(nplayers)]), np.ndarray)

        for i in range(len(indices)):
            # get strategy profile
            k = []
            for j in range(len(indices[i])):
                k.extend(strategy_sets[j][indices[i][j]])

            # get payoffs
            node = n0
            index = -1
            while node.payoffs == []:
                for m in range(len(k)):
                    if node.node_number in k[m]["num"]:
                        if node.children[k[m]["index"]][0].payoffs != []:
                            index = k[m]["index"]
                            node_perm = ret_perms[r][node.node_number]
                            for pn in range(len(node_perm)):
                                if node_perm[pn][0] == index:
                                    cnode_perm = node_perm[pn][1]
                            node = node.children[k[m]["index"]][cnode_perm]
                            break
                        node = node.children[k[m]["index"]][0]
                        break
            
            sub_arr[tuple(indices[i])] = {
                "strategy_profile": k,
                "payoff": node.payoffs,
                "payoff_node": node
            }
            
        big_arr[r] = sub_arr

    # convert ret_perms back to original form: remove the index tuple
    for i in range(len(ret_perms)):
        for k, v in ret_perms[i].items():
            ret_perms[i][k] = [j[1] for j in v]

    # ret_perms has all possible perms of pre terminal nodes
    # while final_perms has all possible perms indexed by the root's direct children
    # we need to return in the format of final_perms thus, converting ret_perms' format to final_perms'
    unified_perms = []
    for pm in range(len(ret_perms)):
        d = {}
        for i in range(len(n0.children)):
            unified_child = []
            node = n0.children[i][0]
            
            def find_nodes(node):
                c = 0
                for n in range(len(node.children)):
                    if node.children[n][0].payoffs != []:
                        unified_child.append(ret_perms[pm][node.node_number][c])
                        c += 1
                    find_nodes(node.children[n][0])
        
            find_nodes(node)

            d[node.node_number] = unified_child
        unified_perms.append(d)
            
    ret_perms = unified_perms

    # returns the final list of perms
    true_perms = []
    for i in range(len(ret_perms)):
        ind = []
        for k, v in ret_perms[i].items():
            ind.append(final_perms[k].index(v))
        true_perms.append(ind)

    return big_arr, true_perms, nplayers, strategy_sets

def nash_eq(n0):

    # when called from the spne function, it must also take into account multiple possible children
    # done in get_matrix

    fin_matrix, perms, nplayers, strategy_sets = get_matrix(n0)

    for p in range(len(fin_matrix)):

        best_responses = []

        for l in range(nplayers):

            if nplayers > 1:
                indices = all_perms([len(strategy_sets[i]) - 1 for i in range(nplayers) if i != l])
            else:
                indices = [[]]

            # set up indices to hold all other players' strategies constant
            for j in range(len(indices)):
                indices[j].insert(l, slice(None))

                max_payoff_arr = [{"payoff": [float("-inf") for _ in range(nplayers)]}]

                for k in range(len(fin_matrix[p][tuple(indices[j])])):
                    sub_dict = fin_matrix[p][tuple(indices[j])][k]

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
        
        yield perms[p], final_responses

################################# Main #################################

def main_spne(n0):
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

def main_nash(n0):
    final_response = []
    for _, i in nash_eq(n0):
        final_response.extend(i)
    ret = {"payoffs": [], "profile": []}
    for i in range(len(final_response)):
        ret["profile"].append(final_response[i]["strategy_profile"])
        ret["payoffs"].append(final_response[i]["payoff"])

    return ret


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

# n1.imperfect_to = [2, 3]
# n2.imperfect_to = [1, 3]
# n3.imperfect_to = [1, 2]

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


# n0 = Node(node_number=0, player=0, children=[], actions=("A", "B"))

# n1 = Node(node_number=1, player=1, children=[], actions=("C", "D"))
# n0.children.append([n1])

# n2 = Node(node_number=2, player=1, children=[], actions=("E", "F"))
# n0.children.append([n2])

# n3 = Node(node_number=3, player=0, children=[], actions=("G", "H"))
# n1.children.append([n3])

# n4 = Node(node_number=4, player=0, children=[], actions=("I", "J"))
# n1.children.append([n4])

# n5 = Node(node_number=5, player=0, children=[], actions=("K", "L"))
# n2.children.append([n5])

# n6 = Node(node_number=6, player=0, children=[], actions=("M", "N"))
# n2.children.append([n6])

# n3.imperfect_to = [6]
# n4.imperfect_to = [5]
# n6.imperfect_to = [3]
# n5.imperfect_to = [4]

# n7 = Node(node_number=7, payoffs=(2,0))
# n3.children.append([n7])

# n8 = Node(node_number=8, payoffs=(0,0))
# n3.children.append([n8])

# n9 = Node(node_number=9, payoffs=(1,1))
# n4.children.append([n9])

# n10 = Node(node_number=10, payoffs=(0,0))
# n4.children.append([n10])

# n11 = Node(node_number=11, payoffs=(0,2))
# n5.children.append([n11])

# n12 = Node(node_number=12, payoffs=(0,0))
# n5.children.append([n12])

# n13 = Node(node_number=13, payoffs=(0,0))
# n6.children.append([n13])

# n14 = Node(node_number=14, payoffs=(0,0))
# n6.children.append([n14])


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