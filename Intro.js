import React, { useState, useEffect } from 'react';
import './Intro.css'; // Định dạng CSS
import App from './App';

function Intro() {
  const text = [
    "Welcome to HEM (Health Endpoint Monitoring) !",
    "This is the website that helps monitor your system health",
    "Let's get started !",
  ];

  const [currentText, setCurrentText] = useState(""); // Văn bản hiện tại
  const [wordIndex, setWordIndex] = useState(0); // Câu hiện tại
  const [showContinueButton, setShowContinueButton] = useState(false); // Hiển thị nút
  const [index, setIndex] = useState(0); // Ký tự hiện tại
  const [showApp, setShowApp] = useState(false); // Trạng thái hiển thị App

  // Hiệu ứng gõ chữ
  useEffect(() => {
    if (index < text[wordIndex].length) {
      const timer = setTimeout(() => {
        setCurrentText((prev) => prev + text[wordIndex].charAt(index)); // Thêm ký tự
        setIndex(index + 1);
      }, 36);

      return () => clearTimeout(timer); // Xóa timer cũ khi unmount
    } else {
      // Khi hoàn thành một câu
      if (wordIndex < text.length - 1) {
        setTimeout(() => {
          setWordIndex(wordIndex + 1);
          setCurrentText(""); // Reset văn bản
          setIndex(0); // Reset chỉ số ký tự
        }, 500);
      } else {
        // Hiển thị nút sau khi gõ xong toàn bộ
        setTimeout(() => {
          setShowContinueButton(true);
        }, 500);
      }
    }
  }, [index, wordIndex]);

  // Chuyển sang App
  function startApp() {
    setShowApp(true); // Hiển thị App
  }

  // Nếu đã nhấn nút "Bắt đầu", hiển thị App và ẩn Intro
  if (showApp) {
    return <App />;
  }

  return (
    <><div className="card-intro">
        <img src='.\Health.png' className='Logo'></img>
        <div className="slogan">
            <p>Health Endpoint Monitoring</p>
        </div>
        <div className="typing-text">
            {currentText}
        </div>
          {showContinueButton && (
              <button id="continueButton" onClick={startApp}>Start
              </button>
          )}
      </div></>
  );
}

export default Intro;
