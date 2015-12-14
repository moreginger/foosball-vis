import Reflux from 'reflux';
import LeagueActions from '../../actions/LeagueActions';

var store = Reflux.createStore({
  listenables: LeagueActions,
  onLoad: function() {
    console.log('load');
  },
  onLoadCompleted: function(stuff) {
    console.log('loadCompleted')
    console.log(stuff);
  },
  onLoadFailed: function() {
    console.log('loadFailed');
  }
});

export var LeagueStore = store;
