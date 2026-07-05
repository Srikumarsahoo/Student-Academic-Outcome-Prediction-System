/* ============================================================
   STUDENT PREDICT — ENHANCED JAVASCRIPT
   Scroll reveals, step wizard, animated counters, chart themes
   ============================================================ */

document.addEventListener("DOMContentLoaded", () => {
    initTheme();
    initTooltips();
    initScrollReveal();
    initNavbarScroll();
    initStepWizard();
    initCounterAnimation();
    initTableSearch();
    renderCharts();
});

/* ─── Theme Toggle ─── */
function initTheme() {
    const root = document.documentElement;
    const storedTheme = localStorage.getItem("theme");
    if (storedTheme) {
        root.setAttribute("data-bs-theme", storedTheme);
    }
    updateThemeIcon();

    const themeToggle = document.getElementById("themeToggle");
    if (themeToggle) {
        themeToggle.addEventListener("click", () => {
            const next = root.getAttribute("data-bs-theme") === "dark" ? "light" : "dark";
            root.setAttribute("data-bs-theme", next);
            localStorage.setItem("theme", next);
            updateThemeIcon();
            // Re-render charts with new theme
            renderCharts();
        });
    }
}

function updateThemeIcon() {
    const icon = document.getElementById("themeIcon");
    if (!icon) return;
    const isDark = document.documentElement.getAttribute("data-bs-theme") === "dark";
    icon.className = isDark ? "bi bi-sun" : "bi bi-moon-stars";
}

/* ─── Bootstrap Tooltips ─── */
function initTooltips() {
    document.querySelectorAll("[data-bs-toggle='tooltip']").forEach((el) => {
        new bootstrap.Tooltip(el);
    });
}

/* ─── Scroll Reveal (Intersection Observer) ─── */
function initScrollReveal() {
    const revealElements = document.querySelectorAll(".reveal");
    if (!revealElements.length) return;

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("revealed");
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.1, rootMargin: "0px 0px -40px 0px" }
    );

    revealElements.forEach((el) => observer.observe(el));
}

/* ─── Navbar Scroll Effect ─── */
function initNavbarScroll() {
    const navbar = document.getElementById("mainNav");
    if (!navbar) return;

    const onScroll = () => {
        navbar.classList.toggle("scrolled", window.scrollY > 20);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
}

/* ─── Step Wizard ─── */
function initStepWizard() {
    const form = document.getElementById("predictionForm");
    if (!form) return;

    const steps = form.querySelectorAll(".form-section[data-step]");
    const dots = form.querySelectorAll(".step-dot[data-step-dot]");
    const connectors = form.querySelectorAll(".step-connector");
    let currentStep = 0;

    // Field labels map for the review panel
    const fieldLabels = {
        age: "Age",
        gender: "Gender",
        course: "Course",
        admission_grade: "Admission Grade",
        model: "Prediction Model",
        scholarship_holder: "Scholarship Holder",
        debtor: "Debtor",
        tuition_fees_up_to_date: "Tuition Fees Up To Date",
        sem1_enrolled: "Sem 1 Enrolled",
        sem1_approved: "Sem 1 Approved",
        sem1_grade: "Sem 1 Grade",
        sem2_enrolled: "Sem 2 Enrolled",
        sem2_approved: "Sem 2 Approved",
        sem2_grade: "Sem 2 Grade",
        mother_qualification: "Mother's Qualification",
        father_qualification: "Father's Qualification",
    };

    function showStep(index) {
        steps.forEach((s, i) => {
            s.classList.toggle("active-step", i === index);
        });

        dots.forEach((d, i) => {
            d.classList.remove("active", "completed");
            if (i < index) d.classList.add("completed");
            else if (i === index) d.classList.add("active");
        });

        connectors.forEach((c, i) => {
            c.classList.toggle("filled", i < index);
        });

        currentStep = index;

        // Populate review panel on last step
        if (index === steps.length - 1) {
            populateReview();
        }

        // Scroll to step indicator
        const indicator = document.getElementById("stepIndicator");
        if (indicator) {
            const offset = indicator.getBoundingClientRect().top + window.scrollY - 100;
            window.scrollTo({ top: offset, behavior: "smooth" });
        }
    }

    function getDisplayValue(field) {
        if (field.tagName === "SELECT" && field.selectedIndex > 0) {
            return field.options[field.selectedIndex].text;
        }
        return field.value || "—";
    }

    function populateReview() {
        const panel = document.getElementById("reviewPanel");
        if (!panel) return;

        const fields = [...form.querySelectorAll("input[name], select[name]")];
        let html = '<h4><i class="bi bi-clipboard-check me-1"></i> Your Entries</h4>';

        fields.forEach((field) => {
            const label = fieldLabels[field.name] || field.name;
            const value = getDisplayValue(field);
            html += `<div class="review-row"><span>${label}</span><span>${value}</span></div>`;
        });

        panel.innerHTML = html;
    }

    function validateCurrentStep() {
        const currentSection = steps[currentStep];
        const fields = currentSection.querySelectorAll("input[required], select[required]");
        let valid = true;

        fields.forEach((field) => {
            if (!field.value || field.value === "") {
                field.classList.add("is-invalid");
                valid = false;
            } else {
                field.classList.remove("is-invalid");
                field.classList.add("is-valid");
            }
        });

        return valid;
    }

    // Next buttons
    form.querySelectorAll(".btn-next").forEach((btn) => {
        btn.addEventListener("click", () => {
            if (validateCurrentStep() && currentStep < steps.length - 1) {
                showStep(currentStep + 1);
            }
        });
    });

    // Previous buttons
    form.querySelectorAll(".btn-prev").forEach((btn) => {
        btn.addEventListener("click", () => {
            if (currentStep > 0) {
                showStep(currentStep - 1);
            }
        });
    });

    // Clickable step dots (only go to completed or current steps)
    dots.forEach((dot, i) => {
        dot.addEventListener("click", () => {
            if (i <= currentStep || dot.classList.contains("completed")) {
                showStep(i);
            }
        });
    });

    // Live field validation feedback
    form.addEventListener("input", (e) => {
        const field = e.target;
        if (field.hasAttribute("required")) {
            if (field.value && field.value !== "") {
                field.classList.remove("is-invalid");
                field.classList.add("is-valid");
            }
        }
    });

    form.addEventListener("change", (e) => {
        const field = e.target;
        if (field.hasAttribute("required")) {
            if (field.value && field.value !== "") {
                field.classList.remove("is-invalid");
                field.classList.add("is-valid");
            }
        }
    });

    // Form submission validation
    form.addEventListener("submit", (e) => {
        if (!form.checkValidity()) {
            e.preventDefault();
            e.stopPropagation();
        }
        form.classList.add("was-validated");
    });

    // Initialize first step
    showStep(0);
}

/* ─── Animated Counters ─── */
function initCounterAnimation() {
    const counters = document.querySelectorAll("[data-count]");
    if (!counters.length) return;

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.3 }
    );

    counters.forEach((el) => observer.observe(el));
}

function animateCounter(element) {
    const target = parseInt(element.dataset.count, 10);
    const suffix = element.dataset.suffix || "";
    const duration = 1500;
    const startTime = performance.now();

    function tick(now) {
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / duration, 1);
        // Ease-out cubic
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = Math.round(eased * target);

        element.textContent = current.toLocaleString() + suffix;

        if (progress < 1) {
            requestAnimationFrame(tick);
        }
    }

    requestAnimationFrame(tick);
}

/* ─── Analytics Table Search ─── */
function initTableSearch() {
    const search = document.getElementById("analyticsSearch");
    const table = document.getElementById("recentTable");
    if (!search || !table) return;

    search.addEventListener("input", () => {
        const query = search.value.toLowerCase();
        table.querySelectorAll("tbody tr").forEach((row) => {
            row.style.display = row.textContent.toLowerCase().includes(query) ? "" : "none";
        });
    });
}

/* ─── Charts ─── */
function chartPayload(id) {
    const canvas = document.getElementById(id);
    if (!canvas || typeof Chart === "undefined") return null;
    const data = JSON.parse(canvas.dataset.chart || "{}");
    return { canvas, labels: Object.keys(data), values: Object.values(data) };
}

// Track chart instances for theme-swap re-rendering
const chartInstances = {};

function renderCharts() {
    // Destroy existing instances before re-rendering
    Object.values(chartInstances).forEach((c) => c.destroy());
    Object.keys(chartInstances).forEach((k) => delete chartInstances[k]);

    const isDark = document.documentElement.getAttribute("data-bs-theme") === "dark";
    const textColor = isDark ? "#94a3b8" : "#475569";
    const gridColor = isDark ? "rgba(148,163,184,0.1)" : "rgba(148,163,184,0.15)";

    const colors = ["#6366f1", "#06b6d4", "#10b981", "#f59e0b", "#ec4899"];

    Chart.defaults.color = textColor;
    Chart.defaults.borderColor = gridColor;

    const doughnutCharts = [
        ["predictionChart", "Prediction Distribution"],
        ["confidenceChart", "Confidence Distribution"],
        ["modelChart", "Model Usage"],
    ];

    doughnutCharts.forEach(([id, title]) => {
        const payload = chartPayload(id);
        if (!payload) return;

        chartInstances[id] = new Chart(payload.canvas, {
            type: "doughnut",
            data: {
                labels: payload.labels,
                datasets: [{
                    label: title,
                    data: payload.values,
                    backgroundColor: colors,
                    borderWidth: 0,
                    hoverBorderWidth: 2,
                    hoverBorderColor: isDark ? "#1e293b" : "#ffffff",
                }],
            },
            options: {
                responsive: true,
                cutout: "65%",
                plugins: {
                    legend: {
                        position: "bottom",
                        labels: {
                            padding: 16,
                            usePointStyle: true,
                            pointStyle: "circle",
                            font: { weight: "600", family: "Inter" },
                        },
                    },
                },
            },
        });
    });

    const trend = chartPayload("trendChart");
    if (trend) {
        chartInstances["trendChart"] = new Chart(trend.canvas, {
            type: "line",
            data: {
                labels: trend.labels,
                datasets: [{
                    label: "Predictions",
                    data: trend.values,
                    borderColor: "#6366f1",
                    backgroundColor: isDark ? "rgba(99,102,241,0.08)" : "rgba(99,102,241,0.12)",
                    fill: true,
                    tension: 0.4,
                    borderWidth: 2.5,
                    pointBackgroundColor: "#6366f1",
                    pointBorderColor: isDark ? "#151b2b" : "#ffffff",
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                }],
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false },
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { font: { family: "Inter", weight: "600" } },
                    },
                    y: {
                        beginAtZero: true,
                        grid: { color: gridColor },
                        ticks: { font: { family: "Inter", weight: "600" } },
                    },
                },
            },
        });
    }
}
