import * as prep from './prepare-data';
import * as plot from './plot-data';
import * as tntfl from './tntfl-games';

// ES6-style import doesn't work for ion-rangslider. 
global.jQuery = require('jquery');
require('ion-rangeslider');
import moment from 'moment';

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
