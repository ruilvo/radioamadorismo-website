import { Helmet } from "react-helmet-async";

function App() {
  return (
    <h1 className="site-heading">
      <Helmet>
        <title>Hello World</title>
      </Helmet>
      Hello world!
    </h1>
  );
}

export default App;
