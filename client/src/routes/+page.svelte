<script lang="ts">
	import { PUBLIC_SERVER_URL } from "$env/static/public";
    /*
    SOP for tree
    - ask for number of players
    - get initial node and get the player on it
    - get actions on initial node
    and so on
    - in the end, get payoffs
    */

    import Subtree from "$lib/components/Subtree.svelte";
    import { global_node_num } from "$lib/stores";

    let answer: string = "";

    class Node {
        public node_number: number
        public player: number
        public children: Array<Node>
        public actions: Array<string>
        public payoffs: Array<number>

        constructor(
            node_number: number,
            player: number = 0,
            children: Array<Node> = [],
            actions: Array<string> = [],
            payoffs: Array<number> = [],
        ) {
            this.node_number = node_number;
            this.player = player;
            this.children = children;
            this.actions = actions;
            this.payoffs = payoffs;
        }
    }

    const node = new Node($global_node_num)
    global_node_num.update(n => n+1)

    const solve = () => {
        fetch(`${PUBLIC_SERVER_URL}/solve`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(node)
        }).then(resp => {
            resp.text().then(data => {
                answer = data
            })
        })
    }
</script>

<div class="container">
    <h1>game-practical</h1>

    <div class="tree">

        <Subtree node={node} Node_class={Node} />

    </div>

    <div class="answer-container">
        <button on:click={solve}>SPNE</button>
        <div class="ans">{answer}</div>
    </div>
</div>

<style>
    .container {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 5vh 5vw;
        box-sizing: border-box;
        gap: 7.5vh;
    }

    h1 {
        font-family: "airbnb-bold";
        text-align: center;
        font-size: 2.25em;
        margin: 0;
    }

    .tree {
        display: flex;
        align-items: center;
        flex-direction: column;
    }

    .answer-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 2vh;
    }

    button {
        background-color: #fff;
        border: 3px solid #000;
        color: #000;
        /* font-weight: bold; */
        border-radius: 7px;
        height: 100%;
        padding: 0.5vw 1vw;
        font-size: 1em;
    }

    button:hover {
        cursor: pointer;
    }

    .ans {
        font-size: 1.2em;
    }
</style>