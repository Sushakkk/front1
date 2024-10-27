import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import './App.css'; // Подключаем стили
import Navbar from './Navbar';
import Breadcrumbs from './Breadcrumbs';

// Мок-данные для угроз
const mockThreats = [
  {
    pk: 1,
    threat_name: 'Угроза 1',
    description: 'Подробное описание угрозы 1.',
    detections: 5,
    price: 1500
  },
  {
    pk: 2,
    threat_name: 'Угроза 2',
    description: 'Подробное описание угрозы 2.',
    detections: 3,
    price: 2000
  },
  {
    pk: 3,
    threat_name: 'Угроза 3',
    description: 'Подробное описание угрозы 3.',
    detections: 10,
    price: 1200
  },
];

const defaultImageUrl = 'http://127.0.0.1:9000/static/network.jpg';

const ThreatDescription = () => {
  const { threatId } = useParams();
  const [threat, setThreat] = useState(null);
  const [loading, setLoading] = useState(true); // Для отображения состояния загрузки
  const [error, setError] = useState(null); // Для обработки ошибок

  useEffect(() => {
    const fetchThreat = async () => {
      try {
        const response = await fetch(`/api/threats/detail/${threatId}/`);
        
        if (!response.ok) {
          throw new Error('Ошибка при загрузке данных');
        }

        const threatData = await response.json();
        setThreat(threatData);
      } catch (err) {
        // Если произошла ошибка, используем мок-данные
        const mockThreat = mockThreats.find(item => item.pk === parseInt(threatId, 10));
        
        if (mockThreat) {
          setThreat(mockThreat);
        } else {
          setError('Угроза не найдена');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchThreat();
  }, [threatId]);

  // Обработка состояния загрузки и ошибок
  if (loading) {
    return <div>Загрузка данных угрозы...</div>;
  }

  if (error) {
    return <div>Ошибка: {error}</div>;
  }

  // Если данные угрозы загружены
  return (
    <div>
      <header className="site-header">
        <a href="/" className="site-name">Мониторинг угроз</a>
        <Navbar /> {/* Добавляем Navbar */}
      </header>
      <Breadcrumbs />

      <main className="site-body">
        <div className="card_overview">
          <div className="card__content">
            <h3 className="card__name">{threat.threat_name}</h3>
            <div className="card_description">{threat.description}</div>

            <div className="card__statistics">
              <div className="card__statistics__header">Статистика</div>
              <div className="card__statistics__item">
                Количество обнаружений: {threat.detections}
              </div>
              <div className="card__statistics__item">
                Средняя цена мониторинга: {threat.price} ₽
              </div>
            </div>
          </div>
          <img src={threat.img_url ? threat.img_url : defaultImageUrl} alt={threat.threat_name} className="card__image__description" />
        </div>
      </main>
    </div>
  );
};

export default ThreatDescription;
