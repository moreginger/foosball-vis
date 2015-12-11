import React, { PropTypes, Component } from 'react';
import { Nav, NavItem } from 'react-bootstrap';
import LeagueTable from '../LeagueTable';

class League extends Component {

  constructor(props) {
    super(props);
    this.state = {
      tab: 1,
      data: [{
        name: 'tmm',
        points: 100
      }, {
        name: 'tlr',
        points: 101
      }]
    };
  }
  
  handleSelect = (selectedKey) => {
    this.setState({
      tab: selectedKey
    });
  }

  render() {
    return (
      <div>
        <Nav bsStyle='tabs' activeKey={this.state.tab} onSelect={this.handleSelect}>
          <NavItem eventKey={1}>Current</NavItem>
          <NavItem eventKey={2}>All Time</NavItem>
        </Nav>
        <LeagueTable data={this.state.data}/>
      </div>
    );
  }
}

export default League;
