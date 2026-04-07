import { Routes, Route } from "react-router-dom";

export function App() {
  return (
    <Routes>
      <Route path="/" element={<div>[[ project_name ]] — frontend listo</div>} />
    </Routes>
  );
}
