# 🗂️ GCP File Upload Notifier using Cloud Run, Cloud Storage, Pub/Sub & Eventarc

This project sets up an automated serverless pipeline on **Google Cloud Platform (GCP)** to **detect when a file is uploaded to a Cloud Storage bucket** and then log details about the uploaded file using a **Cloud Run service**.

---

## 📌 Use Case

When a file is uploaded to a bucket named `tyty08`, the event is captured by Eventarc and sent to a custom **Cloud Run service**. This service logs details about the uploaded file such as:

- File name
- Bucket name
- File generation ID
- Media download URL

---

## 🧱 Architecture Overview

📁 Upload → ⚡ Eventarc → 📬 Pub/Sub → 🚀 Cloud Run → 📝 Logging

