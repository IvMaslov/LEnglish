const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
	async function registerUser() {
		let url = new URL(window.location.href);
		let nickname = document.getElementById("nicknameFormControl").value;
		let email = document.getElementById("emailFormControl").value;
		let password = document.getElementById("passwordFormControl").value;

		let response = await fetch(url, {
			method: "POST",
			headers:{
				"X-CSRFToken": csrftoken,
				"Content-Type": "application/json"
			},
			body: JSON.stringify({"email": email, "nickname": nickname, "password": password})
		});
		resp_status = await response.json();
		console.log(resp_status);
		if (resp_status.status == "0")
			window.location.href = "{% url 'auth' %}";
		else if (resp_status.status == "1")
			fillFields();
		else if (resp_status.status == "2")
			console.log("User already exists");
	}
	function fillFields() {
		/*const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
		const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))*/
		let popover = new bootstrap.Popover(document.querySelector('[data-bs-toogle="popover"]'));

	}