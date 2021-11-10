import React from "react";
import { Container } from "react-bootstrap";
import RepeatersView from "./RepeatersView";

class MainBody extends React.Component {
  render() {
    return (
      <Container fluid="xl">
        <RepeatersView />
      </Container>
    );
  }
}

export default MainBody;
