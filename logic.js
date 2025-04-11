// Добавим функцию для отображения графика для каждой привычки
function showStats(index) {
    if (currentChartIndex === index) {
      // Если пользователь снова нажал на тот же элемент, скрываем график
      chartContainer.style.display = "none";
      currentChartIndex = null;
      return;
    }
  
    // Собираем данные для графика
    const stats = {};
    habits[index].doneDates.forEach(date => {
      stats[date] = (stats[date] || 0) + 1;
    });
  
    // Сортируем даты
    const labels = Object.keys(stats).sort();
    const data = labels.map(date => stats[date]);
  
    // Показываем контейнер для графика
    chartContainer.style.display = "block";
    currentChartIndex = index;
  
    // Создаем график с помощью Chart.js
    const ctx = document.getElementById("habitChart").getContext("2d");
    
    // Если график уже есть, уничтожаем его и создаем новый
    if (window.habitChart) window.habitChart.destroy();
  
    // Создаем новый график
    window.habitChart = new Chart(ctx, {
      type: 'bar', // Тип диаграммы
      data: {
        labels: labels, // Даты
        datasets: [{
          label: `Статистика: ${habits[index].name}`, // Название привычки
          data: data, // Количество выполнений привычки в каждый день
          backgroundColor: '#4caf50', // Цвет столбцов
          borderRadius: 8, // Радиус скругления столбцов
        }]
      },
      options: {
        responsive: true, // График адаптивный
        animation: {
          duration: 600,
          easing: 'easeOutQuart'
        },
        scales: {
          y: {
            beginAtZero: true, // Начинаем отсчет с нуля
            ticks: {
              precision: 0 // Убираем десятичные числа
            }
          }
        },
        plugins: {
          legend: {
            display: true // Показывать легенду
          },
          tooltip: {
            backgroundColor: "#333", // Цвет фона тултипа
            titleColor: "#fff", // Цвет заголовка тултипа
            bodyColor: "#fff", // Цвет текста тултипа
          }
        }
      }
    });
  }
  