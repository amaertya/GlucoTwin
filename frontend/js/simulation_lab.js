import { postScenario } from "./api_client.js";
import { renderSimulationChart } from "./chart_renderer.js";

export function initSimulationLab(currentPatientId, currentGlucose) {
    const carbsSlider = document.getElementById("simCarbs");
    const activitySlider = document.getElementById("simActivity");
    const sleepSlider = document.getElementById("simSleep");
    
    document.getElementById("carbsVal").innerText = carbsSlider.value;
    document.getElementById("activityVal").innerText = activitySlider.value;
    document.getElementById("sleepVal").innerText = sleepSlider.value;

    carbsSlider.oninput = () => document.getElementById("carbsVal").innerText = carbsSlider.value;
    activitySlider.oninput = () => document.getElementById("activityVal").innerText = activitySlider.value;
    sleepSlider.oninput = () => document.getElementById("sleepVal").innerText = sleepSlider.value;

    document.getElementById("runSimulationBtn").onclick = async () => {
        const payload = {
            patient_id: currentPatientId,
            baseline_glucose: currentGlucose,
            delta_carbs_g: parseFloat(carbsSlider.value),
            delta_activity_minutes: parseFloat(activitySlider.value),
            delta_sleep_hours: parseFloat(sleepSlider.value)
        };
        
        const res = await postScenario(payload);
        document.getElementById("simExplanation").innerText = res.explanation;
        
        const labels = ["T (Now)", "T + 15m", "T + 30m (Counterfactual)"];
        const baselineArr = [currentGlucose, currentGlucose, res.baseline_forecast];
        const scenarioArr = [currentGlucose, currentGlucose + (res.scenario_forecast - currentGlucose)*0.5, res.scenario_forecast];
        
        renderSimulationChart(labels, baselineArr, scenarioArr);
    };

    document.getElementById("resetSimulationBtn").onclick = () => {
        carbsSlider.value = 50;
        activitySlider.value = 30;
        sleepSlider.value = 7.5;
        document.getElementById("carbsVal").innerText = "50";
        document.getElementById("activityVal").innerText = "30";
        document.getElementById("sleepVal").innerText = "7.5";
        document.getElementById("simExplanation").innerText = "Simulation reset to baseline.";
        renderSimulationChart(["T (Now)", "T + 30m"], [currentGlucose, currentGlucose], [currentGlucose, currentGlucose]);
    };
}