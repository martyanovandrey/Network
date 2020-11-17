document.addEventListener('DOMContentLoaded', function () {
	document.querySelectorAll(".edit").forEach(e =>
		e.addEventListener("click", function () {
			edit(e.parentNode.id)
		}))
});

function load_post(postbox) {
	if (postbox == '') {
		postbox = 'all'
	}
	fetch(`/posts/${postbox}`)
		.then(response => response.json())
		.then(posts => {
			// Print emails
			posts.forEach(add_posts);
		});
}

function add_posts(object) {
	const post = document.createElement('div');
	post.id = 'post'
	post.dataset.postid = object.id
	post.classList.add('card-body')
	post.classList.add('post')
	post.innerHTML = `
		<h5><a href="/profile/${object.user}">${object.user}</a></h5> 
		<a>Edit</a>
		<span>${object.text}</span>
		<span style='color:#b2b2b2'>${object.timestamp}</span>
		<span>❤️ ${object.likes}</span>
		<a style='color:#c6c6c6'>Comment</a>
		`
	document.querySelector('#posts-view').append(post)
};

function getCookie(name) {
	if (!document.cookie) {
		return null;
	}
	const token = document.cookie.split(';')
		.map(c => c.trim())
		.filter(c => c.startsWith(name + '='));

	if (token.length === 0) {
		return null;
	}
	return decodeURIComponent(token[0].split('=')[1]);
}

function create_post() {
	fetch('/create_post', {
			credentials: 'include',
			method: 'POST',
			mode: 'same-origin',
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json',
				'X-CSRFToken': getCookie('csrftoken')
			},
			body: JSON.stringify({
				post: document.querySelector('#post-text').value,
				username: JSON.parse(document.getElementById('username').textContent)
			})
		})
		.then(response => response.json())
		.then(result => {
			console.log(result);
		});
}

function follow() {
	fetch(`/profile/${this.dataset.mailid}`, {
		method: 'PUT',
		body: JSON.stringify({
			read: true
		})
	})
}

function edit(id) {
	var post_id = document.getElementById(id)
	var post = post_id.querySelector("#edit_text");
	edit_post = post_id.querySelector('#new_text');
	edit_post.style.display = 'block';
	post.style.display = 'none';
	edit_post.innerHTML = post.innerHTML

	var save_button = post_id.querySelector('#save_btn')
	save_button.style.display = 'block';
	save_button.onclick = function () {
		fetch('/create_post', {
				credentials: 'include',
				method: 'PUT',
				mode: 'same-origin',
				headers: {
					'Accept': 'application/json',
					'Content-Type': 'application/json',
					'X-CSRFToken': getCookie('csrftoken')
				},
				body: JSON.stringify({
					id: edit_post.parentNode.id,
					post: edit_post.value,
					username: JSON.parse(document.getElementById('username').textContent)
				})
			})
			.then(response => response.json())
			.then(result => {

			});
		edit_post.style.display = 'none';
		save_button.style.display = 'none';
		post.innerHTML = edit_post.value
		post.style.display = 'block';
	}
};

function like(id) {
	var post_id = document.getElementById(id)
	var post = post_id.querySelector("#edit_text");

	save_button.onclick = function () {
		fetch('/like', {
				credentials: 'include',
				method: 'PUT',
				mode: 'same-origin',
				headers: {
					'Accept': 'application/json',
					'Content-Type': 'application/json',
					'X-CSRFToken': getCookie('csrftoken')
				},
				body: JSON.stringify({
					id: edit_post.parentNode.id,
					post: edit_post.value,
					username: JSON.parse(document.getElementById('username').textContent)
				})
			})
			.then(response => response.json())
			.then(result => {

			});
	}
};