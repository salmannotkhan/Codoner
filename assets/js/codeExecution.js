function sendreq() {
	formdata = new FormData(document.querySelector('form'));
	const terminal = document.querySelector('.terminal .output');
	const xhr = new XMLHttpRequest();
	xhr.responseType = 'json';
	xhr.open('POST', '/code/execute/');
	xhr.send(formdata);
	xhr.onload = () => {
		console.log(xhr);
		res = xhr.response;
		if (res.error) {
			terminal.classList.add('error');
			terminal.innerText = res.details;
		} else {
			terminal.classList.add('success');
			terminal.classList.remove('error');
			htmlOutput = res.output.replaceAll(' ', '&nbsp;');
			htmlOutput = htmlOutput.replaceAll('\n', '<br>');
			console.log(htmlOutput);
			terminal.innerHTML = htmlOutput;
		}
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
