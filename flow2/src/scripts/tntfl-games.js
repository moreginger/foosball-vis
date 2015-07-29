exports.getGames = function(from, to, callback) {
  var url = 'http://localhost:8000/games.cgi?view=json&from=' + from + '&to=' + to;
  var request = new XMLHttpRequest();
  request.open('GET', url, true);
  request.onload = function() {
    if (request.status >= 200 && request.status < 400) {
      callback(JSON.parse(request.responseText));
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