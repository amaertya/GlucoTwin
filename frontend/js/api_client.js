const API_BASE = "http://127.0.0.1:8000";

export async function checkApiHealth() {
    try {
        const res = await fetch(`${API_BASE}/api/health`);
        return await res.json();
    } catch (e) {
        return { status: "offline", model_loaded: false };
    }
}

export async function fetchPatients() {
    const res = await fetch(`${API_BASE}/api/patients`);
    const data = await res.json();
    return data.patients;
}

export async function fetchPatientObservations(patientId) {
    const res = await fetch(`${API_BASE}/api/patients/${patientId}/observations?limit=40`);
    const data = await res.json();
    return data.observations;
}

export async function postPrediction(payload) {
    const res = await fetch(`${API_BASE}/api/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });
    return await res.json();
}

export async function postScenario(payload) {
    const res = await fetch(`${API_BASE}/api/scenario`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });
    return await res.json();
}

export async function fetchModelMetrics() {
    const res = await fetch(`${API_BASE}/api/model/metrics`);
    return await res.json();
}