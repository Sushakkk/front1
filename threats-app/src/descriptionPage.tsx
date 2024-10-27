import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import './App.css'; // Подключаем стили

const ThreatDescription = () => {
  const { threatId } = useParams();
  const [threat, setThreat] = useState(null);

  useEffect(() => {
    // Моковые данные угроз
    const mockThreats = {
      '1': {
        name: 'Пример угрозы 1',
        description: 'Описание угрозы 1',
        count: 10,
        price: '1200 ₽',
        img_url: 'http://127.0.0.1:9000/static/network.jpg'
      },
      '2': {
        name: 'Пример угрозы 2',
        description: 'Описание угрозы 2',
        count: 15,
        price: '1500 ₽',
        img_url: 'http://127.0.0.1:9000/static/network.jpg'
      },
      '3': {
        name: 'Пример угрозы 3',
        description: 'Описание угрозы 3',
        count: 5,
        price: '1800 ₽',
        img_url: 'http://127.0.0.1:9000/static/network.jpg'
      }
    };

    // Получаем данные для переданного threatId
    setThreat(mockThreats[threatId]);
  }, [threatId]);

  // Если данные угрозы не загружены, показываем сообщение
  if (!threat) {
    return <div>Загрузка данных угрозы...</div>;
  }

  return (
    <div>
      <header className="site-header">
        <a href="/" className="site-name">Мониторинг угроз</a>
      </header>

      <main className="site-body">
        <div className="card_overview">
          <div className="card__content">
            <h3 className="card__name">{threat.name}</h3>
            <div className="card_description">{threat.description}</div>

            <div className="card__statistics">
              <div className="card__statistics__header">Статистика</div>
              <div className="card__statistics__item">
                Количество обнаружений за последний год: {threat.count}
              </div>
              <div className="card__statistics__item">
                Средняя цена мониторинга (месяц): {threat.price}
              </div>
            </div>
          </div>
          <img src={threat.img_url} alt={threat.name} className="card__image__description" />
        </div>
      </main>
    </div>
  );
};

export default ThreatDescription;
