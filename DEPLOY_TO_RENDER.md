# 🚀 Deploying ShopX to Render (24/7 Free Hosting)

Follow these simple steps to deploy ShopX on Render so the website and link stay active 24/7, even when your PC is completely turned off.

---

### Step 1: Push Your Code to GitHub

1. Go to [github.com](https://github.com) and log in (or create a free account).
2. Click the **"+"** icon in the top right and select **"New repository"**.
3. Name your repository: `shopx` (set it to Public or Private) and click **"Create repository"**.
4. In your project terminal or PowerShell, run:

```bash
cd C:\Users\ragha\.gemini\antigravity\scratch\shopx
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/shopx.git
git branch -M main
git push -u origin main
```
*(Replace `<YOUR_GITHUB_USERNAME>` with your actual GitHub username)*

---

### Step 2: Create a Free Web Service on Render

1. Go to [render.com](https://render.com) and sign in with your GitHub account.
2. In the Render Dashboard, click **New +** in the top navigation bar and select **Web Service**.
3. Under **"Connect a repository"**, select your `shopx` repository.
4. Fill in the deployment details (Render automatically fills most of these from `render.yaml`):
   * **Name:** `shopx` (or any custom name)
   * **Region:** Any (e.g., Singapore or Frankfurt for fast response in India)
   * **Branch:** `main`
   * **Runtime:** `Python 3`
   * **Build Command:** `pip install -r requirements.txt`
   * **Start Command:** `gunicorn app:app`
   * **Instance Type:** `Free`
5. Click **Deploy Web Service** at the bottom.

---

### Step 3: Access Your 24/7 Permanent Website

* Render will build and deploy the app in 2–3 minutes.
* You will receive a permanent HTTPS link:
  **`https://shopx-xxxx.onrender.com`**
* This link will **never turn off**, whether your computer is shut down, sleeping, or disconnected from the internet.

---

### Step 4: Accessing Logs & Customer Data Online

Because the app is in the cloud, you can access your data center from any phone or computer:
* **Online Admin Dashboard:** `https://your-app.onrender.com/admin`
* **Download Excel Sheet (.xlsx):** `https://your-app.onrender.com/admin/export-excel`
* **Download CSV File (.csv):** `https://your-app.onrender.com/admin/export-csv`
