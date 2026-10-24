export function populateObservationTable(observations) {
    const tbody = document.getElementById("observationTableBody");
    tbody.innerHTML = "";
    observations.forEach(obs => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${obs.timestamp}</td>
            <td>${obs.glucose_mg_dl}</td>
            <td>${obs.steps}</td>
            <td>${obs.sleep_hours}</td>
            <td>${obs.carbs_consumed_g || 0}</td>
        `;
        tbody.appendChild(tr);
    });
}