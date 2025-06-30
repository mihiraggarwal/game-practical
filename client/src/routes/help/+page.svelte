<div class="main">
    <div class="help">
        <h1>game-practical</h1>
        <p class="subhead">game-practical is an extensive form game tree solver. It can calculate the Pure Strategy Nash Equilibrium and Subgame Perfect Nash Equilibrium of any perfect and imperfect game tree which is discrete and finite.</p>

        <h2>How to use</h2>
        <ul>
            <li>Click on the + button to add a new node.</li>
            <li>Choose whether the node is going to be a move or a payoff</li>
            <li>If the node is a move:</li>
            <ul>
                <li>Enter the player number</li>
                <li>Add all actions that the player takes from that node</li>
            </ul>
            <li>If the node is a payoff:</li>
            <ul>
                <li>Enter the payoff for each player of the game separated by a comma (,)</li>
            </ul>
            <li>If you want to add an imperfect information set</li>
            <ul>
                <li>Right click on all of the nodes that will be a part of that set - they should turn blue</li>
                <li>Click on the Add Imperfect Info Set button to save the set</li>
                <li>You can view all your imperfect info sets using the circle buttons at the top of the page</li>
            </ul>
            <li>Make sure your tree is complete before requesting a solution</li>
            <li>Click on the whichever solution concept you want the tree to be evaluated using (Nash / SPNE)</li>
            <li>Wait for the solution to load - this may take a bit of time</li>
            <li>Once the solution is calculated, the nodes part of the solution should turn green and the payoff for that profile should be visible</li>
            <li>In case of multiple solutions, you can toggle between them using the circle buttons on the bottom.</li>
        </ul>

        <h2>Core Concepts</h2>
        <ul>
            <li><span>Player: </span>A player is a participant in the game who makes decisions based on the information available to them.</li>
            <li><span>Action: </span>An action is a move that a player plays. A valid strategy must specify an action at each of the player's information sets.</li>
            <li><span>Information Set: </span>An information set is a set of nodes in the game tree that are indistinguishable to a player when making a decision.</li>
            <li><span>Payoff: </span>A payoff is a set of numbers that represent the outcome of the game for each player in the game tree.</li>
            <li><span>Pure Strategy: </span>A pure strategy a strategy in which a player chooses one and only one action at each information set.</li>
            <li><span>Extensive Form Game Tree: </span>An extensive form game tree is a tree representation of a sequential game, where players make decisions at different points in time. Every normal form game can be converted into an extensive form game.</li>
            <li><span>Nash Equilibrium: </span>A pure strategy Nash equilibrium is a set of strategies, one for each player, such that no player has a unilateral incentive to deviate from their strategy given the strategies of the other players.</li>
            <li><span>Subgame Perfect Nash Equilibrium: </span>A subgame perfect Nash equilibrium is a set of credible strategies, one for each player, such that the strategy profile specifies a Nash equilibrium in every subgame of the original game.</li>
        </ul>

        <h2>Issues</h2>
        <ul>
            <li>If the game tree isn't correctly setup, the site may throw an error or continuously keep loading failing to produce a solution.</li>
            <li>Due to the complexity of the algorithm, the site may take a bit of time to calculate the solution for the game tree.</li>
            <li>If the site keeps loading for too long, it's possible that the algorithm has run into an unanticipated error. In any such cases, please reach out to me via <a href="mailto:mail@mihiraggarwal.me" target="_blank">email</a> by sending me a screenshot of the game tree, and I'll try to fix the issue.</li>
        </ul>
    </div>

    <footer>
        <p>Made with &lt;3 by <a href="https://mihiraggarwal.me" target="_blank">Mihir Aggarwal</a></p>
    </footer>
</div>


<style>
    .main {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
    }

    .help {
        display: flex;
        flex-direction: column;
        gap: 2vh;
        padding: 3vh;
        border: 3px solid #000;
        margin: 5vh;
        border-radius: 5px;
    }

    h1 {
        font-family: "airbnb-bold";
        font-size: 2.25em;
        text-align: center;
        padding: 0;
        margin: 0;
        margin-bottom: 3vh;
    }

    h2 {
        font-family: "airbnb-bold";
        font-size: 1.5em;
        padding: 0;
        margin: 0;
        margin-top: 2vh;
    }

    ul {
        margin: 0;
    }

    .subhead, li {
        font-family: "Inter";
        font-size: 1em;
        padding: 0;
        margin: 0;
    }

    span {
        font-family: "airbnb-bold";
    }

    footer {
		border-top: 1px solid #000;
		text-align: center;
		font-family: "airbnb-bold";
        width: 100%;
	}
</style>