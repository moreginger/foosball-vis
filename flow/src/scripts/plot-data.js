import cytoscape from 'cytoscape';
// TODO npm:webcola isn't in a usable state, needs build etc, doesn't support commonjs style.
// require('webcola')
// require('./cola.v3.js')
import * as prep from './prepare-data';

export function plotData(e, elements) {

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

    ready: function(){
      window.cy = this;
    }
  });

}

export function updateData(elements) {
  var cy = window.cy;
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
  cy.layout();
}
