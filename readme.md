# Video Motion Detection & Blurring System

This project detects motion in a video, applies blurring to detected areas, and saves the processed video.

## 📌 Features
- Reads video frames (`Streamer`).
- Detects motion (`Detector`).
- Applies blurring to moving objects (`Displayer`).
- Saves the final processed video.

---

## 🚀 Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/asaf919/solu.git
   cd solu
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
    ```
   
---


## ▶️ Running the Program

This project includes **two main execution modes**:

1. **Multithreaded Mode (`main.py`)** – Runs all components in parallel for better performance.
2. **Sequential Mode (`main_seq.py`)** – Runs components **one by one**, making it easier to debug.

Both modes **print logs to the console** and **store logs in the `debug_output/` directory** for later analysis.

---

### **1️⃣ Running the Multithreaded Version**
   ```sh
   python main.py
   ```

---


### **2️⃣ Running the Sequential Version**
   ```sh
   python main_seq.py
   ```

--- 