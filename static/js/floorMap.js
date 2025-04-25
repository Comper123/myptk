
  // Инициализация
  function init() {
    updateContainerSize();
    setupInitialViewBox();
    
    // События
    mapImage.addEventListener('mousedown', startPan);
    document.addEventListener('mousemove', handlePan);
    document.addEventListener('mouseup', endPan);
    mapContainer.addEventListener('wheel', handleWheel, { passive: false });
    window.addEventListener('resize', handleResize);
    
    mapContainer.style.cursor = 'grab';
  }

  function updateContainerSize() {
    state.containerSize = {
      width: mapContainer.clientWidth,
      height: mapContainer.clientHeight
    };
  }

  function setupInitialViewBox() {
    // Устанавливаем начальный viewBox (можно адаптировать под ваши нужды)
    state.viewBox = {
      x: 0,
      y: 0,
      width: mapContainer.clientWidth,
      height: mapContainer.clientHeight
    };
    
    updateViewBox();
  }

  function updateViewBox() {
    
    
    // Масштабируем изображение внутри SVG
    svgImage.setAttribute('width', state.viewBox.width);
    svgImage.setAttribute('height', state.viewBox.height);
    svgImage.setAttribute('x', state.viewBox.x);
    svgImage.setAttribute('y', state.viewBox.y);
  }

  function constrainViewBox() {
    // Ограничиваем перемещение
    const maxX = state.viewBox.width * (1 - 1/state.scale);
    const maxY = state.viewBox.height * (1 - 1/state.scale);
    
    state.viewBox.x = Math.min(0, Math.max(-maxX, state.viewBox.x));
    state.viewBox.y = Math.min(0, Math.max(-maxY, state.viewBox.y));
    
    updateViewBox();
  }

  // Обработчики событий
  function startPan(e) {
    if (e.button === 0) {
      state.isPanning = true;
      state.startPoint = { x: e.clientX, y: e.clientY };
      mapContainer.style.cursor = 'grabbing';
      e.preventDefault();
    }
  }

  function handlePan(e) {
    if (!state.isPanning) return;
    
    const dx = (e.clientX - state.startPoint.x) * (state.viewBox.width / state.containerSize.width);
    const dy = (e.clientY - state.startPoint.y) * (state.viewBox.height / state.containerSize.height);
    
    state.viewBox.x -= dx;
    state.viewBox.y -= dy;
    
    constrainViewBox();
    state.startPoint = { x: e.clientX, y: e.clientY };
    e.preventDefault();
  }

  function endPan() {
    state.isPanning = false;
    mapContainer.style.cursor = 'grab';
  }

  function handleWheel(e) {
    e.preventDefault();
    
    // Вертикальное перемещение (обычное колесо)
    if (!e.ctrlKey && !e.shiftKey) {
      state.viewBox.y += e.deltaY;
      constrainViewBox();
      return;
    }
    
    // Горизонтальное перемещение (shift + колесо)
    if (e.shiftKey && !e.ctrlKey) {
      state.viewBox.x += e.deltaY;
      constrainViewBox();
      return;
    }
    
    // Масштабирование (ctrl + колесо)
    if (e.ctrlKey) {
      const zoomIntensity = 0.1;
      const wheelDelta = -Math.sign(e.deltaY);
      const oldScale = state.scale;
      
      // Вычисляем новый масштаб
      state.scale = Math.max(state.minScale, 
                   Math.min(state.maxScale, 
                   state.scale * (1 + wheelDelta * zoomIntensity)));
      
      if (state.scale === oldScale) return;
      
      // Координаты курсора
      const mouseX = e.clientX - mapContainer.getBoundingClientRect().left;
      const mouseY = e.clientY - mapContainer.getBoundingClientRect().top;
      
      // Процентное положение курсора
      const mouseXPercent = mouseX / state.containerSize.width;
      const mouseYPercent = mouseY / state.containerSize.height;
      
      // Вычисляем новые размеры viewBox
      const scaleChange = state.scale / oldScale;
      const newWidth = state.viewBox.width / scaleChange;
      const newHeight = state.viewBox.height / scaleChange;
      
      // Корректируем viewBox
      state.viewBox.x += mouseXPercent * (state.viewBox.width - newWidth);
      state.viewBox.y += mouseYPercent * (state.viewBox.height - newHeight);
      state.viewBox.width = newWidth;
      state.viewBox.height = newHeight;
      
      constrainViewBox();
    }
  }

  function handleResize() {
    updateContainerSize();
    constrainViewBox();
  }

  // Запуск
  init();