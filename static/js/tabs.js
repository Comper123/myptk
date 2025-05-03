// Получим линки табов
const tab_links = document.getElementById("tabs_links");
// Получим все возможные сыылки из табов
const tab_links_list = tab_links.querySelectorAll("a");
// Получим все доступные табы
const tabs = document.getElementById("tabs");
const tabs_list = tabs.querySelectorAll(".tab");

tab_links_list.forEach(link => {
    link.addEventListener("click", (e) => {
        e.preventDefault();
        // Очищаем все табы от активности
        tabs_list.forEach(tab => {
            tab.classList = "tab"
        });
        // Очищаем все ссылки на табы от активности
        tab_links_list.forEach(tablink => {
            tablink.classList = ""
        });

        // Устанавливаем активный таб
        let index = parseInt(link.getAttribute('data-id')) - 1;
        tabs_list[index].classList = "tab active_tab";
        // Установим авктиную ссылку таба
        tab_links_list[index].classList = "active"
    });
});