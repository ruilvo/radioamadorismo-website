import React from "react";
import { Helmet } from "react-helmet-async";
import { Navbar, Container, Nav, NavDropdown } from "react-bootstrap";

class Header extends React.Component {
  constructor(props) {
    super(props);
    this.state = { title: "Hello world" };
  }

  render() {
    return (
      <Navbar bg="light" expand="lg">
        <Helmet>
          <title>{this.state.title}</title>
        </Helmet>
        <Container>
          <Navbar.Brand href="#home">{this.state.title}</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              <Nav.Link href="#home">Home</Nav.Link>
              <Nav.Link href="#link">Link</Nav.Link>
              <NavDropdown title="Dropdown" id="basic-nav-dropdown">
                <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
                <NavDropdown.Item href="#action/3.2">
                  Another action
                </NavDropdown.Item>
                <NavDropdown.Item href="#action/3.3">
                  Something
                </NavDropdown.Item>
                <NavDropdown.Divider />
                <NavDropdown.Item href="#action/3.4">
                  Separated link
                </NavDropdown.Item>
              </NavDropdown>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    );
  }
}

export default Header;
