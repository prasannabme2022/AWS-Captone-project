---
description: Zero-Cost Patient Data Storage Plan (S3 Alternative)
---

# 📂 Zero-Cost Data Storage Plan: Local EBS Strategy

Since AWS S3 is outside the current budget, we will utilize the **Elastic Block Store (EBS)** volume attached to your EC2 instance. This provides persistent "cloud disk" storage without the additional per-request costs of S3.

## 1. Architecture Overview

Instead of sending files to an external bucket (S3), the application will save uploaded patient records (PDFs, Images, X-Rays) directly to the server's hard drive.

**Flow:**
1. **User** uploads a file via the Medical Vault.
2. **Flask** receives the file.
3. **Application** saves it to `medtrack/uploads/` on the EC2 instance.
4. **Database** (DynamoDB) stores the *filepath* (e.g., `uploads/scan_123.jpg`) instead of an S3 URL.
5. **Nginx/Flask** serves the file back to the doctor/patient when requested.

## 2. Implementation Details

### Current Configuration (`app.py`)
Your application is **already pre-configured** for this method!
```python
# app.py matches this strategy:
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'medtrack', 'uploads')
# ...
file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
```

### Advantages
| Feature | S3 (Standard) | Local EBS (Our Plan) |
| :--- | :--- | :--- |
| **Cost** | Storage + Request Fees | **Free** (Included in EC2) |
| **Speed** | Network Latency | **Instant** (Local Disk) |
| **Complexity** | High (IAM, Buckets) | **Low** (Standard IO) |

## 3. Deployment Instructions (For EC2)

When you deploy to AWS EC2, you must ensure the upload directory persists.

1. **Create the Directory:**
   In your setup script or manually on the server:
   ```bash
   mkdir -p /home/ubuntu/medtrack/uploads
   chmod 777 /home/ubuntu/medtrack/uploads
   ```

2. **Persistence Rule:**
   * **Do not** destroy/terminate the EC2 instance, or you lose the data.
   * **Do** Stop/Start the instance freely (EBS persists data across reboots).

## 4. Backup Strategy (Recommended)

To mimic S3 durability:
* **EBS Snapshots:** Once a week, go to AWS Console -> EC2 -> Volumes -> Actions -> **Create Snapshot**. This is your backup.

## 5. Security Note
* The `uploads` folder is local. Ensure file permissions are restricted so only the web user can read/write.
* Access is controlled via Flask's `@login_required` decorators before serving the file.

---
**Status:** ✅ Implemented in Code. Ready for Deployment.
