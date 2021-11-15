import React from "react";
import axios from "axios";
import { Table } from "react-bootstrap";

class RepeatersView extends React.Component {
  constructor(props) {
    super(props);
    this.state = { repeaters: [] };
  }

  componentDidMount() {
    this.refreshList();
  }

  refreshList = () => {
    axios
      .get("/api/v1/")
      .then((res) => {
        this.setState({ repeaters: res.data });
      })
      .catch((err) => {
        console.log(err);
      });
  };

  getRepeatersAsRows = () => {
    return this.state.repeaters.map((repeater) => (
      <tr key={repeater.id}>
        <td>{repeater.id}</td>
        <td>{repeater.callsign}</td>
      </tr>
    ));
  };

  render() {
    return (
      <div>
        <h1>Repetidores nacionais</h1>
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>#</th>
              <th>Callsign</th>
            </tr>
          </thead>
          <tbody>{this.getRepeatersAsRows()}</tbody>
        </Table>
      </div>
    );
  }
}

export default RepeatersView;
