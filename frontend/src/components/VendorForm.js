import React, { useState, useEffect, useRef } from "react";
import axios from "axios";

const VendorForm = ({ initialData, onSave }) => {
  const isEdit = Boolean(initialData);

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

  const [errors, setErrors] = useState({});
  const fieldRefs = {
    vendor_name: useRef(null),
    company_name: useRef(null),
    email: useRef(null),
  };

  useEffect(() => {
    if (isEdit) {
      setFormData(initialData);
    }
  }, [initialData]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setErrors({ ...errors, [e.target.name]: "" });
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.vendor_name.trim())
      newErrors.vendor_name = "Vendor name is required.";
    if (!formData.company_name.trim())
      newErrors.company_name = "Company name is required.";
    if (!formData.email.trim())
      newErrors.email = "Email is required.";

    setErrors(newErrors);

    if (Object.keys(newErrors).length > 0) {
      const firstErrorKey = Object.keys(newErrors)[0];
      fieldRefs[firstErrorKey]?.current?.scrollIntoView({
        behavior: "smooth",
        block: "center",
      });
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    try {
      if (isEdit) {
        await axios.put(`http://127.0.0.1:8000/vendors/${initialData.id}`, formData);
        alert("Vendor Updated Successfully!");
      } else {
        await axios.post("http://127.0.0.1:8000/vendors/", formData);
        alert("Vendor Added Successfully!");

        // await axios.post(
        //   "http://127.0.0.1:8000/auth/password-reset-request",
        //   { email: formData.email }
        // );
      }
      onSave();
    } catch (err) {
      if (err.response?.status === 400) {
        setErrors({ email: "This email already exists. Please use another email." });
        fieldRefs.email?.current?.scrollIntoView({ behavior: "smooth", block: "center" });
      } else {
        alert("Something went wrong, please try again.");
      }
    }
  };

  return (
    <div className="bg-white p-4 max-w-3xl mx-auto overflow-y-auto" style={{ maxHeight: "90vh" }}>
      <h1 className="text-xl font-bold text-center mb-6 text-blue-500">
        {isEdit ? "Edit Vendor" : "Add New Vendor"}
      </h1>

      <form className="grid grid-cols-1 sm:grid-cols-2 gap-6" onSubmit={handleSubmit}>
        
        {/* Vendor Name */}
        <div ref={fieldRefs.vendor_name}>
          <label className="block text-gray-600 font-medium mb-1">
            Vendor Name <span className="text-red-500">*</span>
          </label>
          <input
            name="vendor_name"
            value={formData.vendor_name}
            onChange={handleChange}
            className="w-full border border-gray-300 rounded-lg px-3 py-2"
          />
          {errors.vendor_name && (
            <p className="text-red-600 text-sm mt-1">{errors.vendor_name}</p>
          )}
        </div>

        {/* Company Name */}
        <div ref={fieldRefs.company_name}>
          <label className="block text-gray-600 font-medium mb-1">
            Company Name <span className="text-red-500">*</span>
          </label>
          <input
            name="company_name"
            value={formData.company_name}
            onChange={handleChange}
            className="w-full border border-gray-300 rounded-lg px-3 py-2"
          />
          {errors.company_name && (
            <p className="text-red-600 text-sm mt-1">{errors.company_name}</p>
          )}
        </div>

        {/* Email */}
        <div ref={fieldRefs.email}>
          <label className="block text-gray-600 font-medium mb-1">
            Email <span className="text-red-500">*</span>
          </label>
          <input
            name="email"
            value={formData.email}
            onChange={handleChange}
            className="w-full border border-gray-300 rounded-lg px-3 py-2"
          />
          {errors.email && (
            <p className="text-red-600 text-sm mt-1">{errors.email}</p>
          )}
        </div>

        {/* Vendor Type */}
        <div>
          <label className="block text-gray-600 font-medium mb-1">Vendor Type</label>
          <select
            name="vendor_type"
            value={formData.vendor_type}
            onChange={handleChange}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 bg-white"
          >
            <option value="">Select Vendor Type</option>
            {[
              "Staffing Vendor","Recruitment Vendor","Software Vendor","Hardware Vendor",
              "Managed Service Provider (MSP)","Cloud Service Vendor","Consulting Vendor",
              "System Integrator (SI)","Outsourcing Vendor","Cybersecurity Vendor","OEM Vendor",
              "Value Added Reseller (VAR)","Technology Partner","Freelancer",
              "Training & Certification Vendor",
            ].map((type, index) => (
              <option key={index} value={type}>{type}</option>
            ))}
          </select>
        </div>

        {["vendor_mobile", "vendor_code", "gst_number", "website"].map((field, i) => (
          <div key={i}>
            <label className="block text-gray-600 font-medium mb-1">
              {field.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())}
            </label>
            <input
              name={field}
              value={formData[field]}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-lg px-3 py-2"
            />
          </div>
        ))}

        <div className="col-span-2 flex justify-center mt-4">
          <button
            type="submit"
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg shadow-md transition"
          >
            {isEdit ? "Update Vendor" : "Save Vendor"}
          </button>
        </div>

      </form>
    </div>
  );
};

export default VendorForm;
