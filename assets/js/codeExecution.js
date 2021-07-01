function sendreq() {
	formdata = new FormData(document.querySelector('form'));
	const terminal = document.querySelector('.terminal .output');
	const xhr = new XMLHttpRequest();
	xhr.responseType = 'json';
	xhr.open('POST', '/code/execute/');
	xhr.send(formdata);
	xhr.onload = () => {
		console.log(xhr);
		terminal.innerHTML = '';
		res = xhr.response;
		let count = 1;
		res.output.forEach((result) => {
			card = document.createElement('div');
			card.classList.add('result');
			card.innerHTML = `Test Case ${count}: `;
			if (result.passed) {
				card.classList.add('success');
				card.innerHTML += 'Passed';
			} else {
				card.classList.add('failed');
				card.innerHTML += `Failed: ${result.error}`;
			}
			terminal.appendChild(card);
			count++;
		});
	};
}
const codeConsole = document.querySelector('textarea');
codeConsole.addEventListener('keydown', (e) => {
	if (e.keyCode == 9) {
		var index = codeConsole.selectionStart;
		codeConsole.value =
			codeConsole.value.slice(0, index) +
			'    ' +
			codeConsole.value.slice(index);
		codeConsole.select();
		codeConsole.selectionStart = index + 4;
		codeConsole.selectionEnd = index + 4;
		e.preventDefault();
	}
});
