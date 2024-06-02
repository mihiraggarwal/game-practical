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
            children: list[list["Node"]] = None, # interpret as all possible children
            actions: tuple[str] = None,
            action: list[str] = None,
            payoffs: tuple[int] = None
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
        if children[i][0].payoffs == None:
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
                "num": nums[i]
            }])

        final_arr.extend(another_arr)

    return sub_nodes, final_arr

def main():
    # arr = [] # dynamic programming 👍

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


    n0 = Node(node_number=0, player=0, children=[], actions=(0, 1, 2))

    n1 = Node(node_number=1, player=1, children=[], actions=("A", "R"))
    n0.children.append([n1])

    n2 = Node(node_number=2, player=1, children=[], actions=("A", "R"))
    n0.children.append([n2])

    n3 = Node(node_number=3, player=1, children=[], actions=("A", "R"))
    n0.children.append([n3])

    n4 = Node(node_number=4, payoffs=(2,0))
    n1.children.append([n4])

    n5 = Node(node_number=5, payoffs=(0,0))
    n1.children.append([n5])

    n6 = Node(node_number=6, payoffs=(1,1))
    n2.children.append([n6])

    n7 = Node(node_number=7, payoffs=(0,0))
    n2.children.append([n7])

    n8 = Node(node_number=8, payoffs=(0,2))
    n3.children.append([n8])

    n9 = Node(node_number=9, payoffs=(0,0))
    n3.children.append([n9])


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

    n, arr = spne([], n0)

    for k in range(len(arr)):
        s0, s1 = [], []
        print(f"SPNE payoff: {arr[k][-1]["payoff"]}")
        for i in range(len(arr[k])-1, -1, -1):
            if "action" in arr[k][i].keys():
                if arr[k][i]["player"] == 0:
                    s0.append({f"n{arr[k][i]["num"]}": arr[k][i]["action"]})
                else:
                    s1.append({f"n{arr[k][i]["num"]}": arr[k][i]["action"]})
        print(f"SPNE strategy profile: ({s0}, {s1})")

if __name__ == '__main__':
    main()