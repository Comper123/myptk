const inputs = document.querySelectorAll('input select');

inputs.forEach(input => {
    input.addEventListener("blur", function() {
        if (this.value.trim() === "") {
          this.classList.remove("hastext");
        }
    });
    input.addEventListener("focus", function() {
        this.classList.add("hastext");
    });
})