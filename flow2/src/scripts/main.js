// this is the main file that pulls in all other modules
// you can require() bower components too!
var prep = require("./prepare-data.js");
var plot = require("./plot-data.js");
var games = require("./games.js");

var data = games.games();
var elements = prep.prepareData(data);
var container = document.getElementById('chart');
plot.plotData(container , elements);

// example.welcome();
// var _ = require("underscore");
