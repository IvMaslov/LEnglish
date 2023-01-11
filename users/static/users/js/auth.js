	const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
	async function authenticateUser() {
		let url = new URL(window.location.href);
		let nickname = "";//document.getElementById("nicknameFormControl").value;
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
		response_data = await response.json();
		console.log(response_data);

		if(response_data.status == "0")
			window.location.href = response_data.url;
		else
			console.log("Wrong data!");
	}