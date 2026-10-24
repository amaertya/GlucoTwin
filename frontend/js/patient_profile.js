export function renderPatientProfileDetails(patient) {
    const container = document.getElementById("patientProfileDetails");
    container.innerHTML = `
        <p><strong>Patient ID:</strong> ${patient.patient_id}</p>
        <p><strong>Age:</strong> ${patient.age}</p>
        <p><strong>Gender:</strong> ${patient.gender}</p>
        <p><strong>BMI:</strong> ${patient.bmi}</p>
        <p><strong>HbA1c:</strong> ${patient.hba1c}%</p>
        <p><strong>Diabetes Type:</strong> ${patient.diabetes_type}</p>
        <p><strong>Insulin Sensitivity Index:</strong> ${patient.baseline_insulin_sensitivity}</p>
    `;
}