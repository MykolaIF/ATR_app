function fetchOrders() {
    fetch("/admin/get-orders")
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("orders-container");
            container.innerHTML = "";

            // Виконані ордери
            data.completed_orders.forEach(order => {
                const orderElement = document.createElement("div");
                orderElement.classList.add("order", order.side.toLowerCase());  // buy/sell
                orderElement.innerText = `${order.time} ${order.side.padEnd(4, ' ')} ${order.price.toFixed(4).padStart(6, ' ')} ${Math.floor(order.quantity).toString().padStart(6, ' ')}`;
                container.appendChild(orderElement);
            });

            // Розділювач
            if (data.open_orders.length > 0) {
                const divider = document.createElement("div");
                divider.classList.add("divider");
                container.appendChild(divider);
            }

            // Відкриті ордери
            data.open_orders.forEach(order => {
                const orderElement = document.createElement("div");
                orderElement.classList.add("order", order.side.toLowerCase());  // buy/sell
                orderElement.innerText = `${order.time} ${order.side.padEnd(4, ' ')} ${order.price.toFixed(4).padStart(6, ' ')} ${Math.floor(order.quantity).toString().padStart(6, ' ')}`;
                container.appendChild(orderElement);
            });
        })
        .catch(error => console.error("Помилка завантаження:", error));
}

// Оновлення кожні 20 секунд
setInterval(fetchOrders, 20000);
fetchOrders();
