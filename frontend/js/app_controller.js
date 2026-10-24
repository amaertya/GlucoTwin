import { checkApiHealth, fetchPatients, fetchPatientObservations, postPrediction, fetchModelMetrics } from "./api_client.js";
import { renderOverviewChart, renderWearableChart } from "./chart_renderer.js";
import { renderPatientProfileDetails } from "./patient_profile.js";
import { initSimulationLab } from "./simulation_lab.js";
import { populateObservationTable } from "./ui_utils.js";

let activePatientId = null;
let latestObservations = [];
let currentGlucoseValue = 140.0;

async function initGlucoTwinApp() {
    const health = await checkApiHealth();
    const badge = document.getElementById("apiStatusBadge");
    const sysConn = document.getElementById("sysConnection");
    const sysModel = document.getElementById("sysModelStatus");
    
    if (health.status === "healthy") {
        badge.className = "status-indicator online";
        badge.innerText = "API Online";
        sysConn.innerText = "Connected (OK)";
        sysModel.innerText = health.model_loaded ? "Loaded (Random Forest)" : "Not Loaded";
    } else {
        badge.className = "status-indicator offline";
        badge.innerText = "API Offline";
        sysConn.innerText = "Disconnected - Start FastAPI Backend";
        sysModel.innerText = "Unavailable";
    }

    const patients = await fetchPatients();
    const select = document.getElementById("globalPatientSelect");
    select.innerHTML = "";
    patients.forEach(p => {
        const opt = document.createElement("option");
        opt.value = p.patient_id;
        opt.innerText = `${p.patient_id} (Age: ${p.age}, HbA1c: ${p.hba1c}%)`;
        select.appendChild(opt);
    });

    if (patients.length > 0) {
        activePatientId = patients[0].patient_id;
        select.value = activePatientId;
        renderPatientData(activePatientId);
    }

    select.onchange = (e) => {
        activePatientId = e.target.value;
        renderPatientData(activePatientId);
    };

    document.querySelectorAll(".nav-item").forEach(item => {
        item.onclick = (e) => {
            document.querySelectorAll(".nav-item").forEach(i => i.classList.remove("active"));
            document.querySelectorAll(".content-section").forEach(s => s.classList.remove("active"));
            
            e.target.classList.add("active");
            const targetId = e.target.getAttribute("data-target");
            document.getElementById(targetId).classList.add("active");
            document.getElementById("pageTitle").innerText = e.target.innerText;
        };
    });

    document.getElementById("triggerPredictionBtn").onclick = async () => {
        const recentGl = latestObservations.slice(-5).map(o => o.glucose_mg_dl);
        while(recentGl.length < 5) recentGl.unshift(140.0);
        
        const payload = {
            patient_id: activePatientId,
            recent_glucose: recentGl,
            current_steps: 120,
            current_sleep: 7.5
        };
        const res = await postPrediction(payload);
        document.getElementById("predValueDisplay").innerText = `${res.predicted_glucose_30min} mg/dL`;
        document.getElementById("predCiDisplay").innerText = `[${res.confidence_interval[0]} - ${res.confidence_interval[1]}] mg/dL`;
        document.getElementById("predModelDisplay").innerText = res.model_version;
    };

    const metrics = await fetchModelMetrics();
    if (metrics.mae) {
        document.getElementById("metricMae").innerText = metrics.mae;
        document.getElementById("metricRmse").innerText = metrics.rmse;
        document.getElementById("metricR2").innerText = metrics.r2_score;
        document.getElementById("metricBaseMae").innerText = metrics.persistence_baseline_mae;
        document.getElementById("metricNote").innerText = metrics.note;
    }
}

async function renderPatientData(patientId) {
    const patients = await fetchPatients();
    const patient = patients.find(p => p.patient_id === patientId);
    if (patient) {
        renderPatientProfileDetails(patient);
        document.getElementById("overviewHbA1c").innerText = `${patient.hba1c}%`;
        document.getElementById("overviewBmi").innerText = `BMI: ${patient.bmi}`;
    }

    latestObservations = await fetchPatientObservations(patientId);
    if (latestObservations.length > 0) {
        const last = latestObservations[latestObservations.length - 1];
        currentGlucoseValue = last.glucose_mg_dl;
        document.getElementById("overviewCurrentGlucose").innerText = `${currentGlucoseValue} mg/dL`;
        document.getElementById("overviewTimestamp").innerText = last.timestamp;
        
        const labels = latestObservations.map(o => o.timestamp.split(" ")[1]);
        const glucoseData = latestObservations.map(o => o.glucose_mg_dl);
        const stepsData = latestObservations.map(o => o.steps);
        
        renderOverviewChart(labels, glucoseData);
        renderWearableChart(labels, stepsData);
        populateObservationTable(latestObservations);
        
        initSimulationLab(patientId, currentGlucoseValue);
        
        document.getElementById("predValueDisplay").innerText = `${(currentGlucoseValue * 1.01).toFixed(1)} mg/dL`;
        document.getElementById("overviewForecast").innerText = `${(currentGlucoseValue * 1.01).toFixed(1)} mg/dL`;
    }
}

window.onload = initGlucoTwinApp;