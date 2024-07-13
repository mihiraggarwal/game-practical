import { writable } from "svelte/store";

export const global_node_num = writable(0);

export const profile = writable<Array<Array<Array<{action: string, payoff: number[], player: number, num: number, destination: number}>>>>([[[{
    action: "",
    payoff: [],
    player: -1,
    num: -1,
    destination: -1
}]]]);

export const profile_index = writable(0);