document.addEventListener("DOMContentLoaded", () => {
    const root = document.documentElement;
    const storedTheme = localStorage.getItem("theme");
    if (storedTheme) {
        root.setAttribute("data-bs-theme", storedTheme);
    }

    const themeToggle = document.getElementById("themeToggle");
    if (themeToggle) {
        themeToggle.addEventListener("click", () => {
            const nextTheme = root.getAttribute("data-bs-theme") === "dark" ? "light" : "dark";
            root.setAttribute("data-bs-theme", nextTheme);
            localStorage.setItem("theme", nextTheme);
        });
    }

    document.querySelectorAll("[data-bs-toggle='tooltip']").forEach((element) => {
        new bootstrap.Tooltip(element);
    });

    const form = document.querySelector(".prediction-form");
    const progressBar = document.getElementById("formProgress");
    const progressLabel = document.getElementById("progressLabel");
    if (form && progressBar && progressLabel) {
        const updateProgress = () => {
            const fields = [...form.querySelectorAll("input, select")].filter((field) => field.name);
            const completed = fields.filter((field) => field.value !== "").length;
            const percent = Math.max(16, Math.round((completed / fields.length) * 100));
            progressBar.style.width = `${percent}%`;
            progressLabel.textContent = `${completed} of ${fields.length} fields complete`;
        };
        form.addEventListener("input", updateProgress);
        form.addEventListener("change", updateProgress);
        form.addEventListener("submit", (event) => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add("was-validated");
        });
        updateProgress();
    }

    const search = document.getElementById("analyticsSearch");
    const table = document.getElementById("recentTable");
    if (search && table) {
        search.addEventListener("input", () => {
            const query = search.value.toLowerCase();
            table.querySelectorAll("tbody tr").forEach((row) => {
                row.style.display = row.textContent.toLowerCase().includes(query) ? "" : "none";
            });
        });
    }

    renderCharts();
});

function chartPayload(id) {
    const canvas = document.getElementById(id);
    if (!canvas || typeof Chart === "undefined") {
        return null;
    }
    const data = JSON.parse(canvas.dataset.chart || "{}");
    return { canvas, labels: Object.keys(data), values: Object.values(data) };
}

function renderCharts() {
    const colors = ["#2563eb", "#14b8a6", "#f59e0b", "#ef4444", "#8b5cf6"];
    const doughnutCharts = [
        ["predictionChart", "Prediction Distribution"],
        ["confidenceChart", "Confidence Distribution"],
        ["modelChart", "Model Usage"],
    ];

    doughnutCharts.forEach(([id, title]) => {
        const payload = chartPayload(id);
        if (!payload) {
            return;
        }
        new Chart(payload.canvas, {
            type: "doughnut",
            data: {
                labels: payload.labels,
                datasets: [{ label: title, data: payload.values, backgroundColor: colors }],
            },
            options: { responsive: true, plugins: { legend: { position: "bottom" } } },
        });
    });

    const trend = chartPayload("trendChart");
    if (trend) {
        new Chart(trend.canvas, {
            type: "line",
            data: {
                labels: trend.labels,
                datasets: [{
                    label: "Predictions",
                    data: trend.values,
                    borderColor: "#2563eb",
                    backgroundColor: "rgba(37, 99, 235, 0.12)",
                    fill: true,
                    tension: 0.35,
                }],
            },
            options: { responsive: true, plugins: { legend: { display: false } } },
        });
    }
}
