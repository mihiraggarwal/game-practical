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

        constructor(
            node_number: number = 0,
            player: number = 0,
            children: Array<Node> = [],
        ) {
            this.node_number = node_number;
            this.player = player;
            this.children = children;
        }
    }

    const node = new Node($global_node_num)
    global_node_num.update(n => n+1)
</script>

<h1>game-practical</h1>
<div class="pre-tree">
    <label for="players">Number of players</label>
    <input type="number" id="players" name="players" bind:value={nPlayers} required />
</div>
<br /><br />

<div class="tree">

    <Subtree node={node} Node_class={Node} />

    <!-- 
        way to display tree:
        - second row, nodes are spaced-evenly along full width
        - if a row is added, all previous rows' widths are halved along right and left extremes
        - a node's children will get the width of that node / (it + n(siblings))
    -->

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
</style>