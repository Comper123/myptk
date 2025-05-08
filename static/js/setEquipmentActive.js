import { getCookie } from "./getCookie.js";


const modalActive = document.getElementById("modalActive");
const span = modalActive.getElementsByClassName("close")[0];
const eqname = modalActive.querySelector('.eqname');
const setactivebutton = modalActive.querySelector("button");
let eq_id;


// Сделаем функцию глобальной
window.setEquipmentActive = async function setEquipmentActive(equipment_id){
    // отображаем наше окно
    modalActive.style.display = "flex";

    const resp = await fetch(`/api/equipment/${equipment_id}`, 
        {method: "GET"});
    const equipment = await resp.json();
    eqname.innerText = equipment.name; 
    
    // Установим значение кабинета для изменения
    eq_id = equipment_id;
}


async function setActiveRequest(){
    const response = await fetch("/api/discardequipment", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            "eq_id": eq_id
        })
    })

    if (response.ok){
        // Перезагружаем страницу
        window.location = window.location;
    }
}

span.addEventListener("click", () => {
    modalActive.style.display = "none";
})

// Закрытие при клике вне модального окна
window.onclick = function(event) {
    if (event.target == modalActive) {
        modalActive.style.display = "none";
    }
}

// Подключим функцию отправки данных о перемещении оборудования
setactivebutton.addEventListener("click", setActiveRequest);