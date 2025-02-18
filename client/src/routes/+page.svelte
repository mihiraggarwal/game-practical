<script>
    import question from "$lib/icons/question-sign.png"
    import play from "$lib/icons/play-button-arrowhead.png"
    import github from "$lib/icons/github.png"
</script>

<div class="container">
    <div></div>
    <div class="main">
        <h1>game-practical</h1>
        <div class="options">
            <a class="link" href="/help"><img src={question} alt="question" class="question"></a>
            <a class="link" href="/play"><img src={play} alt="play" class="play"></a>
            <a href="https://github.com/mihiraggarwal/game-practical" target="_blank" class="link"><img src={github} alt="github" class="github"></a>
        </div>
    </div>
    <footer>
        <p>Made with &lt;3 by <a href="https://github.com/mihiraggarwal" target="_blank">Mihir Aggarwal</a></p>
    </footer>
</div>

<style>
    .container {
        display: flex;
        flex-direction: column;
        min-height: 100vh;
        box-sizing: border-box;
        justify-content: space-between;
        align-items: center;
    }

    .main {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 3vh;
    }

    h1 {
        font-family: "airbnb-bold";
        font-size: 2.5em;
        padding: 0;
        margin: 0;
    }

    .options {
        display: flex;
        gap: 2vw;
    }

    .link {
        border: 3px solid #000;
        border-radius: 100%;
        width: 5rem;
        height: 5rem;
        padding: 0;
        background-color: #fff;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    img {
        width: 2.6rem;
    }

    .play {
        margin-left: 0.5vw;
    }

    .github {
        width: 3.2vw;
    }

    footer {
		border-top: 1px solid #000;
		text-align: center;
		font-family: "airbnb-bold";
        width: 100%;
	}
</style>