import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";



import VendorManagement from "./pages/Vendormanagement";

function App() {
  return (
    <Router>
      
      <div className="min-h-screen bg-gray-100 p-4 sm:p-8">
        <Routes>
          {/* Default route → Show Vendors List */}
          <Route path="/"  />
          <Route path="/vendors" element={<VendorManagement />} />
        </Routes>
      </div>

      
    </Router>
  );
}

export default App;
