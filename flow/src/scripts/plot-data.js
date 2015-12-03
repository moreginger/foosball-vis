import jquery from 'jquery';
import cytoscape from 'cytoscape';

// TODO npm:webcola isn't in a usable state, needs build etc, doesn't support commonjs style.
// require('webcola')
// require('./cola.v3.js')
import * as prep from './prepare-data';

export function plotData(e, elements) {
  cytoscape({

    container: e,

    layout: {
      name: 'preset'
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
        'width': 'mapData(strength, 0, 100, 2, 10)',
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

    ready: function() {
      window.cy = this;
      updateLayout(this);
    }
  });

}

export function updateData(elements) {
  var cy = window.cy;
  window.layout.stop();
  var newNodes = elements.nodes.map(n => n.data.id);
  cy.remove(cy.nodes().filter((_, n) => newNodes.indexOf(n.data('id')) === -1));
  var currentNodes = cy.nodes().toArray().map(n => n.data('id'));
  cy.add(elements.nodes.filter(n => currentNodes.indexOf(n.data.id) === -1).map(n => ({
    group: 'nodes',
    data: n.data
  })));
  cy.remove(cy.edges());
  cy.add(elements.edges.map(e => ({
    group: 'edges',
    data: e.data
  })));
  updateLayout(cy);
}


function updateLayout(cy) {
  // cola is nicer in some ways - in particular it allows the initial node positions to be retained -
  // but it seems to have developed quirks when the graph is updated in Cytochrome.
  var layout = cy.makeLayout({
    name: 'cose',
    coolingFactor: 0.98,
    numIter: 100000,
    padding: 10,
    infinite: true,
  });
  layout.run();
  window.layout = layout;
}
