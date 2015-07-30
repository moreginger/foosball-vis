// this is the main file that pulls in all other modules
// you can require() bower components too!
var prep = require('./prepare-data.js');
var plot = require('./plot-data.js');
var tntfl = require('./tntfl-games.js');
global.jQuery = require('jquery');
require('ion-rangeslider');
var moment = require('moment');
var now = moment();
var start = moment(now).subtract(2, 'months');

var container = document.getElementById('chart');
tntfl.getGames(parseInt(start.format('X')), parseInt(now.format('X')), function(data) {
  var elements = prep.prepareData(data);
  plot.plotData(container, elements);
});

jQuery('#range').ionRangeSlider({
  type: 'double',
  min: parseInt(moment(now).subtract(1, 'years').format('X')),
  max: parseInt(moment(now).add(1, 'months').format('X')),
  from: parseInt(start.format('X')),
  to: parseInt(now.format('X')),
  prettify: function (num) {
    return moment(num, 'X').format('LL');
  },
  drag_interval: true,
  onFinish: function (data) {
    tntfl.getGames(data.from, data.to, function(data) {
      var elements = prep.prepareData(data);
      plot.updateData(elements);
    });
  }
});
