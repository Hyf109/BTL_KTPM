import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import './Style.css'; // Import file CSS

// Đăng ký các phần mở rộng của Chart.js
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

function App() {
  const [healthData, setHealthData] = useState(null);
  const [error, setError] = useState(null);
  const [networkData, setNetworkData] = useState(null);
  const [loading, setLoading] = useState(true);

  const [downloadSpeeds, setDownloadSpeeds] = useState([]);
  const [uploadSpeeds, setUploadSpeeds] = useState([]);
  const [timestamps, setTimestamps] = useState([]);
  
  const [cpuUsages, setCpuUsages] = useState([]);
  const [memoryUsages, setMemoryUsages] = useState([]);

  // Hàm fetch dữ liệu API
  const fetchHealthData = async () => {
    setLoading(true); 

    try {
      const response = await axios.get('http://localhost:8003/health');
      setHealthData(response.data);

      const networkResponse = await axios.get('http://localhost:8003/network');
      setNetworkData(networkResponse.data);

      const currentTime = new Date().toLocaleTimeString();
      setDownloadSpeeds((prev) => [...prev, networkResponse.data.bytes_sent]);
      setUploadSpeeds((prev) => [...prev, networkResponse.data.bytes_recv]);
      setTimestamps((prev) => [...prev, currentTime]);

      const cpuUsageValue = parseFloat(response.data.system.cpu_usage.replace('%', ''));
      const memoryUsageValue = parseFloat(response.data.system.memory_usage.replace('%', ''));
      setTimestamps((prev) => [...prev, currentTime]);
      setCpuUsages((prev) => [...prev, cpuUsageValue]);
      setMemoryUsages((prev) => [...prev, memoryUsageValue]);

      setError(null);
    } catch (err) {
      console.error('Failed to fetch health data:', err.message);
      setError('Failed to fetch health data');
    } finally {
      setLoading(false); 
    }
  };

  useEffect(() => {
    fetchHealthData(); 

    const interval = setInterval(() => {
      fetchHealthData(); 
    }, 30000); 

    return () => clearInterval(interval);
  }, []); 

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
        beginAtZero: true, // Không bắt đầu từ 0
        min: 1,            // Giá trị nhỏ nhất
        max: 2.5,            // Giá trị lớn nhất
        ticks: {
          stepSize: 0.15,    // Khoảng cách giữa các giá trị trên trục tung
          callback: (value) => `${value}Mbps`, // Thêm ký hiệu % vào các giá trị trục tung
        },
        title: {
          display: true,
          text: 'Mbps', // Nhãn trục tung
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
        borderColor: 'rgba(255,99,132,1)', // Màu đỏ
        tension: 0.1,
      },
    ],
  };
  
  const cpuLineChartOptions = {
    scales: {
      y: {
        beginAtZero: false, // Bắt đầu từ 0
        min: 0,           // Giá trị nhỏ nhất
        max: 2,           // Giá trị lớn nhất
        ticks: {
          stepSize: 0.2,  // Khoảng cách giữa các giá trị trên trục tung
          callback: (value) => `${value}%`, // Thêm ký hiệu % vào các giá trị trục tung
        },
        title: {
          display: true,
          text: 'CPU Usage (%)', // Nhãn cho trục tung
        },
      },
    },
  };

  const memoryLineChartData = {
    labels: timestamps,
    datasets: [
      {
        label: 'Memory Usage',
        data: memoryUsages,
        fill: false,
        borderColor: 'rgba(54,162,235,1)', // Màu xanh lam
        tension: 0.1,
      },
    ],
  };
  
  const memoryLineChartOptions = {
    scales: {
      y: {
        beginAtZero: false, // Không bắt đầu từ 0
        min: 11,            // Giá trị nhỏ nhất
        max: 13,            // Giá trị lớn nhất
        ticks: {
          stepSize: 0.2,    // Khoảng cách giữa các giá trị trên trục tung
          callback: (value) => `${value}%`, // Thêm ký hiệu % vào các giá trị trục tung
        },
        title: {
          display: true,
          text: 'Memory Usage (%)', // Nhãn trục tung
        },
      },
    },
  };
  
  
  
  

  if (loading) {
    return <div>Loading health data...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <>
      <div className="header">
        <img src="/Health.png" className="logo" alt="Logo" />
        <h1>Health Endpoint Monitoring</h1>
      </div>
      <div className="container">
        {healthData ? (
          <>
            <div className="left-column">
              <div className="card">
                <h2>API Exchange</h2>
                <p>Status: {healthData.exchange_api}</p>
                <p>Docker: {healthData.exchange_docker}</p>
              </div>
              <div className="card">
                <h2>API Gold</h2>
                <p>Status: {healthData.gold_api}</p>
                <p>Docker: {healthData.gold_docker}</p>
              </div>
              <div className="card">
                <h2>System</h2>
                <p>CPU Usage: {healthData.system.cpu_usage}</p>
                <p>Memory Usage: {healthData.system.memory_usage}</p>
              </div>
              <div className="card">
                <h2>Network Status</h2>
                <p>Download Speed: {networkData?.bytes_sent} Mbps</p>
                <p>Upload Speed: {networkData?.bytes_recv} Mbps</p>
              </div>
              <div className="card">
                <h2>Overall Status</h2>
                <p>{healthData.status}</p>
                <p>Uptime: {healthData.uptime}</p>
              </div>
            </div>
            <div className="right-column">
              <div className="chart">
                <h2 className="chart-title">Network Traffic:</h2>
                <div className="chart-container">
                  <Line data={networkDataChart} options={networkLineChartOptions} />
                </div>
              </div>

              {/* Biểu đồ CPU */}
              <div className="chart">
                  <h2 className="chart-title">CPU Usage:</h2>
                  <div className="chart-container">
                    <Line 
                      data={cpuLineChart} options={cpuLineChartOptions}
                    />
                  </div>
                </div>

                {/* Biểu đồ Memory */}
                <div className="chart">
                  <h2 className="chart-title">Memory Usage:</h2>
                  <div className="chart-container">
                  <Line data={memoryLineChartData} options={memoryLineChartOptions} />
                  </div>
                </div>
            </div>
          </>
        ) : (
          <p>Loading data...</p>
        )}
      </div>
    </>
  );
}

export default App;
