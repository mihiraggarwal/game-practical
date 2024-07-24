import { writable } from "svelte/store";

export const global_node_num = writable(0);

export const profile = writable<Array<Array<Array<{action: string, payoff: number[], player: number, num: number[], destination: number}>>>>([[[{
    action: "",
    payoff: [],
    player: -1,
    num: [-1],
    destination: -1
}]]]);

export const profile_index = writable(0);

class Node {
    public node_number: number
    public player: number
    public children: Array<Node>
    public actions: Array<string>
    public imperfect_to: Array<Node|number>
    public payoffs: Array<number>

    constructor(
        node_number: number,
        player: number = 0,
        children: Array<Node> = [],
        actions: Array<string> = [],
        imperfect_to: Array<Node|number> = [],
        payoffs: Array<number> = [],
    ) {
        this.node_number = node_number;
        this.player = player;
        this.children = children;
        this.actions = actions;
        this.imperfect_to = imperfect_to;
        this.payoffs = payoffs;
    }
}

export const current_imperfection = writable<Array<Node>>([])

export const any_imperfect = writable(false)

export const all_imperfections = writable<Array<Array<Node>>>([])