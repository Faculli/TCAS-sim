# ✈️ ATC Radar & TCAS Simulation Engine

A 2D Air Traffic Control (ATC) simulation engine written in Python. The system simulates realistic aircraft kinematics, multi-aircraft radar conflict detection, and an automated Traffic Collision Avoidance System (TCAS) designed to resolve airborne conflicts in real time.

---

## 📌 Project Overview

This project simulates airspace operations where multiple aircraft navigate simultaneously. It features a conflict detection algorithm based on real-world aviation separation standards ($5.0\text{ NM}$ horizontal and $1,000\text{ ft}$ vertical), a critical midair-collision threshold ($0.5\text{ NM}$ horizontal and $200\text{ ft}$ vertical) that freezes the scene on impact, and visually represents aircraft telemetry via a 2D ATC radar console interface.

---

## ✨ Features Implemented

- [x] **Modular Object-Oriented Architecture**: Clean separation between entity models (`Aircraft`, `Position`), services (`Radar`, `TCASControl`, `Simulator`), and visualization (`RadarView`).
- [x] **Kinematics & Physics Engine**: Accurate position updating using trigonometric vector analysis, converted airspeed (knots to NM/s), and climb/descent rates (ft/s).
- [x] **Radar Conflict Detection**: Real-time detection of loss of separation between aircraft pairs using Euclidean distance formulas for horizontal and vertical airspace parameters.
- [x] **Midair Collision Detection & Simulation Freeze**: A critical proximity threshold ($< 0.5\text{ NM}$ horizontal and $< 200\text{ ft}$ vertical) flags an actual midair collision, logs it to the console, and puts the simulation into a permanent frozen (resting) state.
- [x] **Basic Vertical TCAS Resolution**: Automatic resolution advisory (RA) that issues climb/descent orders to conflicting aircraft pairs.
- [x] **Realistic 2D ATC Radar Console (`Pygame`)**:
  - Distance range rings ($10\text{ NM}$ increments).
  - Dynamic aircraft blips with direction and velocity vector lines.
  - Real-time 3-line flight data blocks (Callsign, Flight Level with climb/descent trend indicators `▲`/`▼`/`═`, and Airspeed/Vertical Speed).
  - Visual conflict warnings (blips and data blocks turn red upon TCAS alert).
  - Midair collision state: all other traffic is hidden and the colliding pair is greyed out, freezing the scene at the moment of impact.
- [x] **Configurable Parameters**: Parameterized configuration module for global simulation variables.

---

## 🚀 Installation & Usage

### Prerequisites
- Python 3.10+
- Virtual environment (`venv`) recommended

---

### Setup

1. Clone the repository:

        git clone https://github.com/your-username/atc-radar-simulator.git
        cd atc-radar-simulator

2. Create and activate a virtual environment:

        For Windows:
        python -m venv venv
        venv\Scripts\activate

        For Linux / macOS:
        python3 -m venv venv
        source venv/bin/activate

3. Install dependencies:

        pip install -r requirements.txt

4. Run the simulation:

        python main.py

---

## 🗺️ Roadmap & Future Enhancements

The following tasks and features are currently planned or under development:

### 🔴 Critical Features (In Progress / Next Steps)

- [ ] **Continuous Collision Detection via Closest Point of Approach (CPA)**:
  - Replace the discrete per-frame distance sampling with a CPA calculation that finds the minimum distance *within* each time step.
  - Prevents fast-closing aircraft from "tunnelling" through the narrow $0.5\text{ NM}$ collision window between frames, making the midair-collision trigger reliable regardless of speed or update rate.

- [ ] **Advanced Multi-Directional TCAS Logic (Horizontal & Combined Evasion)**:
  - Upgrade `ATCControl` to evaluate surrounding airspace before issuing commands.
  - Implement **Lateral/Horizontal Evasion**: Issue heading vector turns ($15^\circ$ to $45^\circ$) when vertical separation is blocked by traffic in adjacent flight levels.
  - Implement **Combined Evasion**: Simultaneous heading and altitude adjustments for dense traffic scenarios.

- [ ] **Interactive In-App Pygame Menu**:
  - Build an interactive GUI overlay/sidepanel within Pygame to modify parameters during runtime or setup:
    - Adjust aircraft population count dynamically.
    - Modify simulation speed (time multiplier: $1x$, $2x$, $5x$).
    - Toggle radar range ($30\text{ NM}$, $60\text{ NM}$, $120\text{ NM}$).
    - Manually spawn aircraft or inject custom conflict scenarios.

### 🟡 Proposed Future Improvements

- [ ] **TCAS Domino-Effect Prevention**: Predictive look-ahead logic to prevent a climbing/descending aircraft from initiating a secondary conflict with a third aircraft above or below.
- [ ] **Flight Plan & Waypoint Navigation**: Enable aircraft to follow fixed flight paths and waypoints rather than flying fixed headings endlessly.
- [ ] **Telemetry Data Logging & Metrics Export**: Export post-simulation performance reports (CSV/JSON) detailing total flight hours, number of conflicts detected, TCAS intervention counts, and average resolution time.
- [ ] **Sound Effects & Audio Alerts**: Add auditory TCAS alerts ("Traffic, Traffic", "Climb, Climb") using `pygame.mixer`.

---

## 🛠️ Tech Stack

- **Language:** Python 3
- **GUI & Graphics:** Pygame (2D Radar Console)
- **Math & Kinematics:** Built-in `math` module

---

## 📄 License

This project is open-source under the MIT License.