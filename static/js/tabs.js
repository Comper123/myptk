// Получим линки табов
const tab_links = document.getElementById("tabs_links");
// Получим все возможные сыылки из табов
const tab_links_list = tab_links.querySelectorAll("a");
// Получим все доступные табы
const tabs = document.getElementById("tabs");
const tabs_list = tabs.querySelectorAll("div");

tab_links_list.forEach(link => {
    link.addEventListener("click", (e) => {
        e.preventDefault();
        // Очищаем все табы от активности
        tabs_list.forEach(tab => {
            tab.classList = ""
        });
        // Устанавливаем активный таб
        let index = parseInt(link.getAttribute('data-id')) - 1;
        tabs_list[index].classList = "active_tab";
    });
});