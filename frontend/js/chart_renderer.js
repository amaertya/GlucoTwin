let overviewChartInstance = null;
let wearableChartInstance = null;
let simulationChartInstance = null;

export function renderOverviewChart(labels, data) {
    const ctx = document.getElementById("overviewChart").getContext("2d");
    if (overviewChartInstance) overviewChartInstance.destroy();
    
    overviewChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Glucose (mg/dL)',
                data: data,
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { grid: { color: '#334155' }, ticks: { color: '#94a3b8' } },
                x: { grid: { color: '#334155' }, ticks: { color: '#94a3b8', maxTicksLimit: 8 } }
            },
            plugins: { legend: { labels: { color: '#f8fafc' } } }
        }
    });
}

export function renderWearableChart(labels, stepsData) {
    const ctx = document.getElementById("wearableChart").getContext("2d");
    if (wearableChartInstance) wearableChartInstance.destroy();
    
    wearableChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Steps / Activity',
                data: stepsData,
                backgroundColor: '#10b981',
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { grid: { color: '#334155' }, ticks: { color: '#94a3b8' } },
                x: { grid: { color: '#334155' }, ticks: { color: '#94a3b8', maxTicksLimit: 6 } }
            },
            plugins: { legend: { labels: { color: '#f8fafc' } } }
        }
    });
}

export function renderSimulationChart(labels, baselineData, scenarioData) {
    const ctx = document.getElementById("simulationChart").getContext("2d");
    if (simulationChartInstance) simulationChartInstance.destroy();
    
    simulationChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Baseline Forecast',
                    data: baselineData,
                    borderColor: '#94a3b8',
                    borderDash: [5, 5],
                    borderWidth: 2,
                    tension: 0.2
                },
                {
                    label: 'Scenario Counterfactual',
                    data: scenarioData,
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { grid: { color: '#334155' }, ticks: { color: '#94a3b8' } },
                x: { grid: { color: '#334155' }, ticks: { color: '#94a3b8' } }
            },
            plugins: { legend: { labels: { color: '#f8fafc' } } }
        }
    });
}