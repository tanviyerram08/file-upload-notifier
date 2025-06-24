 🗂️ File Upload Notifier using GCP

This project demonstrates a serverless event-driven architecture on Google Cloud Platform (GCP) that logs file upload events to a bucket using Cloud Run triggered by Cloud Storage via Eventarc.


 📌 Use Case

When a file is uploaded to a bucket named `tyty08`, the event is captured by Eventarc and sent to a custom **Cloud Run service**. This service logs details about the uploaded file such as:

- File name
- Bucket name
- File generation ID
- Media download URL

 🧱 Architecture Overview

📁 Upload → ⚡ Eventarc → 📬 Pub/Sub → 🚀 Cloud Run → 📝 Logging

User → uploads file to → Cloud Storage bucket
            ↓
        Eventarc detects "finalize" event
            ↓
      Publishes event to Cloud Run service
            ↓
    Cloud Run logs event details to stdout

🛠️ GCP Services Used

 Service                  Role                                                               
 Cloud Storage (GCS):  File storage. Triggers event on new file uploads.                 
 Eventarc:             Routes storage events to Cloud Run via CloudEvents.               
 Cloud Run:            Containerized service that receives events and logs file info.    
 Pub/Sub:              Used by Eventarc under the hood) for event transport.             
 IAM:                  Service accounts and roles to allow Eventarc to trigger Cloud Run.

 📁 Project Structure

 file-upload-notifier/
├── main.py                  # Flask app to log incoming events
├── Dockerfile               # Container definition
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
└── docs/
    └── architectural diagram.jpg  # Visual flow

🚀 Deployment Steps
1. Enable GCP Services
gcloud services enable run.googleapis.com eventarc.googleapis.com pubsub.googleapis.com storage.googleapis.com
2. Create Storage Bucket
gsutil mb -l asia-south1 gs://your-bucket-name
3. Build and Push Docker Image
gcloud builds submit --tag gcr.io/PROJECT-ID/file-logger
4. Deploy to Cloud Run
   gcloud run deploy file-logger \
  --image gcr.io/PROJECT-ID/file-logger \
  --region asia-south1 \
  --platform managed \
  --allow-unauthenticated
5. Grant Permissions to GCS Event Publisher
   PROJECT_NUM=$(gcloud projects describe PROJECT-ID --format='value(projectNumber)')
gcloud projects add-iam-policy-binding PROJECT-ID \
  --member="serviceAccount:service-${PROJECT_NUM}@gs-project-accounts.iam.gserviceaccount.com" \
  --role='roles/pubsub.publisher'
6. Create Eventarc Trigger
gcloud eventarc triggers create file-upload-trigger \
  --location=asia-south1 \
  --destination-run-service=file-logger \
  --destination-run-region=asia-south1 \
  --event-filters="type=google.cloud.storage.object.v1.finalized" \
  --event-filters="bucket=your-bucket-name" \
  --service-account=PROJECT-NUMBER-compute@developer.gserviceaccount.com

 ✅ Test the Setup
 echo "Hello Eventarc" > test.txt
gsutil cp test.txt gs://your-bucket-name/
View Logs: gcloud logging read "resource.labels.service_name=file-logger" --limit 10 --format="value(textPayload)"

Expected logs will include:
File name
Bucket
Self-link
Media link
Generation ID

📌 Key Learnings
GCP's Eventarc provides a seamless way to connect storage events to serverless containers.
Cloud Run makes it easy to host lightweight logging microservices.
The combination allows fully managed, cost-efficient backend automation.

👤 Author
Tanvi Yerram
GitHub: @tanviyerram08






