import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import './App.css';

const RequestPage = () => {
  const { reqId } = useParams();
  const [currentThreats, setCurrentThreats] = useState([]);
  const [loading, setLoading] = useState(true); // Для состояния загрузки
  const [error, setError] = useState(null); // Для обработки ошибок

  useEffect(() => {
    const fetchRequestData = async () => {
      if (!reqId) {
        setLoading(false); // Если reqId не установлен, выходим из функции
        return;
      }

      try {
        const response = await fetch(`/api/requests/${reqId}/`);
        if (!response.ok) {
          throw new Error('Ошибка загрузки данных! Заявка не активна или необходимо авторизоваться!')
        }
        const requestData = await response.json();
        setCurrentThreats(requestData.threats); // Устанавливаем угрозы из ответа
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchRequestData();
  }, [reqId]);

  const handleDelete = async () => {
    if (!reqId) return; // Если reqId не установлен, ничего не делаем

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
    return document.cookie.split('; ')
      .find(row => row.startsWith('csrftoken'))
      ?.split('=')[1];
  };

  // Обработка состояния загрузки и ошибок
  if (loading) {
    return <div>Загрузка данных заявки...</div>;
  }

  if (error) {
    return <div>Ошибка: {error}</div>;
  }

  // Если reqId не установлен, ничего не выводим
  if (!reqId) {
    return null;
  }

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
          {currentThreats.length > 0 ? (
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
                        <td>{threat.company_name || 'Не указана'}</td>
                        <td>{threat.price} ₽</td>
                        <td>{threat.short_description || 'Нет комментариев'}</td>
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
