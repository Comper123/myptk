const server = "http://127.0.0.1:8888/";


document.addEventListener("DOMContentLoaded", async function (){
    // Получаем необходимые элементы
    const form = document.getElementById('equipmentForm');
    const typeSelect = document.getElementById('equipmentType');
    const dynamicFieldsContainer = document.getElementById('dynamicFieldsContainer');
    const basefieldsblock = document.querySelector(".basefields");
    const baseinputs = basefieldsblock.querySelectorAll('input');

    // Добавим отображения label для начальных инпутов input  
    baseinputs.forEach(input => {
        input.addEventListener("blur", function() {
            if (this.value.trim() === "") {
              this.classList.remove("empty-on-blur");
            }
        });
        input.addEventListener("focus", function() {
            this.classList.add("empty-on-blur");
        });
    })
    
    // Загрузка типов оборудования
    let equipmentTypes = [];
    const response = await fetch(server + 'api/equipmenttypes', {'method': "GET"})
    equipmentTypes = await response.json();

    // Заполняем селект типов
    equipmentTypes.forEach(type => {
        const option = document.createElement('option');
        option.value = type.id;
        option.textContent = type.name;
        typeSelect.appendChild(option);
    });

    // Обработчик изменения типа
    typeSelect.addEventListener("change", async function (){
        const typeId = this.value;
        dynamicFieldsContainer.innerHTML = "";

        // Ищем выбранный тип
        const selectedType = equipmentTypes.find(t => t.id == typeId);
        if (!selectedType) return;

        // Загружаем схему характеристик
        const schema = selectedType.attributes_schema;

        // Генерируем поля формы
        for (var [fieldName, fieldConfig] of Object.entries(schema)){
            const fieldGroup = document.createElement('div');
            
            // Создадим сам инпут
            let input;
            switch (fieldConfig.type) {
                case 'select':
                    input = document.createElement('select');
                    if (fieldConfig.options) {
                        if (!fieldConfig.required) {
                            const emptyOption = document.createElement('option');
                            emptyOption.value = '';
                            emptyOption.textContent = "Не указано";
                            input.appendChild(emptyOption);
                        }
                        fieldConfig.options.forEach(opt => {
                            const option = document.createElement('option');
                            option.innerText = opt;
                            option.value = opt;
                            input.appendChild(option);
                        });
                    }
                    fieldGroup.className = "input_block";
                    break;

                case 'number':
                    input = document.createElement('input');
                    input.type = 'number';
                    if (fieldConfig.min || fieldConfig.min == 0) input.min = fieldConfig.min;
                    if (fieldConfig.max || fieldConfig.min == 0) input.max = fieldConfig.max;
                    if (fieldConfig.step) input.step = fieldConfig.step;
                    fieldGroup.className = "input_block";
                    break;
                
                case 'checkbox':
                    // Создаем основной контейнер
                    const checkboxContainer = document.createElement('div');
                    checkboxContainer.className = 'checkbox-container';
                    
                    // Создаем label с текстом (если есть)
                    if (fieldConfig.label) {
                        const textLabel = document.createElement('label');
                        textLabel.className = 'checkbox-text-label';
                        textLabel.textContent = fieldConfig.label;
                        if (fieldConfig.required) {
                            textLabel.innerHTML += ' <span class="text-danger">*</span>';
                        }
                        checkboxContainer.appendChild(textLabel);
                    }
                    
                    // Создаем toggle
                    const toggleLabel = document.createElement('label');
                    toggleLabel.className = 'toggle';
                    
                    input = document.createElement('input');
                    input.type = 'checkbox';
                    input.id = `attr_${fieldName}`;
                    input.name = fieldName;
                    input.className = 'empty-on-blur';
                    
                    const toggleSpan = document.createElement('span');
                    
                    toggleLabel.appendChild(input);
                    toggleLabel.appendChild(toggleSpan);
                    
                    checkboxContainer.appendChild(toggleLabel);
                    fieldGroup.appendChild(checkboxContainer);
                    dynamicFieldsContainer.appendChild(fieldGroup);
                    break;

                case 'list':
                    // Реализация динамических списков
                    createListField(fieldName, fieldConfig);
                    break;

                // !! Переписать немного под стили адаптировать
                case 'checklist':
                    const checklistContainer = document.createElement('div');
                    checklistContainer.className = 'checklist-container mb-3';
                    checklistContainer.setAttribute('data-field', fieldName);
                    checklistContainer.setAttribute('data-type', 'checklist');
                    if (fieldConfig.required) {
                        checklistContainer.setAttribute('data-required', 'true');
                    }
                    checklistContainer.className = 'checklist-container mb-3';
                    
                    // Заголовок чеклиста
                    const checklistLabel = document.createElement('label');
                    checklistLabel.className = 'form-label';
                    checklistLabel.textContent = fieldConfig.label || fieldName;
                    if (fieldConfig.required) {
                        checklistLabel.innerHTML += ' <span class="text-danger">*</span>';
                    }
                    checklistContainer.appendChild(checklistLabel);
                    
                    // Создаем элементы чеклиста
                    fieldConfig.options.forEach((option, index) => {
                        // Основной контейнер для элемента
                        const itemDiv = document.createElement('div');
                        itemDiv.className = 'checklist-item mb-2 p-2 border rounded';
                        
                        // Внутренний контейнер для содержимого
                        const itemContent = document.createElement('div');
                        itemContent.className = 'd-flex align-items-center';
                        
                        // Toggle-переключатель
                        const toggleLabel = document.createElement('label');
                        toggleLabel.className = 'toggle me-3';
                        
                        const input = document.createElement('input');
                        input.type = 'checkbox';
                        input.id = `attr_${fieldName}_${option.value || index}`;
                        input.name = `${fieldName}[]`;
                        input.value = option.value || option.label;
                        input.className = 'empty-on-blur';
                        
                        const toggleSpan = document.createElement('span');
                        
                        toggleLabel.appendChild(input);
                        toggleLabel.appendChild(toggleSpan);
                        itemContent.appendChild(toggleLabel);
                        
                        // Текст метки
                        const textLabel = document.createElement('label');
                        textLabel.className = 'checkbox-text-label flex-grow-1';
                        textLabel.htmlFor = input.id;
                        textLabel.textContent = option.label;
                        itemContent.appendChild(textLabel);
                        
                        // Поле для количества (если countable)
                        if (option.countable) {
                            const countContainer = document.createElement('div');
                            countContainer.className = 'input_block middlerow';
                            
                            const countLabel = document.createElement('label');
                            countLabel.className = 'me-2 small';
                            countLabel.textContent = 'Кол-во:';
                            
                            const countInput = document.createElement('input');
                            // Добавим отображения label для input  
                            countInput.addEventListener("blur", function() {
                                if (this.value.trim() === "") {
                                this.classList.remove("empty-on-blur");
                                }
                            });
                            countInput.addEventListener("focus", function() {
                                this.classList.add("empty-on-blur");
                            });
                            countInput.type = 'number';
                            countInput.style.width = '100px';
                            countInput.min = 1;
                            countInput.max = 99;
                            countInput.value = 1;
                            countInput.disabled = !input.checked;
                            
                            input.addEventListener('change', () => {
                                countInput.disabled = !input.checked;
                                if (!input.checked) countInput.value = 1;
                            });
                            countContainer.appendChild(countInput);
                            countContainer.appendChild(countLabel);
                            itemContent.appendChild(countContainer);
                        }
                        
                        itemDiv.appendChild(itemContent);
                        checklistContainer.appendChild(itemDiv);
                    });
                    
                    dynamicFieldsContainer.appendChild(checklistContainer);
                    break;

                default:
                    input = document.createElement('input');
                    input.type = 'text';
                    fieldGroup.className = "input_block";
                    
            }
            if (input) {
                if (fieldConfig.type != "checkbox" && fieldConfig.type != "list" && fieldConfig.type != "checklist"){
                    const label = document.createElement('label');
                    label.textContent = fieldConfig.label || fieldName;
                    if (fieldConfig.required) {
                        label.innerHTML += ' <span class="text-danger">*</span>';
                    }
    
                    input.id = `attr_${fieldName}`;
                    input.name = fieldName;
                    if (input.required){
                        input.required = fieldConfig.required;
                    }
                    
                    if (fieldConfig.placeholder) {
                        input.placeholder = fieldConfig.placeholder;
                    }
    
                    // Добавим отображения label для input  
                    input.addEventListener("blur", function() {
                        if (this.value.trim() === "") {
                          this.classList.remove("empty-on-blur");
                        }
                    });
                    input.addEventListener("focus", function() {
                        this.classList.add("empty-on-blur");
                    });
    
                    if (fieldConfig.type == "checkbox" || fieldConfig.type == "list"){
                        fieldGroup.appendChild(label);
                        fieldGroup.appendChild(input);
                    } else {
                        fieldGroup.appendChild(input);
                        fieldGroup.appendChild(label);
                    }                
                    dynamicFieldsContainer.appendChild(fieldGroup);
                }
            }
        }
    })

    // Собиратель данных с полей
    function collectFormData() {
        const formData = {
            type: document.getElementById('equipmentType').value,
            inventory_number: document.getElementById('inventoryNumber').value,
            attributes: {}
        };
    
        // Собираем данные с динамических полей
        document.querySelectorAll('#dynamicFieldsContainer [data-field]').forEach(element => {
            const fieldName = element.getAttribute('data-field');
            const fieldType = element.getAttribute('data-type');
    
            if (fieldType === 'checklist') {
                // Обработка чеклиста
                const checkedItems = {};
                element.querySelectorAll('.checklist-item').forEach(item => {
                    const checkbox = item.querySelector('input[type="checkbox"]');
                    if (checkbox && checkbox.checked) {
                        const countInput = item.querySelector('input[type="number"]');
                        checkedItems[checkbox.value] = countInput ? parseInt(countInput.value) : true;
                    }
                });
                formData.attributes[fieldName] = checkedItems;
            } else if (fieldType === 'list') {
                // Обработка списка
                const items = [];
                element.querySelectorAll('.list-item').forEach(item => {
                    const itemData = {};
                    item.querySelectorAll('[data-subfield]').forEach(field => {
                        const subField = field.getAttribute('data-subfield');
                        itemData[subField] = field.value;
                    });
                    items.push(itemData);
                });
                formData.attributes[fieldName] = items;
            } else {
                // Обработка обычных полей
                if (element.type === 'checkbox') {
                    formData.attributes[fieldName] = element.checked;
                } else {
                    formData.attributes[fieldName] = element.value;
                }
            }
        });
    
        return formData;
    }

    // Обработчик отправки формы
    form.addEventListener("submit", async function (e) {
        e.preventDefault();
        
        // const typeId = typeSelect.value;
        // if (!typeId) {
        //     alert('Выберите тип оборудования');
        //     return;
        // }

        // const selectedType = equipmentTypes.find(t => t.id == typeId);
        // const formData = {
        //     type: typeId,
        //     inventory_number: document.getElementById('inventoryNumber').value,
        //     attributes: {}
        // };

        // // Собираем атрибуты
        // for (const [fieldName] of Object.entries(selectedType.attributes_schema)){
        //     const input = document.getElementById(`attr_${fieldName}`);
        //     if (!input) continue;

        //     let value;
        //     if (input.type === 'checkbox') {
        //         value = input.checked;
        //     } else if (input.type === 'number') {
        //         value = parseFloat(input.value);
        //     } else {
        //         value = input.value;
        //     }

        //     formData.attributes[fieldName] = value;
        // }
        try{
            const response = await fetch(server + 'api/addequipment/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(collectFormData())
            })

            if (response.ok){
                window.location.href = server + ""
            }
        }
        catch (error){
            console.log(error)
        }
    })

    // Процедура создания поля списка
    function createListField(fieldName, config){
        const fieldGroup = document.createElement('div');
        const container = document.createElement('div');
        const container_header = document.createElement('div');
        container_header.className = "list-container-header";
        const label = document.createElement('label');
        label.textContent = config.label || fieldName;
        container_header.appendChild(label);
        container.className = 'list-container';

        const itemsContainer = document.createElement('div');
        itemsContainer.className = 'list-container-body'
        container.appendChild(itemsContainer);

        const addButton = document.createElement('button');
        addButton.type = 'button';
        addButton.className = 'addButton';
        addButton.textContent = '+';
        container_header.appendChild(addButton);

        // Функция добавления элемента
        function addListItem() {
            const itemDiv = document.createElement('div');
            
            const fieldsRow = document.createElement('div');
            itemDiv.appendChild(fieldsRow);

            // Добавляем поля элемента
            for (const [subField, subConfig] of Object.entries(config.fields)){
                const col = document.createElement('div');
                const subLabel = document.createElement('label');
                subLabel.textContent = subConfig.label || subField;

                let subInput;
                
                if (subConfig.type === 'select'){
                    subInput = document.createElement('select');
                    subConfig.options.forEach(opt => {
                        const option = document.createElement('option');
                        option.value = opt;
                        option.textContent = opt;
                        subInput.appendChild(option);
                    });
                } else {
                    subInput = document.createElement('input');
                    subInput.type = subConfig.type || 'text';
                }
                subInput.className = "smallinput"
                col.className = 'input_block smallrow';
                // Добавим отображения label для input  
                subInput.addEventListener("blur", function() {
                    if (this.value.trim() === "") {
                        this.classList.remove("empty-on-blur");
                    }
                });
                subInput.addEventListener("focus", function() {
                    this.classList.add("empty-on-blur");
                });
                col.appendChild(subInput);
                col.appendChild(subLabel);
                const subcol = document.createElement('div');
                subcol.appendChild(col);
                fieldsRow.appendChild(subcol);
            }

            // Кнопка удаления
            const removeBtn = document.createElement('button');
            removeBtn.type = 'button';
            removeBtn.className = 'removeBtn'
            removeBtn.textContent = '-';
            removeBtn.addEventListener('click', () => {itemDiv.remove()});
            itemDiv.appendChild(removeBtn);
            itemsContainer.appendChild(itemDiv);
        }

        addButton.addEventListener('click', addListItem);

        // Добавляем элементы по умолчанию
        if (config.default && config.default.length > 0) {
            config.default.forEach(() => addListItem());
        } else if (config.required) {
            addListItem();
        }
        container.appendChild(container_header);
        container.appendChild(itemsContainer);
        fieldGroup.appendChild(container);
        dynamicFieldsContainer.appendChild(fieldGroup);
    }

    function getCookie(name){
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++){
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')){
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});

