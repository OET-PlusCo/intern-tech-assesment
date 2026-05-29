# End-to-end testing scenario

Use this checklist after Terraform apply, Cloud Build, and trigger setup. Your interviewer may ask you to walk through it live.

## 1. Open the app

1. Get the Cloud Run URL:
   ```sh
   cd frontend/terraform/deploy
   terraform output service_url
   ```
2. Open that URL in a browser.

## 2. Hello World and greeting

Confirm the page shows:

- **Hello World** heading
- A **Greeting** value (not blank if the pipeline is wired correctly)

## 3. Upload to Cloud Storage

1. Click **Upload image to Cloud Storage** and choose an image file from your computer.
2. Wait for the status message to show success.

## 4. Image under the greeting

Below the greeting and button, you should see the **uploaded image** rendered on the page.

If upload succeeds but the image does not appear.

## Quick reference

| Step | Pass |
|------|------|
| Cloud Run URL loads | ☐ |
| Hello World + greeting visible | ☐ |
| Upload completes without error | ☐ |
| Image visible under greeting | ☐ |
