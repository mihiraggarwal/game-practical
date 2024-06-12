<script lang="ts">
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
    let nNodes: number = 0;

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
        const display_node = (n: Node) => {
            if (n.payoffs.length > 0) console.log(n)
            else {
                console.log(n)
                n.children.forEach((element: Node) => {
                    display_node(element)
                });
            }
        }
        display_node(node)
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

<button on:click={solve}>Solve</button>

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

    button {
        background-color: #fff;
        border: 3px solid #000;
        color: #000;
        border-radius: 5px;
        height: 100%;
        width: 6vw;
        margin: auto;
        margin-top: 2vh;
        display: block;
    }

    button:hover {
        cursor: pointer;
    }
</style>