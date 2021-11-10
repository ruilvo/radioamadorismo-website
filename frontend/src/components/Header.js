import React from "react";
import { Helmet } from "react-helmet-async";
import { Navbar, Container } from "react-bootstrap";

class Header extends React.Component {
  constructor(props) {
    super(props);
    this.state = { title: "Portal do radioamadorismo" };
  }

  render() {
    return (
      <Navbar bg="light" expand="lg">
        <Helmet>
          <title>{this.state.title}</title>
        </Helmet>
        <Container>
          <Navbar.Brand>{this.state.title}</Navbar.Brand>
        </Container>
      </Navbar>
    );
  }
}

export default Header;
