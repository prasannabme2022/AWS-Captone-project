# Medtrack Production Deployment Guide

## 🛑 Prerequisites (Read First)
Before you can deploy to the cloud, you **must install these tools** on your local machine:
1.  **Git**: Required to push your code to the cloud. [Download Git](https://git-scm.com/downloads)
2.  **Docker Desktop**: Required if you want to test the "Universal" container locally. [Download Docker](https://www.docker.com/products/docker-desktop/)

This guide details how to deploy Medtrack to a permanent production host...

This guide details how to deploy Medtrack to a permanent production host using Docker. This approach is platform-agnostic and works on **Render**, **DigitalOcean**, **Heroku**, **Railway**, or any **Linux VPS**.

## 🏠 Option 0: Local Windows (No Docker)
If you are running on Windows without Docker installed, use the included `server.py`. It uses **Waitress**, a production-quality server for Windows.

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run Server**:
    ```bash
    python server.py
    ```
3.  **Access**: Open `http://localhost:8080`.

---

## 🚀 Option 1: PaaS (Easiest - Recommended)
Platforms like **Render** or **Railway** allow you to deploy directly from GitHub.

### Deploying to Render.com
1.  **Push** your code to a GitHub repository.
2.  Sign up at [render.com](https://render.com).
3.  Click **New +** -> **Web Service**.
4.  Connect your GitHub repository.
5.  **Settings**:
    *   **Runtime**: Docker
    *   **Region**: Singapore / Frankfurt / New York (Choose closest to you)
    *   **Instance Type**: Free (starts with Free)
6.  Click **Create Web Service**.
7.  Render will auto-detect the `Dockerfile`, build it, and deploy.
8.  **Done!** Your app will be live at `https://medtrack-xxxx.onrender.com`.

---

## 💻 Option 2: Generic Linux VPS (DigitalOcean / Linode / Hetzner)
For complete control, you can host on a virtual private server (VPS).

### Prerequisites
*   A VPS running Ubuntu 22.04 LTS (approx. $5-6/mo).
*   Docker and Docker Compose installed.

### Steps
1.  **SSH into your server:**
    ```bash
    ssh root@your_server_ip
    ```
2.  **Clone your project:**
    ```bash
    git clone https://github.com/yourusername/medtrack.git
    cd medtrack
    ```
3.  **Start the Application:**
    We have included a `docker-compose.yml` that handles networking and persistence.
    ```bash
    docker-compose up -d --build
    ```
4.  **Verify:**
    Visit `http://your_server_ip` in your browser. The app runs on Port 80 by default.

## 📦 Persistence Note
The application uses local storage for `database.py` (in-memory) and uploads (`medtrack/uploads`).
*   **Uploads**: The `docker-compose.yml` maps a volume so uploaded files persist even if you restart the container.
*   **Database**: Since this is a specialized in-memory version, data resets on restart. For data persistence in production, consider connecting to an external Database (PostgreSQL/MongoDB).
