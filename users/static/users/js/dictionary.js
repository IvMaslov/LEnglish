const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
	var deleting = null;

	let selected = document.querySelectorAll(".selected");
	for (var i = 0; i < selected.length; i++) {
		selected[i].addEventListener("focus", selectedWord);
		selected[i].addEventListener("blur", blurWord)
	}

	async function addNewWord() {
		let newWord = document.getElementById("new-word");
		newWord.style.display = "inline";
	}

	async function successNewWord() {
		let word = document.getElementById("word-input").value;
		let translate = document.getElementById("translate-input").value;
		let level = document.getElementById("level-input").value

		if (!!word && !!translate)
		{
			response = await fetch("/create/word", {
				method:"POST",
				headers: {
					"X-CSRFToken": csrftoken,
					"Content-Type": "application/json"
				},
				body: JSON.stringify({
								"word": word,
								"translate": translate,
								"level": level
							})
			});
			window.location.reload(true);
		}
		else 
		{
			let wordElem = document.getElementById("new-word");
			wordElem.style.display = "none";	
		}
	}

	async function deleteWord() {
		console.log(deleting);
		let word = deleting.children[0].innerText;
		let translate = deleting.children[1].innerText;
		let level = deleting.children[2].innerText

		console.log(word);
		console.log(translate);
		console.log(level);

		response = await fetch("/delete/word", {
				method:"POST",
				headers: {
					"X-CSRFToken": csrftoken,
					"Content-Type": "application/json"
				},
				body: JSON.stringify({
								"word": word,
								"translate": translate,
								"level": level
							})
		});
		deleting.style.display = "none";
		deleting = null;
	}

	async function selectedWord() {
		this.children[0].classList = ["col-3"];
		this.children[3].style.display = "inline";
		deleting = this;
	}

	async function blurWord() {
		this.children[0].classList = ["col-4"];
		this.children[3].style.display = "none";
	}
