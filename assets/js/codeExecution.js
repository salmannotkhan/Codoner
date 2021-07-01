const terminal = document.querySelector('.terminal .output');
const totalTestCases = document.getElementById('totalTestCases').value;
const form = document.getElementsByTagName('form')[0];
const currentCase = document.getElementById('currentCase');
const codeConsole = document.querySelector('textarea');
const runBtn = document.getElementById('run');
const xhr = new XMLHttpRequest();
var totalPassed = 0;
xhr.responseType = 'json';

xhr.onreadystatechange = () => {
	if (xhr.readyState == 4) {
		card = document.createElement('div');
		card.classList.add('result');
		card.innerHTML = `Test Case ${parseInt(currentCase.value) + 1}: `;
		res = xhr.response;
		if (res.passed) {
			card.classList.add('success');
			card.innerHTML += 'Passed';
			totalPassed++;
		} else {
			card.classList.add('failed');
			card.innerHTML += `Failed: ${res.error}`;
		}
		terminal.appendChild(card);
		currentCase.value = parseInt(currentCase.value) + 1;
		if (parseInt(currentCase.value) < totalTestCases) {
			formdata = new FormData(form);
			xhr.open('POST', '/code/execute/');
			xhr.send(formdata);
			runBtn.value = `${runBtn.value}.`;
		} else {
			runBtn.disabled = false;
			runBtn.value = 'Run';
			if (totalPassed == totalTestCases) {
				alert('Miracle!');
			}
		}
	}
};

function sendreq() {
	currentCase.value = 0;
	runBtn.disabled = true;
	runBtn.value = 'Running.';
	totalPassed = 0;
	formdata = new FormData(form);
	xhr.open('POST', '/code/execute/');
	xhr.send(formdata);
	terminal.innerHTML = '';
}

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
