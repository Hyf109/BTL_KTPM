import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import './Style.css'; 

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

function App() {
  const [healthData, setHealthData] = useState(null);
  const [networkData, setNetworkData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  const [downloadSpeeds, setDownloadSpeeds] = useState([]);
  const [uploadSpeeds, setUploadSpeeds] = useState([]);
  const [timestamps, setTimestamps] = useState([]);

  const [cpuUsages, setCpuUsages] = useState([]);
  const [memoryUsages, setMemoryUsages] = useState([]);
  
  const [activeSection, setActiveSection] = useState('health'); // Active section state

  // Fetch health and network data
  const fetchData = async () => {
    setLoading(true);
    try {
      const healthResponse = await axios.get('http://localhost:8003/health');
      setHealthData(healthResponse.data);

      const networkResponse = await axios.get('http://localhost:8003/network');
      setNetworkData(networkResponse.data);

      const currentTime = new Date().toLocaleTimeString();
      setDownloadSpeeds((prev) => [...prev, networkResponse.data.bytes_sent]);
      setUploadSpeeds((prev) => [...prev, networkResponse.data.bytes_recv]);
      setTimestamps((prev) => [...prev, currentTime]);

      const cpuUsageValue = parseFloat(healthResponse.data.system.cpu_usage.replace('%', ''));
      const memoryUsageValue = parseFloat(healthResponse.data.system.memory_usage.replace('%', ''));
      setCpuUsages((prev) => [...prev, cpuUsageValue]);
      setMemoryUsages((prev) => [...prev, memoryUsageValue]);

      setError(null);
    } catch (err) {
      console.error('Failed to fetch data:', err.message);
      setError('Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000); // Poll every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const renderAPIStatus = () => {
    return healthData.apis.map((api) => (
      <div key={api.api_name} className="card">
        <h2>API: {api.api_name}</h2>
        <p>Status: {api.api_status}</p>
        <p>Docker: {api.docker_status}</p>
      </div>
    ));
  };

  const networkDataChart = {
    labels: timestamps,
    datasets: [
      {
        label: 'Download Speed (Mbps)',
        data: downloadSpeeds,
        fill: false,
        borderColor: 'rgba(75,192,192,1)',
        tension: 0.1,
      },
      {
        label: 'Upload Speed (Mbps)',
        data: uploadSpeeds,
        fill: false,
        borderColor: 'rgba(153,102,255,1)',
        tension: 0.1,
      },
    ],
  };

  const networkLineChartOptions = {
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          autoSkip: true,
        },
      },
    },
  };

  const cpuLineChart = {
    labels: timestamps,
    datasets: [
      {
        label: 'CPU Usage (%)',
        data: cpuUsages,
        fill: false,
        borderColor: 'rgba(255,99,132,1)',
        tension: 0.1,
      },
    ],
  };

  const memoryLineChart = {
    labels: timestamps,
    datasets: [
      {
        label: 'Memory Usage (%)',
        data: memoryUsages,
        fill: false,
        borderColor: 'rgba(54,162,235,1)',
        tension: 0.1,
      },
    ],
  };

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <>
      <div className="header">
        <img src="/Health.png" className="logo" alt="Logo" />
        <h1>Health Endpoint Monitoring</h1>
      </div>
      
      <div className="main">
        <div className="menu">
          <button onClick={() => setActiveSection('health')}>Health Overview</button>
          <button onClick={() => setActiveSection('network')}>Network Data</button>
          <button onClick={() => setActiveSection('cpu')}>CPU Usage</button>
          <button onClick={() => setActiveSection('memory')}>Memory Usage</button>
        </div>

        <div className="container">
          {activeSection === 'health' && healthData && (
            <div className="left-column">
              {renderAPIStatus()}
              <div className="card">
                <h2>System</h2>
                <p>CPU Usage: {healthData.system.cpu_usage}</p>
                <p>Memory Usage: {healthData.system.memory_usage}</p>
              </div>
              <div className="card">
                <h2>Overall Status</h2>
                <p>{healthData.status}</p>
                <p>Uptime: {healthData.uptime}</p>
              </div>
            </div>
          )}

          {activeSection === 'network' && networkData && (
            <div className="chart">
              <h2 className="chart-title">Network Traffic:</h2>
              <Line data={networkDataChart} options={networkLineChartOptions} />
            </div>
          )}

          {activeSection === 'cpu' && (
            <div className="chart">
              <h2 className="chart-title">CPU Usage:</h2>
              <Line data={cpuLineChart} />
            </div>
          )}

          {activeSection === 'memory' && (
            <div className="chart">
              <h2 className="chart-title">Memory Usage:</h2>
              <Line data={memoryLineChart} />
            </div>
          )}
        </div>
      </div>
    </>
  );
}

export default App;
