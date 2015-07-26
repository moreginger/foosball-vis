System.import('npm:cytoscape').catch(function(_) {
  // Fails due to import of childprocess on a browser, hence catch not then.
  cyto(document.getElementById('chart'), elements(games));
});

function elements(data) {
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

  var players = [];
  players.addPlayer = function(p) {
    if (players.indexOf(p) === -1) {
      players.push(p);
    }
  };
  var edges = [];
  for (key in rels) {
    // TODO: remove stupid hack. Added method isOwnProperty so we need to skip.
    if (!rels.hasOwnProperty(key) || key === "getRel") {
      continue;
    }
    var r = rels[key];
    var absFlow = Math.abs(r.flow);
    if (absFlow < 10) {
      continue;
    }
    players.addPlayer(r.p1);
    players.addPlayer(r.p2);
    edges.push({
      data : {
        source: r.flow < 0 ? r.p1 : r.p2,
        target: r.flow < 0 ? r.p2 : r.p1,
        strength: 4 * absFlow,
        faveColor: '#6FB1FC'
      }
    });
  }
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
  console.log("whee");
  console.log(result);

  return result;
};

function cyto(e, elements) {

  cytoscape({

    container: e,

    layout: {
      name: 'cola',
      padding: 10,
      infinite: true,
    },

    style: cytoscape.stylesheet()
      .selector('node')
        .css({
          'shape': 'octagon',
          'width': 'mapData(weight, 40, 80, 20, 60)',
          'content': 'data(name)',
          'text-valign': 'center',
          'text-outline-width': 2,
          'text-outline-color': 'data(faveColor)',
          'background-color': 'data(faveColor)',
          'color': '#fff'
        })
      .selector(':selected')
        .css({
          'border-width': 3,
          'border-color': '#333'
        })
      .selector('edge')
        .css({
          'opacity': 0.666,
          'width': 'mapData(strength, 70, 100, 2, 6)',
          'target-arrow-shape': 'triangle',
          'line-color': 'data(faveColor)',
          'source-arrow-color': 'data(faveColor)',
          'target-arrow-color': 'data(faveColor)'
        })
      .selector('.faded')
        .css({
          'opacity': 0.25,
          'text-opacity': 0
        }),

    elements: elements,

    /*{
      nodes: [
        { data: { id: 'j', name: 'Jerry', weight: 65, faveColor: '#6FB1FC', faveShape: 'triangle' } },
        { data: { id: 'e', name: 'Elaine', weight: 45, faveColor: '#EDA1ED', faveShape: 'ellipse' } },
        { data: { id: 'k', name: 'Kramer', weight: 75, faveColor: '#86B342', faveShape: 'octagon' } },
        { data: { id: 'g', name: 'George', weight: 70, faveColor: '#F5A45D', faveShape: 'rectangle' } }
      ],
      edges: [
        { data: { source: 'j', target: 'e', faveColor: '#6FB1FC', strength: 90 } },
        { data: { source: 'j', target: 'k', faveColor: '#6FB1FC', strength: 70 } },
        { data: { source: 'j', target: 'g', faveColor: '#6FB1FC', strength: 80 } },

        { data: { source: 'e', target: 'j', faveColor: '#EDA1ED', strength: 95 } },
        { data: { source: 'e', target: 'k', faveColor: '#EDA1ED', strength: 60 }, classes: 'questionable' },

        { data: { source: 'k', target: 'j', faveColor: '#86B342', strength: 100 } },
        { data: { source: 'k', target: 'e', faveColor: '#86B342', strength: 100 } },
        { data: { source: 'k', target: 'g', faveColor: '#86B342', strength: 100 } },

        { data: { source: 'g', target: 'j', faveColor: '#F5A45D', strength: 90 } }
      ]
    }, */

    ready: function(){
      window.cy = this;

      // giddy up
    }
  });

}
