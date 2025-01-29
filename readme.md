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