import { getCookie } from "./getCookie.js";


const modal = document.getElementById("myModal");
const span = document.getElementsByClassName("close")[0];
const eqname = document.querySelector('.eqname');
const roomSelect = document.querySelector(".roomselect");
const movebutton = modal.querySelector("button");
let eq_id;


// Сделаем функцию глобальной
window.moveequipment = async function moveequipment(equipment_id){
    // отображаем наше окно
    modal.style.display = "flex";

    const resp = await fetch(`/api/equipment/${equipment_id}`, 
        {method: "GET"});
    const equipment = await resp.json();
    eqname.innerText = equipment.name; 
    
    // Установим значение кабинета для изменения
    eq_id = equipment_id;

    // Загрузка кабинетов
    const rooms = []
    const roomsresponse = await fetch('/api/rooms', {'method': 'GET'});
    rooms.value = await roomsresponse.json();

    // Очищаем select кабинета
    roomSelect.innerHTML = "";

    // Заполняем select кабинета
    rooms.value.forEach(room => {
        const option = document.createElement('option');
        option.value = room.id;
        option.textContent = room.name;
        roomSelect.appendChild(option);
        
    });
    roomSelect.value = equipment.room_id;
}


async function moveRequest(){
    const response = await fetch("/api/moveequipment", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            "room_id": roomSelect.value,
            "eq_id": eq_id
        })
    })

    if (response.ok){
        // Перезагружаем страницу
        window.location = window.location;
    }
}

span.addEventListener("click", () => {
    modal.style.display = "none";
})

// Закрытие при клике вне модального окна
window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
}

// Подключим функцию отправки данных о перемещении оборудования
movebutton.addEventListener("click", moveRequest);