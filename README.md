# Satellite Crash Predictor

A web app that estimates collision risk between two orbiting objects
using simplified conjunction assessment logic.

Built as a portfolio project to demonstrate full-stack development
with Python, Flask, and vanilla JavaScript.

> **Disclaimer:** This is a heuristic scoring tool for educational
> purposes only. It does not use real orbital propagation, live
> satellite data, or physics-based probability-of-collision math.

---

## Features

- Estimates collision risk as Low / Medium / High
- Recommends action: Monitor / Prepare maneuver / Immediate maneuver
- Explains why a risk level was assigned in plain English
- Time-to-closest-approach can escalate recommended action
- Animated starfield UI with live score bar

---

## Tech Stack

- Python 3
- Flask
- Vanilla HTML / CSS / JavaScript

---

## How to Run

1. Clone the repository
2. Install dependencies:
```
   pip install flask
```
3. Run the app:
```
   python app.py
```
4. Open your browser and go to:
```
   http://localhost:5000
```

---

## Inputs

| Field | Description |
|---|---|
| Altitude of Object 1 | Orbital altitude in km |
| Altitude of Object 2 | Orbital altitude in km |
| Relative Velocity | Velocity at closest approach (km/s) |
| Miss Distance | Predicted miss distance (km) |
| Object Size Category | Debris / CubeSat / Large Satellite |
| Time to Closest Approach | Hours until closest approach |

---

## Risk Scoring Logic

Scores are calculated out of 100 across three factors:

| Factor | Max Points |
|---|---|
| Miss Distance | 50 |
| Relative Velocity | 30 |
| Object Size | 20 |

Risk levels:
- **Low** — 0 to 39
- **Medium** — 40 to 69
- **High** — 70 to 100

Time to closest approach does not affect the score but can
escalate the recommended action if the window is short.

---

## Project Structure

```
satellite-crash-predictor/
├── app.py              # Flask server
├── risk_logic.py       # Scoring logic
├── templates/
│   └── index.html      # UI layout
└── static/
    ├── style.css        # Styling
    └── script.js        # Starfield + fetch logic
```

---

*Developed by B R Devamayookha — AI & Data Science, Sona College of Technology*