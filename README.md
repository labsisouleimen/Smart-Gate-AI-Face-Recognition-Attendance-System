# 🛡️ FaceGuard-Pro: Low-Resource Biometric Access Control
> **High-speed facial recognition system using FaceNet, optimized for real-time performance on low-spec hardware (CPU optimized).**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![FaceNet](https://img.shields.io/badge/Model-FaceNet-blueviolet?style=for-the-badge)
![Security](https://img.shields.io/badge/Security-Biometric_Auth-red?style=for-the-badge)
![Optimization](https://img.shields.io/badge/Hardware-CPU_Optimized-green?style=for-the-badge)

---
<img src="https://github.com/labsisouleimen/Smart-Gate-AI-Face-Recognition-Attendance-System/blob/main/image.png?raw=true" width="350">
---

## 🚀 Overview
FaceGuard-Pro is an advanced biometric security solution designed for government buildings, airports, and universities. It replaces traditional ID cards with a high-accuracy facial recognition engine. 

**The standout feature of this project is its efficiency; it delivers lightning-fast recognition even on standard office PCs with weak processors, without requiring a dedicated GPU.**

---

## ✨ Key Features
* **CPU-Friendly:** Highly optimized feature extraction using FaceNet embeddings, making it perfect for low-resource environments.
* **Instant Verification:** Millisecond-level matching against large databases.
* **Universal Camera Integration:** Works with any standard USB webcam or IP-based CCTV system.
* **Privacy Focused:** The system does not store images; it converts faces into encrypted 128-d/512-d numerical embeddings.
* **Secure Access Logs:** Automatic logging of entry/exit times with identity verification.

---
## 📸 System Showcase

| Feature | Interface Preview | Technical Description |
| :--- | :---: | :--- |
| **Real-time Recognition** | <img src="https://raw.githubusercontent.com/labsisouleimen/Smart-Gate-AI-Face-Recognition-Attendance-System/1e528c8b24df34bbe8d0c27cb938126b41ca0b15/image.png" width="350"> | Detecting and identifying faces instantly from a live camera stream. |
| **Enrollment System** | <img src="https://raw.githubusercontent.com/labsisouleimen/Smart-Gate-AI-Face-Recognition-Attendance-System/ff504f572f0ccbd5a701572729ad30118e2efe0b/image.png" width="350"> | High-speed facial registration to the encrypted biometric database. |
| **Activity Reports** | <img src="https://raw.githubusercontent.com/labsisouleimen/Smart-Gate-AI-Face-Recognition-Attendance-System/6ae4d9e5df1f74b4e02708c526a159889a8ebaa9/image.png" width="350"> | Detailed access logs for security audits and attendance tracking. |

---

## ⚙️ Model Download
Due to GitHub's file size limits, the pre-trained FaceNet model is hosted externally.
1. **[Download the FaceNet Model Here](رابط_التحميل_الخاص_بك)**
2. Place the downloaded file inside the `/models` directory of this project.

---

## 🛠️ Technical Implementation
* **Face Localization:** MTCNN / Haar Cascades.
* **Feature Extraction:** FaceNet (Inception ResNet v1).
* **Optimization:** Image resizing and grayscale pre-processing to maintain high FPS on weak CPUs.
* **Database:** Secure local storage of identity embeddings.

---

## 🚀 Quick Start
1. **Clone the Repo:**
   ```bash
   git clone [https://github.com/labsisouleimen/FaceGuard-Pro.git](https://github.com/labsisouleimen/FaceGuard-Pro.git)

---

## 🔒 Privacy & Security Note
Identity data is stored as mathematical vectors (embeddings). Even if the database is accessed, the original 
faces cannot be reconstructed, providing a high layer of security and privacy compliance.

---

## 📩 Contact
Developed by Souleimen Labsi
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/souleimen-labsi-5937783ab/)
