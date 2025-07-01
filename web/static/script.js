let previousBenchState = null;
const charts = {};  // stores Chart.js instances by canvas ID

/**
 * Fetch data from the Flask API.
 */
async function fetchData() {
  const response = await fetch('/data');
  return await response.json();
}

/**
 * Draw or update a line chart (temperature, humidity, feels-like).
 */
function drawChart(id, label, data, color) {
  const ctx = document.getElementById(id).getContext('2d');

  if (!charts[id]) {
    // Create the chart the first time
    charts[id] = new Chart(ctx, {
      type: 'line',
      data: {
        labels: data.map(p => new Date(p.time).toLocaleTimeString()),
        datasets: [{
          label: label,
          data: data.map(p => p.value),
          borderColor: color,
          fill: false,
          tension: 0.4,
          pointRadius: 3,
          pointHoverRadius: 6
        }]
      },
      options: {
        responsive: true,
        scales: {
          x: {
            ticks: { autoSkip: true, maxTicksLimit: 5 }
          },
          y: { beginAtZero: true }
        },
        plugins: {
          tooltip: {
            callbacks: {
              label: ctx => `${ctx.dataset.label}: ${ctx.parsed.y.toFixed(2)}`
            }
          }
        }
      }
    });
  } else {
    // Update existing chart in place
    charts[id].data.labels = data.map(p => new Date(p.time).toLocaleTimeString());
    charts[id].data.datasets[0].data = data.map(p => p.value);
    charts[id].update();
  }
}

/**
 * Main UI update function, runs every 2 seconds.
 */
async function render() {
  const { temp, hum, feels, sun, rain, sitting, avg_scores, total_reviews } = await fetchData();
  
  drawChart('tempChart', 'Temperature (°C)', temp, 'red');
  drawChart('humidityChart', 'Humidity (%)', hum, 'blue');
  drawChart('feelsChart', 'Feels Like (°C)', feels, 'orange');

  // Ensure consistent normalized values
  const latestSit = sitting.length > 0 ? sitting.at(-1).value : 0;
  const latestSitState = (latestSit === 1 || latestSit === true) ? 1 : 0;
  const latestRain = rain.at(-1)?.value;
  const latestSun = sun.at(-1)?.value;
  const latestAvgScore = avg_scores.length > 0 ? avg_scores.at(-1).value : null;
  const latestTotalReviews = total_reviews.length > 0 ? total_reviews.at(-1).value : 0;

  // Update bench status
  const benchCard = document.getElementById('benchStatus');
  if (latestSit === 1) {
    benchCard.textContent = 'Bench is taken';
    benchCard.classList.add('bench-taken');
    benchCard.classList.remove('bench-free');
  } else {
    benchCard.textContent = 'Bench is free';
    benchCard.classList.add('bench-free');
    benchCard.classList.remove('bench-taken');
  }

  // Reload the whole page if bench state changed
  if (previousBenchState !== null && previousBenchState !== latestSitState) {
      console.log("Bench state changed! Reloading page...");
      location.reload();
  }
  previousBenchState = latestSitState;

  // Update other cards
  document.getElementById('rainChance').textContent = 
    latestRain === 1 ? 'Rain chance is high – bring an umbrella!' : 'Rain chance is low';

  document.getElementById('shadeStatus').textContent = 
    latestSun > 0.6 ? 'Full sun exposure' :
    latestSun > 0.2 ? 'Partial sunny' :
                      'Mostly shaded';
  
  
  const reviewStatus = document.getElementById('reviewStatus');
  if (latestTotalReviews > 0) {
    reviewStatus.textContent = `Average comfort: ⭐ ${latestAvgScore} (from ${latestTotalReviews} reviews)`;
  } else {
    reviewStatus.textContent = `No reviews yet`;
  }
}

// Start fetching & updating UI every 2 seconds
render();
setInterval(render, 2000);
