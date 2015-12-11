import React, { PropTypes, Component } from 'react';
import { Nav, NavItem } from 'react-bootstrap';

class League extends Component {

  constructor(props) {
    super(props);
    this.state = {
      tab: 1
    };
    //this.handleSelect = this.handleSelect.bind(this); // Weird
  }

  handleSelect = (selectedKey) => {
    this.setState({
      tab: selectedKey
    });
  }

  render() {
    return (
      <Nav bsStyle='tabs' activeKey={this.state.tab} onSelect={this.handleSelect}>
        <NavItem eventKey={1}>Current</NavItem>
        <NavItem eventKey={2}>All Time</NavItem>
      </Nav>
    );
  }
}

export default League;
