let form = document.querySelector('#loginForm');

runEventListeners();
function runEventListeners()
{
    form.addEventListener('submit', search);
}
async function search(e)
{
    e.preventDefault();

    let name = document.querySelector('#exampleInputEmail1').value;
    let pass = document.querySelector('#exampleInputPassword1').value;
    console.log(name, pass);

	try {
        const response = await fetch("http://localhost:8000/user/login",{
            method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
            body: JSON.stringify({
				"username": name,
                "password": pass
            }),
        })
		.then((response)  => {return response})
        .then((result) => {
			if(result.status === 200)
			{
                alert("Login successful");
			}
			else 
				alert("Please check your login information.");
		})
    } catch (error) {
        console.log(error);
    }
}
// let check = true;

// function createPromise()
// {
// 	return new Promise((resolve, reject) => {
// 		if (check)
// 			resolve("Success");
// 		else
// 			reject("Error");
// 	})
// }

// createPromise()
// .then((response) => {
// 	console.log(response);
// })
// .catch((error) => {
// 	console.log(error);
// })
// .finally(() => {
// 	console.log("Promise is settled");
// })



// function readStudents(url)
// {
// 	return new Promise((resolve, reject) => {
// 		const xhr = new XMLHttpRequest();
// 		try
// 		{
// 			xhr.addEventListener("readystatechange", () => {
// 					if (xhr.readyState === 4 && xhr.status === 200)
// 						resolve(JSON.parse(xhr.responseText));
// 		})
// 		}
// 		catch (error)
// 		{
// 			reject(error);
// 		}
// 		xhr.open("GET", url);
// 		xhr.send();
// 	})
// }
// readStudents("student.json")
// .then((response) => {
// 	console.log(response);
// })
// .catch((error) => {
// 	console.log(error);
// })

// function getUsers(url)
// {
// 	return new Promise((resolve, reject) => {
// 		const xhr = new XMLHttpRequest();
// 		try
// 		{
// 			xhr.addEventListener("readystatechange", () => {
// 				if (xhr.readyState === 4 && xhr.status === 200)
// 					resolve(JSON.parse(xhr.responseText));
// 			})
// 		}
// 		catch (error)
// 		{
// 			reject(error);
// 		}
// 		xhr.open("GET", url);
// 		xhr.send();
// 	})
// }
// function getCommentsByUserID(url)
// {
// 	return new Promise((resolve, reject) => {
// 		const xhr = new XMLHttpRequest();
// 		try
// 		{
// 			xhr.addEventListener("readystatechange", () => {
// 				if (xhr.readyState === 4 && xhr.status === 200)
// 					resolve(JSON.parse(xhr.responseText));
// 			})
// 		}
// 		catch (error)
// 		{
// 			reject(error);
// 		}
// 		xhr.open("GET", url);
// 		xhr.send();
// 	})
// }

// getUsers("https://jsonplaceholder.typicode.com/users/3")
// .then((response) => {
// 	console.log(response);
// 	return getCommentsByUserID(`https://jsonplaceholder.typicode.com/comments/${response.id}`);
// })
// .then((res) => {console.log(res)})
// .catch((error) => {
// 	console.log(error);
// })


// console.log(this);

// fetch("student.json");

// function getStudents(url)
// {
// 	// const promise = fetch(url);
// 	// console.log(promise);
// 	fetch(url)
// 	.then((response) => {return response.json()})
// 	.then((data) => {console.log(data)})
// 	// .catch((error) => {console.log(error)});
// }

// getStudents("student.json");



// function getData(url)
// {
// 	fetch(url)
// 	.then((response) => {return response.json()})
// 	.then((data) => {console.log(data)})
// 	.catch((error) => {console.log(error)});
// }

// getData("https://jsonplaceholder.typicode.com/users");


// async function hello()
// {
// 	return	"Hello";
// }

// hello()
// .then((response) => {console.log(response)})

