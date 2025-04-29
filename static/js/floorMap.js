const mapContainer = document.getElementById('map-container');
  // const mapImage = document.getElementById('map-image');
  const mapImage = mapImage.querySelector('image');
  const editModeToggle = document.getElementById("editModeToggle");
  

  // Состояние карты
  const state = {
    scale: 1,                     // Текущий масштаб
    minScale: 1,                  // Минимальный масштаб
    maxScale: 4,                  // Максимальный масштаб
    scaleCoef: 0.1,               // Коэфициент масштабирования
    startPoint: { x: 0, y: 0 },
    constsize: {width: mapImage.getBoundingClientRect().width, height: mapImage.getBoundingClientRect().height},
    size: {width: {{ width }}, height: {{ height }}},
    aspectRatio: {{ width }} / {{ height }}, // Пропорции изображения
    isScaling: true,               // Возможность масштабирования
  };


  // Подключаем включение/выключение режима масштабирования
  editModeToggle.addEventListener('change',() => {
    state.isScaling = !editModeToggle.checked;
  })

  function transformMap(){
    mapImage.style.transform = `translate(${state.startPoint.x}px, ${state.startPoint.y}px)`;
  }

  // Процедура обновления положения
  function updateMap(mouseX, mouseY){
    // Изменяем ширину и высоту карты
    state.size.width = state.constsize.width * state.scale;
    state.size.height = state.constsize.height * state.scale;
    mapImage.style.width = `${state.size.width}px`;
    mapImage.style.height = `${state.size.height}px`;
    // Изменяем координаты карты
    var deltaX = (mouseX / state.constsize.width) * (state.scale * state.constsize.width - state.constsize.width);
    var deltaY = (mouseY / state.constsize.height) * (state.scale * state.constsize.height - state.constsize.height);
    state.startPoint.x = -deltaX;
    state.startPoint.y = -deltaY;
    // Применяем смещение
    transformMap();
  }


  // Добавим ивент на масштабирование и перемещение карты
  mapContainer.addEventListener("wheel", (e) => {
    // Игнорируем дефолтное поведение при ивенте
    e.preventDefault();
    
    // Перемещение по горизонтали
    if (e.shiftKey && !e.ctrlKey && state.isScaling){
      // Проверяем выход за границу карты
      if (e.deltaY > 0 && state.constsize.width + state.startPoint.x - state.size.width / 100 < state.constsize.width){
        // Проверяем возможность перемещения вправо
        console.log("Вправо");
        state.startPoint.x = -1 * (state.size.width - state.constsize.width);        
      }
      else if (e.deltaY < 0 && state.startPoint.x + (state.size.width / 100) > 0){
        // Проверяем возможность перемещения влево
        console.log("Влево");
        state.startPoint.x = 0;
      }
      else{
        state.startPoint.x += state.size.width / 100 * (e.deltaY < 0 ? -1 : 1);
      }
      // Перемещаем карту
      transformMap();
      return;
    }

    // Масштабирование (ctrl + колесо)
    if (e.ctrlKey && state.isScaling){
      // Проверяем на возможность масштабирования иначе выходим из обработчика
      if ((state.scale === state.minScale && e.deltaY > 0) || 
          (state.scale === state.maxScale && e.deltaY < 0)) return;
      var zoomDelta = state.scaleCoef * (e.deltaY > 0 ? -1 : 1); // Определяем величину масштабирования
      state.scale += zoomDelta;
      // Координаты курсора
      let mouseX = e.clientX - mapImage.getBoundingClientRect().left;
      let mouseY = e.clientY - mapImage.getBoundingClientRect().top;
      // Обновим положение нашей карты
      updateMap(mouseX, mouseY);
      return;
    }

    if (!e.ctrlKey && !e.shiftKey && state.isScaling){
      // Перемещение по вертикали
      if (((e.deltaY > 0 && state.startPoint.y > 0) ||
      (e.deltaY < 0 && state.startPoint.y > state.height)) 
      ){
      // Проверяем выход за границу карты
      // state.startPoint.y = 0;
      return;
      } 
      // Перемещаем карту
      state.startPoint.y -= state.size.height / 100 * (e.deltaY > 0 ? 1 : -1);
      mapImage.style.transform = `translate(${state.startPoint.x}px, ${state.startPoint.y}px)`;
    }
  })