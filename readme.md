# Video Motion Detection & Blurring System

This project detects motion in a video, applies blurring to detected areas, and saves the processed video.

## 📌 Features
- Reads video frames (`Streamer`).
- Detects motion (`Detector`).
- Applies blurring to moving objects (`Displayer`).
- Saves the final processed video.

---

## 🚀 Installation

   ```sh
   git clone https://github.com/asaf919/solu.git
   cd solu
   python3.12 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
**Note**: This project was tested on **Python 3.12**.

---

## ▶️ Running the Program

This project includes **two main execution modes**:

1. **Multithreaded Mode (`main.py`)** – Runs all components in parallel for better performance.
2. **Sequential Mode (`main_seq.py`)** – Runs components **one by one**, making it easier to debug.

Both modes **print logs to the console** and **store logs in the `debug_output/` directory** for later analysis.

---

### **1️⃣ Running the Multithreaded Version**
   ```sh
   python main.py --input_video <path_to_input_video>
   ```

- output is stored as an output.mp4 file in the root directory.

---

### **2️⃣ Running the Sequential Version**
   ```sh
   python main_seq.py --input_video <path_to_input_video>
   ```

- output is stored as an output.mp4 file in the root directory.

---

## ✅ Running Tests (Currently Disabled)

> ⚠️ **Due to technical issues, the tests are currently not working and have been commented out.**