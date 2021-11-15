import React from "react";
import { Container } from "react-bootstrap";
import { Outlet } from "react-router-dom";

class MainBody extends React.Component {
  render() {
    return (
      <Container>
        <Outlet />
      </Container>
    );
  }
}

export default MainBody;
