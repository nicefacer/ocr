import os
from google.cloud import vision
from google.cloud import storage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set up authentication
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'vision_key.json'

# Initialize Google Cloud clients
vision_client = vision.ImageAnnotatorClient()
storage_client = storage.Client()
docs_client = build('docs', 'v1')

def detect_text_gcs(bucket_name, prefix):
    """Detects text in images stored in a GCS bucket."""
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix)
    
    extracted_texts = {}
    for blob in blobs:
        if not blob.name.endswith(('.jpg', '.png', '.jpeg', '.gif', '.bmp', '.tiff')):
            continue  # Skip non-image files
        
        image = vision.Image(source=vision.ImageSource(image_uri=f"gs://{bucket_name}/{blob.name}"))
        response = vision_client.text_detection(
            image=image,
            image_context={"language_hints": ["zh", "ja"]}  # Hints for Chinese and Japanese
        )
        if response.error.message:
            print(f"Error processing {blob.name}: {response.error.message}")
            extracted_texts[blob.name] = None
            continue

        # Extract and store OCR text
        texts = response.text_annotations
        if texts:
            extracted_texts[blob.name] = texts[0].description
        else:
            extracted_texts[blob.name] = "No text detected"

    return extracted_texts

def save_to_google_doc(texts, doc_title="OCR Results"):
    """Saves OCR results to a Google Doc."""
    doc_content = "\n\n".join([f"{file}:\n{text}" for file, text in texts.items()])
    
    try:
        # Create a new document
        doc = docs_client.documents().create(body={"title": doc_title}).execute()
        document_id = doc['documentId']
        
        # Add text to the document
        requests = [{"insertText": {"location": {"index": 1}, "text": doc_content}}]
        docs_client.documents().batchUpdate(
            documentId=document_id,
            body={"requests": requests}
        ).execute()
        
        print(f"OCR results saved to Google Doc: https://docs.google.com/document/d/{document_id}")
    except HttpError as e:
        print(f"An error occurred: {e}")

def main(bucket_name, prefix):
    """Main entry point for the OCR script."""
    print("Starting OCR process...")
    texts = detect_text_gcs(bucket_name, prefix)
    save_to_google_doc(texts)
    return texts

if __name__ == "__main__":
    bucket_name = "librarybookz"
    prefix = "sample/"  # Adjust if your images are in a nested folder structure within the bucket
    
    main(bucket_name, prefix)
