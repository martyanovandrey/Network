document.addEventListener('DOMContentLoaded', function () {
	document.querySelector('#all-posts').addEventListener('click', () => load_post('all'));
	document.querySelector('#user-posts').addEventListener('click', () => load_post(document.querySelector('#user-posts').innerHTML));
});

function load_post(postbox) {
	console.log(postbox)
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
	// Create data-id with mail id
	post.dataset.postid = object.id
	post.classList.add('card-body')
	post.classList.add('post')
	/* Another way to add listen function

	const element = document.createElement('div');
	element.innerHTML = 'This is the content of the div.';
	element.addEventListener('click', function() {
		console.log('This element has been clicked!')
	});
	document.querySelector('#emails-view').append(element);
	*/

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
			// Print result
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