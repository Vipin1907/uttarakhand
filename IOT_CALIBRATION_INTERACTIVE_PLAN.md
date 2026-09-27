# Trinetra AI — Interactive IoT Raw ADC Calibration & Jury Presentation Blueprint

## 📌 Document Overview & Purpose

This document logs the architectural design, calibration equations, interactive 3-step UI workflow, and jury defense strategy for the **Trinetra AI Cyber-Physical IoT Ingestion Engine**.

---

## 🎯 1. System Philosophy: Technical Honesty & Raw-to-Calibrated Pipeline

To ensure 100% credibility during SIH / Hackathon evaluation and eliminate "black box AI" skepticism:

1. **State 0 (Raw Telemetry)**: The system first displays uncalibrated, raw hardware signals directly from the ESP32 microcontroller pins as **ADC Integers ($0 - 4095$)**.
2. **State 1 (Physics Scaling Engine)**: Upon clicking **`[ ⚡ Apply Physics Calibration Engine ]`**, the system executes hydrological physics formulas live on screen, scaling raw ADC values into standardized physical metrics ($mm$, $m$, $\%$).
3. **State 2 (ML Risk Inference)**: Upon clicking **`[ 🧠 Run ML Flood Risk Prediction ]`**, calibrated metrics feed into the trained XGBoost model and TreeSHAP explainability engine.

```
+-----------------------------+     +-----------------------------------+     +-----------------------------------+
|  STEP 1: RAW HARDWARE ADC   | ──> | STEP 2: PHYSICS CALIBRATION       | ──> | STEP 3: XGBOOST ML PREDICTION     |
|  Rain ADC: 450              |     | Rain Index: 88% (281.6 mm)        |     | Flood Risk Score: 94.2%           |
|  River ADC: 3400            |     | River Gauge: 20.45m (+0.45m)      |     | Danger Category: HIGH (RED)       |
|  Soil ADC: 380              |     | Soil Saturation: 92%              |     | Safe Route & Shelter Allocated    |
+-----------------------------+     +-----------------------------------+     +-----------------------------------+
```

---

## 📐 2. Calibration Equations & Mathematical Scaling

The ESP32 microcontroller analog-to-digital converter (ADC) operates at **12-bit resolution ($0 - 4095$)**.

### A. Surface Raindrop Sensor (`GPIO 34` / ADC1_34)
* **Raw Signal Behavior**: Dry ($\approx 4095$) $\longrightarrow$ Saturated Wet ($\approx 400$).
* **Normalized Wetness Index**:
  $$\text{Wetness} = \max\left(0.0, \min\left(1.0, \frac{4095 - \text{ADC}_{34}}{3600}\right)\right)$$
* **Physical Equivalents**:
  $$\text{Rain}_{\%} = \text{Wetness} \times 100\%$$
  $$R_{3d} = \text{Wetness} \times 320.0\text{ mm}$$
  $$R_{1h} = \text{Wetness} \times 35.0\text{ mm/h}$$

### B. River Level Probe (`GPIO 35` / ADC1_35)
* **Raw Signal Behavior**: Air/Baseline ($\approx 300$) $\longrightarrow$ Fully Submerged ($\approx 3500$).
* **Submerged Ratio**:
  $$\text{SubmergedPct} = \max\left(0.0, \min\left(1.0, \frac{\text{ADC}_{35} - 300}{3200}\right)\right)$$
* **Physical Gauge Metrics**:
  $$H = 20.0\text{ m} + (\text{SubmergedPct} - 0.40) \times 1.60\text{ m}$$
  $$Q = 220 + (\text{SubmergedPct} \times 1400)\text{ m}^3/\text{s}$$

### C. Soil Hygrometer (`GPIO 32` / ADC1_32)
* **Raw Signal Behavior**: Dry Soil ($\approx 4095$) $\longrightarrow$ Saturated Soil ($\approx 400$).
* **Soil Saturation Percentage**:
  $$\text{Soil}_{\%} = \min\left(98.0\%, 35.0\% + \left(\frac{4095 - \text{ADC}_{32}}{3200}\right) \times 62.0\%\right)$$

---

## 🖥️ 3. UI Presentation Flow & Visual FX

1. **Step-by-Step Action Bar**:
   - `[ 🔌 1. Connect / View Raw ADC ]`
   - `[ ⚡ 2. Apply Calibration Engine ]`
   - `[ 🧠 3. Predict Flood Risk ]`
2. **Glowing Pulse Animation**:
   - When **Apply Calibration** is pressed, formula boxes on cards flash with a subtle green highlight to draw the jury's attention to the live conversion math.
3. **Emergency Hardware Safeguard**:
   - A toggle switch `[ 🛰️ Hardware Wi-Fi/USB Live | 🎛️ Manual Preset Sliders ]` allows manual demonstration using presets (*Dry Baseline*, *Moderate Spray*, *Flash Flood Surge*) if physical hardware loses power/connection during the live pitch.

---

## 🛡️ 4. Jury Defense Script & Cross-Question Responses

### Q1: "Screen par ye raw ADC aur formulas kyu dikh rahe hain?"
> **Response**: *"Sir/Ma'am, humari design philosophy 'Technical Transparency' hai. Screen par pehle ESP32 ka raw 12-bit ADC integer (0-4095) dikhta hai. Jab hum Calibration Engine run karte hain, to background hydrology formulas raw ADC ko real physical parameters (mm, metres, %) me convert karte hain."*

### Q2: "Low-cost 2-inch sensor real 300 mm rainfall volume kaise bata sakta hai?"
> **Response**: *"Sir, low-cost sensors physical volume nahi, surface wetness aur electrical resistance measure karte hain. Humne ise UI par explicitly 'Simulated Precipitation Equivalent Index' label kiya hai taaki technical accuracy bani rahe."*

### Q3: "Agar Satellite Forecast Dry dikhaye aur IoT Sensor Flood surge detect kare, tab system kya karega?"
> **Response**: *"Humara Multi-Source Comparison Mode dono data streams ko compare karta hai. Discrepancy detect hote hi Agentic AI supervisor local cloudburst ya dam release recognize karke immediately Local Emergency Warning dispatch kar deta hai."*

---

## 📅 Log Metadata
* **Created Date**: 2026-09-26
* **Status**: Logged & Verified (Awaiting User Implementation Signal)
* **Target System**: Trinetra AI Dashboard (`index.html`, `app.js`, `main.py`)
