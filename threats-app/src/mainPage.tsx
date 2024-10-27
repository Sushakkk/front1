import React, { useState, useEffect } from 'react';
import './App.css'; // Подключаем стили
import { useNavigate } from 'react-router-dom';

// Мок-данные угроз
const mockThreats = [
  // Здесь могут быть ваши мок-данные
];

const MainPage = () => {
  const [inputValue, setInputValue] = useState('');
  const [threats, setThreats] = useState(mockThreats); // Используем мок-данные
  const [filteredThreats, setFilteredThreats] = useState(mockThreats); // Угрозы для отображения
  const [currentRequestId, setCurrentRequestId] = useState(null);
  const [currentCount, setCurrentCount] = useState(0);
  const navigate = useNavigate();

  // Имитация загрузки данных угроз с сервера
  useEffect(() => {
    const fetchThreats = async () => {
      try {
        const response = await fetch('/api/threats/');
        const threatsData = await response.json();

        // Фильтруем угрозы и отбрасываем поле request
        const filteredData = threatsData.filter(item => item.pk !== undefined);
        const requestData = threatsData.find(item => item.request); // Находим объект с полем request

        setThreats(filteredData);
        setFilteredThreats(filteredData); // Изначально отображаем все угрозы
        setCurrentRequestId(requestData?.request?.pk || null); // Получаем ID текущей заявки
        setCurrentCount(requestData?.request?.threats_amount || 0); // Получаем количество угроз
      } catch (error) {
        console.error('Ошибка при загрузке данных угроз:', error);
      }
    };

    fetchThreats();
  }, []);

  const handleSearchSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`/api/threats/?name=${inputValue}`);
      const result = await response.json();

      // Фильтруем только угрозы
      const filteredResult = result.filter(item => item.pk !== undefined);
      
      setFilteredThreats(filteredResult); // Устанавливаем отфильтрованные угрозы
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
          <a href={`/requests/${currentRequestId}`} className="current-request">
            Текущая заявка ({currentCount})
          </a>
        </div>

        <div className="cards-list">
          {filteredThreats.map((threat) => (
            <a href={`/description/${threat.pk}`} key={threat.pk}>
              <div className="card">
                <div className="card__content card__content-request">
                  <h3 className="card__name">{threat.threat_name}</h3>
                  <div className="card_description">{threat.short_description}</div>
                </div>
                <img src={threat.img_url ? threat.img_url : defaultImageUrl} alt={threat.threat_name} className="card__image" />
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
            </a>
          ))}
        </div>
      </div>
    </div>
  );
};

export default MainPage;
