/* Ana panel: tanıtım hareketi ve veri grafikleri */
document.addEventListener("DOMContentLoaded", () => {
  const banner = document.getElementById("tanitim");
  const bannerToggle = document.getElementById("bannerMotionToggle");
  const prefersReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  if (banner && bannerToggle) {
    bannerToggle.addEventListener("click", () => {
      const paused = banner.classList.toggle("is-paused");
      bannerToggle.setAttribute("aria-pressed", String(paused));
      bannerToggle.setAttribute(
        "aria-label",
        paused ? "Tanıtım geçişini oynat" : "Tanıtım geçişini durdur"
      );
      bannerToggle.querySelector("i").className = paused
        ? "bi bi-play-fill"
        : "bi bi-pause-fill";
    });
  }

  const dataElement = document.getElementById("dash-data");
  const yearCanvas = document.getElementById("yearTrendChart");
  const statusCanvas = document.getElementById("statusDistributionChart");
  if (!dataElement || !yearCanvas || !statusCanvas || !window.Chart) {
    return;
  }

  const data = JSON.parse(dataElement.textContent);
  const burgundy = "#8C1D2F";
  const gold = "#B8860B";
  const ink = "#303740";
  const muted = "#5F6873";
  const grid = "#E4E7EB";
  const animation = prefersReducedMotion
    ? false
    : { duration: 550, easing: "easeOutQuart" };

  Chart.defaults.font.family =
    '"Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif';
  Chart.defaults.color = muted;

  const moneyFormatter = new Intl.NumberFormat("tr-TR", {
    style: "currency",
    currency: "TRY",
    maximumFractionDigits: 0,
  });

  new Chart(yearCanvas, {
    data: {
      labels: data.years,
      datasets: [
        {
          type: "bar",
          label: "Kayıt adedi",
          data: data.year_counts,
          backgroundColor: "rgba(140, 29, 47, .84)",
          borderColor: burgundy,
          borderWidth: 0,
          borderRadius: 5,
          maxBarThickness: 34,
          yAxisID: "count",
        },
        {
          type: "line",
          label: "Ceza tutarı",
          data: data.year_amounts,
          borderColor: gold,
          backgroundColor: gold,
          borderWidth: 2,
          pointRadius: 3,
          pointHoverRadius: 5,
          pointBackgroundColor: "#FFFFFF",
          pointBorderColor: gold,
          pointBorderWidth: 2,
          tension: 0.25,
          yAxisID: "amount",
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation,
      interaction: { mode: "index", intersect: false },
      plugins: {
        legend: {
          position: "bottom",
          align: "start",
          labels: {
            color: ink,
            usePointStyle: true,
            pointStyle: "circle",
            boxWidth: 8,
            padding: 18,
          },
        },
        tooltip: {
          callbacks: {
            label(context) {
              if (context.dataset.yAxisID === "amount") {
                return ` ${context.dataset.label}: ${moneyFormatter.format(context.raw)}`;
              }
              return ` ${context.dataset.label}: ${context.raw}`;
            },
          },
        },
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: muted },
          border: { color: grid },
        },
        count: {
          beginAtZero: true,
          position: "left",
          ticks: { precision: 0, color: muted },
          grid: { color: grid },
          border: { display: false },
        },
        amount: {
          beginAtZero: true,
          position: "right",
          ticks: {
            color: muted,
            callback(value) {
              return moneyFormatter.format(value);
            },
          },
          grid: { drawOnChartArea: false },
          border: { display: false },
        },
      },
    },
  });

  new Chart(statusCanvas, {
    type: "doughnut",
    data: {
      labels: data.status_labels,
      datasets: [
        {
          data: data.status_counts,
          backgroundColor: ["#D49A20", "#B42335", "#247A4B", "#8A939E"],
          borderColor: "#FFFFFF",
          borderWidth: 3,
          hoverOffset: 4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation,
      cutout: "68%",
      plugins: {
        legend: {
          position: "bottom",
          labels: {
            color: ink,
            usePointStyle: true,
            pointStyle: "circle",
            boxWidth: 8,
            padding: 14,
          },
        },
        tooltip: {
          callbacks: {
            label(context) {
              const total = context.dataset.data.reduce(
                (sum, value) => sum + value,
                0
              );
              const percent = total
                ? Math.round((context.raw / total) * 100)
                : 0;
              return ` ${context.label}: ${context.raw} kayıt (%${percent})`;
            },
          },
        },
      },
    },
  });
});
