import React, { useState, useEffect } from "react";
import axios from "axios";

const VendorForm = () => {
  const [vendors, setVendors] = useState([]);

  const [formData, setFormData] = useState({
    vendor_name: "",
    company_name: "",
    vendor_mobile: "",
    email: "",
    vendor_type: "",
    vendor_code: "",
    gst_number: "",
    website: "",
  });

  // Fields label + required configuration
  const fields = {
    vendor_name: { label: "Vendor Name", required: true },
    company_name: { label: "Company Name", required: true },
    vendor_mobile: { label: "Mobile Number", required: false },
    email: { label: "Email", required: true },
    vendor_type: { label: "Vendor Type", required: false },
    vendor_code: { label: "Vendor Code", required: true },
    gst_number: { label: "GST Number", required: false },
    website: { label: "Website / LinkedIn", required: false },
  };

  // Handle input changes
  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  // Submit form
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://127.0.0.1:8000/vendors/", formData);

      alert("✅ Vendor Added Successfully!");
      console.log("Response:", res.data);

      // Auto-send password email
      const passwordRes = await axios.post(
        "http://127.0.0.1:8000/auth/password-reset-request",
        { email: formData.email },
        { headers: { "Content-Type": "application/json" } }
      );

      alert(passwordRes.data.message);

      // Reset form
      setFormData({
        vendor_name: "",
        company_name: "",
        vendor_mobile: "",
        email: "",
        vendor_type: "",
        vendor_code: "",
        gst_number: "",
        website: "",
      });

      getVendors();
    } catch (err) {
      console.error("❌ Error Response:", err.response?.data);
      alert("❌ Error: " + JSON.stringify(err.response?.data));
    }
  };

  // Fetch vendor list
  const getVendors = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/vendors/");
      setVendors(res.data);
    } catch (err) {
      console.error("Failed to fetch vendors:", err);
    }
  };

  useEffect(() => {
    getVendors();
  }, []);

  return (
    <div className="flex flex-col items-center w-full">
      {/* ---------- Vendor List ---------- */}
      <div className="bg-white shadow-2xl rounded-2xl p-6 w-full max-w-6xl border-t-4 mt-5">
        <h2 className="text-2xl font-bold text-gray-700 mb-4 text-center">
          📋 Vendor List
        </h2>

        <div className="overflow-x-auto">
          <table className="w-full border-collapse text-sm">
            <thead>
              <tr className="bg-blue-200 text-gray-700">
                <th className="border p-2">Name</th>
                <th className="border p-2">Company</th>
                <th className="border p-2">Mobile</th>
                <th className="border p-2">Email</th>
                <th className="border p-2">Type</th>
                <th className="border p-2">Code</th>
                <th className="border p-2">GST</th>
                <th className="border p-2">Website</th>
              </tr>
            </thead>

            <tbody>
              {vendors.length > 0 ? (
                vendors.map((v, i) => (
                  <tr
                    key={i}
                    className={`${
                      i % 2 === 0 ? "bg-white" : "bg-blue-50"
                    } hover:bg-blue-100 transition`}
                  >
                    <td className="border p-2">{v.vendor_name}</td>
                    <td className="border p-2">{v.company_name}</td>
                    <td className="border p-2">{v.vendor_mobile}</td>
                    <td className="border p-2 break-all">{v.email}</td>
                    <td className="border p-2">{v.vendor_type}</td>
                    <td className="border p-2">{v.vendor_code}</td>
                    <td className="border p-2">{v.gst_number}</td>
                    <td className="border p-2 text-blue-600 underline">
                      <a href={v.website} target="_blank" rel="noreferrer">
                        {v.website}
                      </a>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="8" className="text-center py-4 text-gray-500">
                    No vendors found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* ---------- Add Vendor Form ---------- */}
      <div className="bg-white shadow-2xl rounded-2xl p-6 w-full max-w-3xl mt-8 border-t-4">
        <h1 className="text-3xl font-bold text-center mb-5 text-blue-600">
          🧾 Add Vendor
        </h1>

        <form onSubmit={handleSubmit} className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {Object.entries(fields).map(([key, cfg]) => (
            <div key={key} className="flex flex-col">
              <label className="font-semibold mb-1 text-gray-600">
                {cfg.label} {cfg.required && <span className="text-red-500">*</span>}
              </label>

              <input
                name={key}
                value={formData[key]}
                onChange={handleChange}
                className="border border-gray-300 rounded-xl px-3 py-2 text-base focus:outline-none focus:ring-2 focus:ring-blue-400 hover:border-blue-400 transition"
                required={cfg.required}
              />
            </div>
          ))}

          {/* ---------- UPDATED BUTTON ---------- */}
          <div className="col-span-2 flex justify-center mt-4">
            <button
              type="submit"
              className="
                bg-blue-500
                hover:bg-blue-600
                text-white
                font-semibold
                px-4
                py-2
                rounded-full
                shadow-md
                text-sm
                transition
              "
            >
              ➕ Add Vendor
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default VendorForm;
