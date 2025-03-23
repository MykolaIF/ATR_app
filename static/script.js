document.addEventListener("DOMContentLoaded", function () {
    const fetchButton = document.getElementById("fetch-data");
    const infoContainer = document.getElementById("info-content");
    const loadingIndicator = document.getElementById("loading");

    fetchButton.addEventListener("click", async () => {
        let seconds = 0;
        const timerElement = document.getElementById("timer");

        // Показати індикатор і запустити таймер
        loadingIndicator.classList.remove("hidden");
        fetchButton.disabled = true;

        const timerInterval = setInterval(() => {
            seconds++;
            timerElement.textContent = seconds;
        }, 1000);

        try {
            const response = await fetch("/user/get-top-atr");
            const data = await response.json();

            // Оновлення вмісту
            infoContainer.innerHTML = "";
            data.forEach((item, index) => {
                const p = document.createElement("p");
                p.textContent = `${index + 1}. ${item.coin} - ${item.percent}%`;
                infoContainer.appendChild(p);
            });
        } catch (error) {
            infoContainer.innerHTML = "<p>Помилка отримання даних.</p>";
        } finally {
            // Приховати індикатор і зупинити таймер
            clearInterval(timerInterval);
            loadingIndicator.classList.add("hidden");
            fetchButton.disabled = false;
        }
    });

});
