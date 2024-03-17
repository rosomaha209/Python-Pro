
function updateUserStatus() {
    fetch(`/messenger/api/chat/${chatId}/user_status/`)
    .then(response => response.json())
    .then(data => {
        data.forEach(userStatus => {
            const statusElement = document.getElementById(`status-user-${userStatus.user_id}`);
            if (statusElement) {
                statusElement.innerText = userStatus.is_online ? 'Online' : 'Offline';
                // Оновлення кольору залежно від статусу користувача
                statusElement.style.color = userStatus.is_online ? 'green' : 'red';
            }
        });
    })
    .catch(error => console.error('Error fetching user statuses:', error));
}

//  оновлення статусу кожні 60 секунд
setInterval(updateUserStatus, 600000);

// Викликати при завантаженні сторінки
updateUserStatus();
