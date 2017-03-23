var PythonShell = require('python-shell');
var pyshell = new PythonShell('the_best_art.py', { mode: 'text'});
pyshell.on('message', function (message) {
    console.log(message);
});
