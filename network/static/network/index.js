/* document.addEventListener('DOMContentLoaded', function () {

	// Use buttons to toggle between views
    document.querySelector('#post').addEventListener('click', () => load_post());
}) */

function load_post() {
    console.log('rwerwrwere1111111111111111111111')
	fetch(`/posts`)
		.then(response => response.json())
		.then(posts => {
			// Print emails
			console.log(posts);
		});
}

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
    console.log('reretrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')
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
				user: `${ user.username }`
			})
		})
		.then(response => response.json())
		.then(result => {
			// Print result
			console.log(result);
        });
}

