import React, { useEffect, useState } from "react";
import axios from "axios";
import VendorForm from "./VendorForm";
import { MdDeleteOutline } from "react-icons/md";
import { CiEdit } from "react-icons/ci";

function ViewVendors() {
  const [vendors, setVendors] = useState([]);
  const [openModal, setOpenModal] = useState(false);
  const [editVendor, setEditVendor] = useState(null);
  const [toggleState, setToggleState] = useState({});

  const getVendors = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/vendors/");
      setVendors(res.data);

      const initialState = {};
      res.data.forEach((v) => (initialState[v.id] = v.status === "active"));
      setToggleState(initialState);
    } catch (err) {
      console.error("Error fetching vendors", err);
    }
  };

  useEffect(() => {
    getVendors();
  }, []);

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this vendor?")) return;

    try {
      await axios.delete(`http://127.0.0.1:8000/vendors/${id}`);
      alert("Vendor Deleted Successfully");
      getVendors();
    } catch (err) {
      alert("Error deleting vendor");
      console.error(err);
    }
  };

  const handleEdit = (vendor) => {
    setEditVendor(vendor);
    setOpenModal(true);
  };

  const truncateWebsite = (url) => {
    if (!url) return ""; // FIX: no dash here
    let clean = url.replace(/^https?:\/\//, "");
    return clean.length > 12 ? clean.slice(0, 12) + "..." : clean;
  };

  const handleToggle = async (id, currentStatus) => {
    const newStatus = currentStatus ? "inactive" : "active";

    const confirmText = currentStatus
      ? "Are you sure you want to INACTIVATE this vendor?"
      : "Are you sure you want to ACTIVELY enable this vendor?";

    if (!window.confirm(confirmText)) return;

    try {
      await axios.patch(
        `http://127.0.0.1:8000/vendors/${id}/status?status=${newStatus}`
      );
      setToggleState((prev) => ({
        ...prev,
        [id]: !prev[id],
      }));
    } catch (err) {
      alert("Failed to update status");
      console.error(err);
    }
  };

  return (
    <>
      <div className="bg-white shadow-lg border border-gray-200 rounded-xl p-6 max-w-7xl mx-auto mt-10 relative">

        <button
          onClick={() => {
            setEditVendor(null);
            setOpenModal(true);
          }}
          className="absolute right-6 top-6 bg-blue-600 hover:bg-blue-700 text-white text-sm px-5 py-2 rounded-lg shadow-md transition-all"
        >
          + Add Vendor
        </button>

        <h2 className="text-3xl font-bold text-center mb-6 text-gray-800">
          Vendor Management
        </h2>

        <div className="overflow-x-auto mt-4">
          <table className="w-full border border-gray-300 rounded-lg overflow-hidden text-sm">
            <thead className="border border-gray-300">
              <tr className="bg-gray-100 text-gray-700">
                <th className="border border-gray-300 p-2">Sr</th>
                <th className="border border-gray-300 p-2">Vendor Name</th>
                <th className="border border-gray-300 p-2">Company</th>
                <th className="border border-gray-300 p-2">Email</th>
                <th className="border border-gray-300 p-2">Mobile</th>
                <th className="border border-gray-300 p-2">Type</th>
                <th className="border border-gray-300 p-2">Code</th>
                <th className="border border-gray-300 p-2">GST</th>
                <th className="border border-gray-300 p-2">Website</th>
                <th className="border border-gray-300 p-2">Status</th>
                <th className="border border-gray-300 p-2">Action</th>
              </tr>
            </thead>

            <tbody>
              {vendors.length > 0 ? (
                vendors.map((v, i) => (
                  <tr key={v.id} className="hover:bg-gray-50 transition-all">
                    
                    <td className="border border-gray-300 p-2 text-center">{i + 1}</td>
                    <td className="border border-gray-300 p-2 text-center">{v.vendor_name || "—"}</td>
                    <td className="border border-gray-300 p-2 text-center">{v.company_name || "—"}</td>
                    <td className="border border-gray-300 p-2 text-center break-all">{v.email || "—"}</td>
                    <td className="border border-gray-300 p-2 text-center">{v.vendor_mobile || "—"}</td>
                    <td className="border border-gray-300 p-2 text-center">{v.vendor_type || "—"}</td>
                    <td className="border border-gray-300 p-2 text-center font-semibold">{v.vendor_code || "—"}</td>
                    <td className="border border-gray-300 p-2 text-center">{v.gst_number || "—"}</td>

                    <td className="border border-gray-300 p-2 text-center">
                      {v.website ? (
                        <a
                          href={v.website.startsWith("http") ? v.website : "https://" + v.website}
                          target="_blank"
                          rel="noreferrer"
                          className="text-blue-600 underline"
                        >
                          {truncateWebsite(v.website)}
                        </a>
                      ) : (
                        "—"
                      )}
                    </td>

                    <td className="border border-gray-300 p-2 text-center">
                      <label className="inline-flex items-center cursor-pointer relative">
                        <input
                          type="checkbox"
                          className="sr-only peer"
                          checked={toggleState[v.id] || false}
                          onChange={() => handleToggle(v.id, toggleState[v.id] || false)}
                        />
                        <div className="w-11 h-6 bg-gray-300 rounded-full peer-checked:bg-green-500 transition-colors relative">
                          <div className="absolute top-[2px] left-[2px] w-5 h-5 bg-white rounded-full shadow transition-all duration-300 peer-checked:translate-x-5"></div>
                        </div>
                      </label>
                    </td>

                    <td className="border border-gray-300 p-2">
                      <div className="flex gap-4 justify-center items-center">
                        <MdDeleteOutline
                          className="text-red-500 text-xl cursor-pointer hover:scale-110 transition"
                          onClick={() => handleDelete(v.id)}
                        />
                        <CiEdit
                          className="text-blue-600 text-xl cursor-pointer hover:scale-110 transition"
                          onClick={() => handleEdit(v)}
                        />
                      </div>
                    </td>

                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="11" className="text-center py-4 text-gray-500">
                    No vendors found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {openModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
          <div className="bg-white rounded-xl shadow-lg p-6 w-full max-w-3xl relative">

            <button
              onClick={() => setOpenModal(false)}
              className="absolute top-4 right-4 text-gray-500 text-xl hover:text-gray-700 transition"
            >
              ✖
            </button>

            <VendorForm
              initialData={editVendor}
              onSave={() => {
                setOpenModal(false);
                getVendors();
              }}
            />

          </div>
        </div>
      )}
    </>
  );
}

export default ViewVendors;
