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

    # sub_nodes: set["Node"] = set()
    sub_nodes: list["Node"] = []
    for p in range(len(perms)):
        # internal_sub = set()
        internal_sub = []
        sub_node: "Node" = ()
        max_payoff = [float("-inf") for i in node.children[0][0].payoffs]
        action = ""
        for i in range(len(perms[p])):
            np = node.children[i][perms[p][i]].payoffs[node.player]
            if np < max_payoff[node.player]:
                continue
            elif np > max_payoff[node.player]:
                internal_sub = []
            sub_node = node.children[i][perms[p][i]]
            action = node.actions[i]
            max_payoff = sub_node.payoffs
    
            internal_sub.append(sub_node)
        
        for i in range(len(internal_sub)):
            sub_nodes.append(internal_sub[i])

    return action, max_payoff, node.player, node.node_number, sub_nodes

def spne(arr: list, node: "Node"):
    children = node.children
    main_arr = []
    for i in range(len(children)):
        if children[i][0].payoffs == None:
            ret, ret_arr = spne(arr, children[i][0]) # recursively make all pre-terminal nodes
            children[i] = ret # automatically propagates to node.children
            main_arr.extend(ret_arr)
    action, payoff, player, num, n = subnash(node)
    main_arr.append({
        "action": action,
        "payoff": payoff,
        "player": player,
        "num": num
    })
    return n, main_arr # find the nash of a pre-terminal node

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

    print(n)
    for i in range(len(n)):
        print(n[i].payoffs)

    s0, s1 = [], []
    print(f"SPNE payoff: {arr[-1]["payoff"]}")
    for i in range(len(arr)-1, -1, -1):
        if arr[i]["player"] == 0:
            s0.append({f"n{arr[i]["num"]}": arr[i]["action"]})
        else:
            s1.append({f"n{arr[i]["num"]}": arr[i]["action"]})
    print(f"SPNE strategy profile: ({s0}, {s1})")

if __name__ == '__main__':
    main()