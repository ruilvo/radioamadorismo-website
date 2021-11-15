import React from "react";
import { Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import MainBody from "./components/MainBody";
import RepeatersView from "./components/views/RepeatersView";

function App() {
  return (
    <React.Fragment>
      <Header />
      <Routes>
        <Route path="/" element={<MainBody />}>
          <Route index element={<RepeatersView />} />
          <Route path="*" element={<h1>Not found!</h1>} />
        </Route>
      </Routes>
    </React.Fragment>
  );
}

export default App;
