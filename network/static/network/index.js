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

function create_post() {
    console.log('reretrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')
	fetch('/create_post', {
			method: 'POST',
			body: JSON.stringify({
				post: document.querySelector('#new-post').value
			})
		})
		.then(response => response.json())
		.then(result => {
			// Print result
			console.log(result);
        });
}
