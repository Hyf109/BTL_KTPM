import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [price, setPrice] = useState(null);
  const [status, setStatus] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Gọi API Prometheus để lấy giá Bitcoin
        const priceResponse = await axios.get('http://localhost:9090/api/v1/query', {
          params: { query: 'bitcoin_price_usd' }
        });
        setPrice(priceResponse.data.data.result[0].value[1]);

        // Gọi API Prometheus để lấy trạng thái của CoinGecko API
        const statusResponse = await axios.get('http://localhost:9090/api/v1/query', {
          params: { query: 'coingecko_api_up' }
        });
        setStatus(statusResponse.data.data.result[0].value[1] === "1" ? "Up" : "Down");

      } catch (error) {
        console.error("Error fetching data from Prometheus:", error);
      }
    };

    // Gọi API mỗi 30 giây để cập nhật dữ liệu
    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval); // Clear interval khi component bị huỷ

  }, []);

  return (
    <div style={{ textAlign: 'center', padding: '50px' }}>
      <h1>Bitcoin Price Monitor</h1>
      <p><strong>Bitcoin Price (USD):</strong> {price !== null ? `$${price}` : "Loading..."}</p>
      <p><strong>CoinGecko API Status:</strong> {status || "Loading..."}</p>
    </div>
  );
}

export default App;
