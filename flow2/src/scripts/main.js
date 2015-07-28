// this is the main file that pulls in all other modules
// you can require() bower components too!
var prep = require("./prepare-data.js");
var plot = require("./plot-data.js");

var url = 'https://www.int.corefiling.com/~tmm/TNTFL-web/games.cgi?view=json&from=' + Math.floor(Date.now() / 1000 - 60 * 24 * 60 * 60);
console.log(url);
var request = new XMLHttpRequest();
request.open('GET', url, true);
request.onload = function() {
  if (request.status >= 200 && request.status < 400) {
    var data = JSON.parse(request.responseText);
    var elements = prep.prepareData(data);
    var container = document.getElementById('chart');
    plot.plotData(container , elements);
  }
  else {
    console.log(request)
  }
};
request.onerror = function() {
  console.log(request)
};
request.send();

// example.welcome();
// var _ = require("underscore");
