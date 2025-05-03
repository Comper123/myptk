document.addEventListener('DOMContentLoaded', function() {
    // Ждем загрузку DOM

    const confirmButtons = document.querySelectorAll('.confirm-user-button');

    confirmButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();  //  Отменяем стандартное поведение

            const userId = this.dataset.url.split('/').slice(-2, -1)[0];  // Получаем ID пользователя из URL (изменено)
            const button = this; // Сохраняем ссылку на кнопку, чтобы потом обновить текст

            // Отправляем AJAX-запрос
            fetch(this.dataset.url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // Получаем CSRF-токен
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert(data.message);  //  Отображаем сообщение об успехе
                    button.textContent = "Подтверждено"; //  Изменяем текст кнопки
                    button.disabled = true; //  Отключаем кнопку
                    // Дополнительно:  Можно обновить страницу или обновить другие элементы (например, отображать "активный")
                } else {
                    alert('Ошибка: ' + data.message);  // Отображаем сообщение об ошибке
                }
            })
            .catch(error => {
                alert('Произошла ошибка при отправке запроса.' + error);
                console.error('Ошибка:', error);
            });
        });
    });

    // Функция для получения CSRF-токена (общая)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});