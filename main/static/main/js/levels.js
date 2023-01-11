	const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
	var rotated = false;
	var r = async function() {
		let url = new URL(window.location.href);
		url.searchParams.set("reverse", "True");
		let ID = getRndInteger(1,5);
		let response = await fetch(url, {method:"POST",
			headers:{
				'X-CSRFToken': csrftoken
			}
		});
		let translations = await response.json();
		let tr = translations.translations;

		let elem = document.getElementById("main-word");
		elem.innerText = CapitalizeFirstLetter(tr[ID-1].word)

		for (let i = 0;i < tr.length; i++) {
			elem = document.getElementById("translate-" + (i + 1));
			elem.innerText = CapitalizeFirstLetter(tr[i].translate)
			elem.parentElement.onclick = handleWrongClick;
		}

		elem = document.getElementById("translate-" + ID);
		elem.id = elem.id + "-" + ID
		elem.parentElement.onclick = handleRightClick;
	};
	function getRndInteger(min, max) {
		return Math.floor(Math.random() * (max - min) ) + min;
	}
	function CapitalizeFirstLetter(string) {
		return string.charAt(0).toUpperCase() + string.slice(1)
	}
	function handleWrongClick() {
		this.style.backgroundColor = "#ff0000"; 
	}
	async function handleRightClick() {
		this.style.backgroundColor = "#32cd32";

		let url = new URL(window.location.href);
		url.searchParams.set("reverse", "True");
		let ID = getRndInteger(1,5);
		let response = await fetch(url, {method:"POST",
			headers:{
				'X-CSRFToken': csrftoken
			}
		});
		let translations = await response.json();
		let tr = translations.translations;

		rotated = !rotated;
		this.style.backgroundColor = "";
		let child = this.childNodes[1];
		/*child.innerText = "";*/
		child.id = child.id.split("-")[0]  + "-" + child.id.split("-")[1];

		if (rotated) {
			let flipper = document.getElementById("flipper");
			flipper.style.transform = "rotateY(180deg)";
			/*flipper.style.transformStyle = "preserve-3d";*/
			let elem = document.getElementById("back-main-word");
			elem.innerText = CapitalizeFirstLetter(tr[ID-1].word)

			for (let i = 0;i < tr.length; i++) {
				try {
					elem = document.getElementById("translate-" + (i + 1));
					/*elem.innerText = "";*/
					elem.parentElement.style.backgroundColor = "";
				}
				catch (exception)
				{
				}
			}

			for (let i = 0;i < tr.length; i++) {
				try {
					elem = document.getElementById("backTranslate-" + (i + 1));
					elem.innerText = CapitalizeFirstLetter(tr[i].translate)
					elem.parentElement.onclick = handleWrongClick;
				}
				catch (exception)
				{
				}
			}

			elem = document.getElementById("backTranslate-" + ID);
			elem.id = elem.id + "-" + ID
			elem.parentElement.onclick = handleRightClick;
		}
		else {
			let flipper = document.getElementById("flipper");
			flipper.style.transform = "rotateY(0deg)";
			let elem = document.getElementById("main-word");
			elem.innerText = CapitalizeFirstLetter(tr[ID-1].word)

			for (let i = 0;i < tr.length; i++) {
				try {
					elem = document.getElementById("backTranslate-" + (i + 1));
					/*elem.innerText = "";*/
					elem.parentElement.style.backgroundColor = "";
				}
				catch (exception)
				{
				}
			}

			for (let i = 0;i < tr.length; i++) {
				try {
					elem = document.getElementById("translate-" + (i + 1));
					elem.innerText = CapitalizeFirstLetter(tr[i].translate)
					elem.parentElement.onclick = handleWrongClick;
				}
				catch (exception)
				{
				}
			}

			elem = document.getElementById("translate-" + ID);
			elem.id = elem.id + "-" + ID
			elem.parentElement.onclick = handleRightClick;
		}

	}
	r();