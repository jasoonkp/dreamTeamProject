import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Navigation } from './components/routes/navigation/navigation.jsx';
import { Home } from "./components/routes/home/home.jsx"

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigation />}>
        <Route index element={<Home />} />
      </Route>
    </Routes>
  );
}

export default App;
