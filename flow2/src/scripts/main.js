// this is the main file that pulls in all other modules
// you can require() bower components too!
var prep = require('./prepare-data.js');
var plot = require('./plot-data.js');
global.jQuery = require('jquery');
require('ion-rangeslider');
var moment = require('moment');

function update(from, to) {
  var url = 'http://localhost:8000/games.cgi?view=json&from=' + from + '&to=' + to;
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
}

jQuery('#range').ionRangeSlider({
  type: 'double',
  min: +moment().subtract(1, 'years').format('X'),
  max: +moment().add(1, 'months').format('X'),
  from: +moment().subtract(2, 'months').format('X'),
  to: +moment().format('X'),
  prettify: function (num) {
    return moment(num, 'X').format('LL');
  },
  drag_interval: true,
  onFinish: function (data) {
    update(data.from, data.to);
  }
});
