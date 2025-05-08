const slider_indicators_block = document.querySelector(".slider_indicators");
const slider_indicators = slider_indicators_block.querySelectorAll(".indicator");

const slider_images_block = document.querySelector(".slider_container");
const slider_images = slider_images_block.querySelectorAll(".img");


function toSlide(slide){
    // Сбросим старые изображения
    for (let i = 0; i < slider_images.length; i++){
        slider_images[i].classList = "img";
    }
    // Установим новое изображение
    slider_images[slide - 1].classList = "img active";

    // Сбросим старые кнопки
    for (let i = 0; i < slider_indicators.length; i++){
        slider_indicators[i].classList = "indicator";
    }
    // Установим новое изображение
    slider_indicators[slide - 1].classList = "indicator active";
}