// HomePage.js
import React from 'react';
import { useNavigate } from 'react-router-dom';
import './App.css'; // Подключаем стили
import Navbar from './Navbar';
import Breadcrumbs from './Breadcrumbs';

const HomePage = () => {
  const navigate = useNavigate();

  const handleNavigateToServices = () => {
    navigate('/main'); // Путь к основной странице с угрозами
  };

  return (
    <div>
    <header className="site-header">
        <a href="/" className="site-name">Мониторинг угроз</a>
        <Navbar /> {/* Добавляем Navbar */}

      </header>
      <Breadcrumbs />
    <div className="home-container">
      <div className="home-content">
        <h1 className="home-title">Добро пожаловать!</h1>
        <p className="home-description">Данный ресурс предназначен для мониторинга событий безопасности в компании.</p>
        <button className="services-button" onClick={handleNavigateToServices}>
          Список услуг
        </button>
      </div>
    </div>
    </div>
  );
};

export default HomePage;
