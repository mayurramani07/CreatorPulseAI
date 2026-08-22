import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Engineering from "./pages/Engineering";

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-[#08090d] text-white">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />

          <Route path="/engineering"
            element={<Engineering />} />

        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;