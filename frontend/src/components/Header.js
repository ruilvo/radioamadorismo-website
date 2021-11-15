import React from "react";
import { Helmet } from "react-helmet-async";
import { Navbar, Container, Nav } from "react-bootstrap";
import { Link } from "react-router-dom";

class Header extends React.Component {
  constructor(props) {
    super(props);
    this.state = { title: "Portal do radioamadorismo" };
  }

  render() {
    return (
      <Navbar bg="dark" variant="dark">
        <Helmet>
          <title>{this.state.title}</title>
        </Helmet>
        <Container>
          <Navbar.Brand as={Link} to="/">
            {this.state.title}
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              <Nav.Link as={Link} to="/link">
                Link
              </Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    );
  }
}

export default Header;
