import React from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import VendorForm from "./components/VendorForm";
import ForgotPassword from "./components/ForgotPassword";
import ResetPassword from "./components/ResetPassword";

function App() {
  return (
    <Router>
      <MainLayout />
    </Router>
  );
}

function MainLayout() {
  const navigate = useNavigate();

  const handleClose = () => {
    // Navigate to home or any other desired route on close
    navigate("/home");
  };

  return (
    <div className="min-h-screen flex flex-col relative">

      {/* ✅ Close Button (Top Right Corner, Always Visible & Clickable) */}
      {/* <button
        onClick={handleClose}
        className="absolute top-3 right-3 bg-red-600 text-white px-3 py-2 
                   rounded-full text-sm font-semibold shadow-lg hover:bg-red-700 
                   transition z-50"
      >
        ✕
      </button> */}

      {/* Header */}
      <header className="w-full bg-gradient-to-r from-blue-600 to-blue-800 text-white py-4 shadow-md">
        <h1 className="text-center text-2xl sm:text-3xl font-bold tracking-wide drop-shadow-md">
          Vendor Management System
        </h1>
      </header>

      {/* Main Content */}
      <main className="flex-grow w-full flex justify-center items-start p-3 sm:p-6 md:p-8">
        <Routes>
          <Route path="/" element={<VendorForm />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/reset-password/:token" element={<ResetPassword />} />
          <Route path="/home" element={<div ></div>} />
        </Routes>
      </main>

      {/* Footer */}
      <footer className="w-full bg-blue-900 text-white text-center py-3 text-xs sm:text-sm">
        © {new Date().getFullYear()} Vendor Management
      </footer>
    </div>
  );
}

export default App;
