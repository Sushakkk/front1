import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import './App.css';

const RequestPage = () => {
  const { reqId } = useParams();
  const [currentThreats, setCurrentThreats] = useState([]);

  useEffect(() => {
    // Моковые данные угроз для текущей заявки
    const mockThreats = [
      {
        threat_name: 'Защита сети',
        company_name: 'Компания A',
        price: 1000,
        comment: 'Ежемесячный мониторинг',
        img_url: 'http://127.0.0.1:9000/static/network.jpg'
      },
      {
        threat_name: 'Антивирус',
        company_name: 'Компания B',
        price: 1500,
        comment: 'Раз в полгода',
        img_url: 'http://127.0.0.1:9000/static/network.jpg'
      },
      {
        threat_name: 'Веб-защита',
        company_name: 'Компания C',
        price: 1200,
        comment: 'Защита веб-приложений',
        img_url: 'http://127.0.0.1:9000/static/network.jpg'
      }
    ];

    // Устанавливаем данные угроз
    setCurrentThreats(mockThreats);
  }, [reqId]);

  const handleDelete = async () => {
    try {
      const response = await fetch('/del_request', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // 'X-CSRFToken': getCsrfToken() // добавьте CSRF токен, если используете Django
        },
        body: JSON.stringify({ request_id: reqId })
      });
      if (response.ok) {
        alert('Запрос успешно удален');
        setCurrentThreats([]); // Очищаем угрозы после удаления
      } else {
        alert('Ошибка при удалении запроса');
      }
    } catch (error) {
      console.error('Ошибка:', error);
    }
  };

  const getCsrfToken = () => {
    // Функция для получения CSRF токена (если необходимо)
    return document.cookie.split('; ')
      .find(row => row.startsWith('csrftoken'))
      ?.split('=')[1];
  };

  return (
    <div>
      <header className="site-header">
        <a href="/">
          <div className="site-name">Мониторинг угроз</div>
        </a>
      </header>

      <div className="request-buttons">
        <button onClick={handleDelete} className="del-button">
          Удалить
        </button>
      </div>

      <main className="site-body">
        <div className="cards-list-request">
          {currentThreats && currentThreats.length > 0 ? (
            currentThreats.map((threat, index) => (
              <div key={index} className="card card-request">
                <div className="card__content">
                  <table className="request-table">
                    <thead>
                      <tr>
                        <th>Услуга</th>
                        <th>Компания</th>
                        <th>Стоимость мониторинга</th>
                        <th>Комментарий</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>{threat.threat_name}</td>
                        <td>{threat.company_name}</td>
                        <td>{threat.price} ₽</td>
                        <td>{threat.comment}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <img src={threat.img_url} alt={threat.threat_name} className="card__image card__image-request" />
              </div>
            ))
          ) : (
            <p>Корзина пуста</p>
          )}
        </div>
      </main>
    </div>
  );
};

export default RequestPage;
