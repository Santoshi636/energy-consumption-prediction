let fullData = [];
let lineChart;
let barChart;

// Load CSV
fetch("predictions.csv")
    .then(res => res.text())
    .then(data => {
        const rows = data.split("\n").slice(1);

        rows.forEach(row => {
            const cols = row.split(",");
            if (cols.length < 3) return;

            const datetime = cols[0];
            const actual = parseFloat(cols[1]);
            const predicted = parseFloat(cols[2]);

            if (isNaN(actual) || isNaN(predicted)) return;

            const hour = new Date(datetime).getHours();
            fullData.push({ datetime, actual, predicted, hour });
        });

        populateDropdown();
        updateCharts("all");
    });

// Populate dropdown
function populateDropdown() {
    const select = document.getElementById("hourFilter");
    for (let i = 0; i < 24; i++) {
        const option = document.createElement("option");
        option.value = i;
        option.text = i + ":00";
        select.appendChild(option);
    }

    select.addEventListener("change", () => {
        updateCharts(select.value);
    });
}

// Update charts
function updateCharts(selectedHour) {
    let filtered = fullData;

    if (selectedHour !== "all") {
        filtered = fullData.filter(d => d.hour == selectedHour);
    }

    drawLineChart(filtered);
    drawBarChart(filtered);
}

// Line Chart
function drawLineChart(data) {
    const ctx = document.getElementById("lineChart").getContext("2d");
    if (lineChart) lineChart.destroy();

    lineChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: data.slice(0, 50).map(d => d.datetime),
            datasets: [
                {
                    label: "Actual",
                    data: data.slice(0, 50).map(d => d.actual),
                    borderWidth: 2,
                    fill: false
                },
                {
                    label: "Predicted",
                    data: data.slice(0, 50).map(d => d.predicted),
                    borderWidth: 2,
                    fill: false
                }
            ]
        }
    });
}

// Bar Chart
function drawBarChart(data) {
    const ctx = document.getElementById("barChart").getContext("2d");
    if (barChart) barChart.destroy();

    const hourlySum = new Array(24).fill(0);
    const hourlyCount = new Array(24).fill(0);

    data.forEach(d => {
        hourlySum[d.hour] += d.actual;
        hourlyCount[d.hour] += 1;
    });

    const hourlyAvg = hourlySum.map((sum, i) =>
        hourlyCount[i] ? sum / hourlyCount[i] : 0
    );

    barChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: [...Array(24).keys()],
            datasets: [
                {
                    label: "Average Energy Consumption",
                    data: hourlyAvg,
                    borderWidth: 1
                }
            ]
        }
    });
}
