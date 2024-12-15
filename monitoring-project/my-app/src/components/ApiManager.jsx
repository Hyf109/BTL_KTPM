import React, { useState, useEffect } from "react";
import axios from "axios";

function ApiManager() {
  const [apiUrls, setApiUrls] = useState([]);
  const [newApi, setNewApi] = useState({ name: "", url: "" });

  const fetchApiUrls = async () => {
    try {
      const response = await axios.get("http://health_monitor:8003/api-urls");
      setApiUrls(response.data);
    } catch (err) {
      console.error("Failed to fetch API URLs:", err.message);
    }
  };

  useEffect(() => {
    fetchApiUrls();
  }, []);

  const addApi = async () => {
    try {
      await axios.post("http://health_monitor:8003/api-urls", newApi);
      setApiUrls([...apiUrls, newApi]);
      setNewApi({ name: "", url: "" });
    } catch (error) {
      console.error("Error adding API:", error.message);
    }
  };

  const deleteApi = async (name) => {
    try {
      await axios.delete(`http://health_monitor:8003/api-urls/${name}`);
      setApiUrls(apiUrls.filter((api) => api.name !== name));
    } catch (error) {
      console.error("Error deleting API:", error.message);
    }
  };

  return (
    <div>
      <h2>API Manager</h2>
      <ul>
        {apiUrls.map((api) => (
          <li key={api.name}>
            {api.name} - {api.url}{" "}
            <button onClick={() => deleteApi(api.name)}>Delete</button>
          </li>
        ))}
      </ul>
      <h3>Add New API</h3>
      <input
        type="text"
        placeholder="Name"
        value={newApi.name}
        onChange={(e) => setNewApi({ ...newApi, name: e.target.value })}
      />
      <input
        type="text"
        placeholder="URL"
        value={newApi.url}
        onChange={(e) => setNewApi({ ...newApi, url: e.target.value })}
      />
      <button onClick={addApi}>Add API</button>
    </div>
  );
}

export default ApiManager;
