import Reflux from 'reflux';

var actions = Reflux.createActions({
  "load": {
    children: ["completed", "failed"]
  }
});

actions.load.listen(function() {
  new Promise(function(resolve, reject) {
    resolve([{
      name: 'tmm',
      points: 100
    }, {
      name: 'tlr',
      points: 101
    }]);
  }).then(this.completed).catch(this.failed);
});

export var LeagueActions = actions;
