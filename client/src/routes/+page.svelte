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

    let nPlayers: number;
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

<h1>game-practical</h1>
<div class="pre-tree">
    <label for="players">Number of players</label>
    <input type="number" id="players" name="players" bind:value={nPlayers} required />
</div>
<br /><br />

<div class="tree">

    <Subtree node={node} Node_class={Node} />

</div>

<div class="answer-container">
    <button on:click={solve}>SPNE</button>
    <div class="ans">{answer}</div>
</div>

<style>
    h1 {
        font-family: "Inter";
        text-align: center;
    }

    .pre-tree {
        display: flex;
        justify-content: center;
        gap: 1vw
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
        border-radius: 5px;
        height: 100%;
        padding: 0.5vw 1vw;
        margin-top: 2vh;
    }

    button:hover {
        cursor: pointer;
    }

    .ans {
        font-size: 1.2em;
    }
</style>