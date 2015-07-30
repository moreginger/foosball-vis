exports.prepareData = function(data) {
  var rels = {};

  rels.getRel = function(p1, p2) {
    var name = p1 > p2 ? p1 + ":" + p2 : p2 + ":" + p1;
    if (!(name in rels)) {
      rels[name] = { p1: p1, p2: p2, flow: 0 };
    }
    return rels[name];
  };
  data.forEach(function(g) {
    var rel = rels.getRel(g.red.name, g.blue.name);
    var flow = g.red.name === rel.p1 ? g.red.skillChange : -g.red.skillChange;
    rel.flow += flow;
  });

  var edges = [];
  for (var key in rels) {
    // TODO: remove stupid hack. Added method isOwnProperty so we need to skip.
    if (!rels.hasOwnProperty(key) || key === "getRel") {
      continue;
    }
    var r = rels[key];
    var absFlow = Math.abs(r.flow);
    edges.push({
      data : {
        source: r.flow < 0 ? r.p1 : r.p2,
        target: r.flow < 0 ? r.p2 : r.p1,
        strength: 4 * absFlow,
        faveColor: '#6FB1FC'
      }
    });
  }
  edges.sort(function(a, b) { return b.data.strength - a.data.strength });
  edges = edges.slice(0, Math.min(edges.length, 32));

  var players = [];
  players.addPlayer = function(p) {
    if (players.indexOf(p) === -1) {
      players.push(p);
    }
  };
  edges.forEach(function(e) {
    players.addPlayer(e.data.source);
    players.addPlayer(e.data.target);
  });

  var nodes = [];
  players.forEach(function(p) {
    nodes.push({
      data : {
        id: p,
        name: p,
        weight: 60,
        faveColor: '#6FB1FC'
      }
    });
  });

  var result = {
    nodes: nodes,
    edges: edges
  };

  return result;
}
