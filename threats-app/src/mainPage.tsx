import React, { useState, useEffect } from 'react';
import './App.css'; // Подключаем стили
import { useNavigate } from 'react-router-dom';
import Breadcrumbs from './Breadcrumbs';
import Navbar from './Navbar';

// Мок-данные угроз
const mockThreats = [
  {
    pk: 1,
    threat_name: 'Угроза 1',
    short_description: 'Описание угрозы 1'
  },
  {
    pk: 2,
    threat_name: 'Угроза 2',
    short_description: 'Описание угрозы 2',
  },
  {
    pk: 3,
    threat_name: 'Угроза 3',
    short_description: 'Описание угрозы 3',
  },
];

const MainPage = () => {
  const [inputValue, setInputValue] = useState('');
  const [priceFrom, setPriceFrom] = useState('');
  const [priceTo, setPriceTo] = useState('');
  const [threats, setThreats] = useState(mockThreats);
  const [filteredThreats, setFilteredThreats] = useState(mockThreats);
  const [currentRequestId, setCurrentRequestId] = useState(null);
  const [currentCount, setCurrentCount] = useState(0);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchThreats = async () => {
      try {
        const response = await fetch('/api/threats/');
        const threatsData = await response.json();

        const filteredData = threatsData.filter(item => item.pk !== undefined);
        const requestData = threatsData.find(item => item.request);

        setThreats(filteredData);
        setFilteredThreats(filteredData);
        setCurrentRequestId(requestData?.request?.pk || null);
        setCurrentCount(requestData?.request?.threats_amount || 0);
      } catch (error) {
        console.error('Ошибка при загрузке данных угроз:', error);
        // Если произошла ошибка, используем мок-данные
        setThreats(mockThreats);
        setFilteredThreats(mockThreats);
        const requestData = mockThreats.find(item => item.request);
        setCurrentRequestId(requestData?.request?.pk || null);
        setCurrentCount(requestData?.request?.threats_amount || 0);
      }
    };

    fetchThreats();
  }, []);

  const handleSearchSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`/api/threats/?name=${inputValue}&price_from=${priceFrom}&price_to=${priceTo}`);
      const result = await response.json();

      const filteredResult = result.filter(item => item.pk !== undefined);
      setFilteredThreats(filteredResult);
    } catch (error) {
      console.error('Ошибка при выполнении поиска:', error);
    }
  };

  const handleAddThreat = async (threatId) => {
    try {
      const response = await fetch('/add_threat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ threat_id: threatId }),
      });
      if (response.ok) {
        alert('Угроза добавлена');
      } else {
        alert('Ошибка при добавлении угрозы');
      }
    } catch (error) {
      console.error('Ошибка при добавлении угрозы:', error);
    }
  };

  const defaultImageUrl = 'http://127.0.0.1:9000/static/network.jpg';

  return (
    <div>
      <header className="site-header">
        <a href="/" className="site-name">Мониторинг угроз</a>
        <Navbar />
      </header>
      <Breadcrumbs />
      <div className="site-body">
        <div className="search">
          <form onSubmit={handleSearchSubmit} className="search-form">
            <input
              type="text"
              name="threat_name"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              className="search-bar"
              placeholder="Имя угрозы"
            />
            <input
              type="number"
              name="price_from"
              value={priceFrom}
              onChange={(e) => setPriceFrom(e.target.value)}
              className="price-input"
              placeholder="Цена от"
            />
            <input
              type="number"
              name="price_to"
              value={priceTo}
              onChange={(e) => setPriceTo(e.target.value)}
              className="price-input"
              placeholder="Цена до"
            />
            <input type="submit" value="Поиск" className="search-button" />
          </form>
          <a href={`/requests/${currentRequestId}`} className="current-request">
            Текущая заявка ({currentCount})
          </a>
        </div>

        <div className="cards-list">
          {filteredThreats.map((threat) => (
            <div key={threat.pk} className="card">
              <a href={`/description/${threat.pk}`}>
                <div className="card__content card__content-request">
                  <h3 className="card__name">{threat.threat_name}</h3>
                  <div className="card_description">{threat.short_description}</div>
                </div>
                <img src={threat.img_url ? threat.img_url : defaultImageUrl} alt={threat.threat_name} className="card__image" />
              </a>
              <div className="buttons">
                <button
                  onClick={(e) => {
                    e.preventDefault(); // Предотвращаем переход по ссылке
                    handleAddThreat(threat.pk);
                  }}
                  className="add-button"
                >
                  Добавить
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default MainPage;
