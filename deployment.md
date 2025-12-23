# Deploying to Streamlit Community Cloud

Hosting your app for free on Streamlit Community Cloud is straightforward.

## 1. Prepare your GitHub Repository
Streamlit Cloud pulls code directly from GitHub.

1.  **Initialize Git** (if you haven't already):
    ```powershell
    git init
    git add .
    git commit -m "Initial commit of Helmet Detection App"
    ```
2.  **Create a Repository on GitHub**:
    - Go to [GitHub.com](https://github.com/new).
    - Create a new **Public** repository (e.g., `helmet-detection-app`).
3.  **Push your code**:
    ```powershell
    git remote add origin https://github.com/<your-username>/helmet-detection-app.git
    git branch -M main
    git push -u origin main
    ```

## 2. Configure Dependencies
Ensure your files are correct (we have already done this):
- **`requirements.txt`**: Must contain `opencv-python-headless` (which we used) instead of `opencv-python` to avoid graphical errors on the server.
- **`packages.txt`** (Optional): If you encounter "libGL" errors, create this file in the root with the following content:
    ```text
    libgl1
    ```

## 3. Deploy on Streamlit Cloud
1.  Go to [share.streamlit.io](https://share.streamlit.io/).
2.  Log in with your GitHub account.
3.  Click **"New app"**.
4.  **Select Repository**: Choose your `helmet-detection-app` repo.
5.  **Branch**: `main`.
6.  **Main file path**: `app.py`.
7.  Click **"Deploy!"**.

## 4. Important Settings for this App
Since this app uses a custom model (`best.pt`) and Webcam:
- **Model File**: Ensure `weights/best.pt` is small enough (<100MB) to be pushed to GitHub. GitHub has a file size limit of 100MB. If it's larger, you need to use **Git LFS** (Large File Storage).
- **HTTPS**: Streamlit Cloud handles HTTPS automatically, which is required for the Webcam to work on mobile devices.

## Troubleshooting
- **Webcam on Mobile**: If the webcam doesn't open on iOS/Android, ensure you gave the browser permission to access the camera.
- **"Module not found" error**: Check that the module is listed in `requirements.txt`.
