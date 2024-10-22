import React, { useState, useEffect } from 'react';

// Компонент для отображения отдельной карты угрозы
const ThreatCard = ({ threat, onAddThreat }) => {
  return (
    <div className="card">
      <div className="card__content card__content-request">
        <h3 className="card__name">{threat.threat_name}</h3>
        <div className="card_description">{threat.short_description}</div>
      </div>
      <img src={threat.img_url} alt={threat.threat_name} className="card__image" />

      <div className="buttons">
        <form onSubmit={(e) => { e.preventDefault(); onAddThreat(threat.id); }} className="add-form">
          <button type="submit" className="add-button">Добавить</button>
        </form>
      </div>
    </div>
  );
};

// Основной компонент приложения
const MainPage = () => {
  const [inputValue, setInputValue] = useState('');
  const [threats, setThreats] = useState([]);
  const [currentRequestId, setCurrentRequestId] = useState(null);
  const [currentCount, setCurrentCount] = useState(0);

  // Имитация загрузки данных угроз с сервера
  useEffect(() => {
    // Здесь должен быть запрос на сервер для получения данных
    const mockThreats = [
      { id: 1, threat_name: 'Угроза 1', short_description: 'Описание угрозы 1', img_url: 'http://127.0.0.1:9000/static/network.jpg' },
      { id: 2, threat_name: 'Угроза 2', short_description: 'Описание угрозы 2', img_url: 'http://127.0.0.1:9000/static/network.jpg' },
      { id: 3, threat_name: 'Угроза 2', short_description: 'Описание угрозы 2', img_url: 'http://127.0.0.1:9000/static/network.jpg' },
      { id: 4, threat_name: 'Угроза 2', short_description: 'Описание угрозы 2', img_url: 'http://127.0.0.1:9000/static/network.jpg' },
      { id: 5, threat_name: 'Угроза 2', short_description: 'Описание угрозы 2', img_url: 'http://127.0.0.1:9000/static/network.jpg' },
      { id: 6, threat_name: 'Угроза 2', short_description: 'Описание угрозы 2', img_url: 'http://127.0.0.1:9000/static/network.jpg' },
      // Добавьте больше данных по необходимости
    ];
    setThreats(mockThreats);
    setCurrentRequestId(123);  // Пример ID текущей заявки
    setCurrentCount(5);        // Пример текущего количества
  }, []);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    // Обработка поиска угроз
    console.log('Поиск угрозы:', inputValue);
  };

  const handleAddThreat = (threatId) => {
    console.log('Добавлена угроза с ID:', threatId);
    // Логика добавления угрозы
  };

  return (
    <div>
      <header className="site-header">
        <a href="/" className="site-name">Мониторинг угроз</a>
      </header>

      <div className="site-body">
        <div className="search">
          <form onSubmit={handleSearchSubmit} className="search-form">
            <input
              type="text"
              name="threat_name"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              className="search-bar"
            />
            <input type="submit" value="Поиск" className="search-button" />
          </form>
          <a href={`/current/${currentRequestId}`} className="current-request">
            Текущая заявка ({currentCount})
          </a>
        </div>

        <div className="cards-list">
          {threats.map((threat) => (
            <ThreatCard key={threat.id} threat={threat} onAddThreat={handleAddThreat} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default MainPage;
