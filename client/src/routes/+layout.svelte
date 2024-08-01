<script>

</script>

<div class="app">
	<main>
		<slot />
		<footer>
			<p>Made with &lt;3 by <a href="https://github.com/mihiraggarwal" target="_blank">Mihir Aggarwal</a></p>
		</footer>
	</main>
</div>

<style>
	@font-face {
        src: url(../../../font/AirbnbCerealBold.ttf);
        font-family: "airbnb-bold"
    }

	footer {
		border-top: 1px solid #000;
		text-align: center;
		font-family: "airbnb-bold";
	}
</style>
