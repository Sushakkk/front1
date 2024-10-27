import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import './App.css'; // Подключаем стили

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
        setError(err.message);
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
      </header>

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
          <img src={threat.img_url} alt={threat.threat_name} className="card__image__description" />
        </div>
      </main>
    </div>
  );
};

export default ThreatDescription;
