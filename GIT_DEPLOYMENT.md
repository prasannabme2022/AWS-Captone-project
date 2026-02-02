# 🚀 Git Deployment Guide for MedTrack

## Quick Push to GitHub

### Step 1: Navigate to Project Directory
```bash
cd c:\Users\every\.gemini\antigravity\playground\holographic-ring\medtrack
```

### Step 2: Initialize Git (if not already done)
```bash
git init
```

### Step 3: Add Remote Repository
```bash
git remote add origin https://github.com/prasannabme2022/AWS-Captone-project.git
```

If you get an error that remote already exists, update it:
```bash
git remote set-url origin https://github.com/prasannabme2022/AWS-Captone-project.git
```

### Step 4: Check Current Status
```bash
git status
```

### Step 5: Add All Updated Files
```bash
git add .
```

Or add specific files:
```bash
git add aws_setup.py
git add requirements.txt
git add requirements-lite.txt
git add README.md
```

### Step 6: Commit Changes
```bash
git commit -m "✨ Updated AWS integration with DynamoDB and SNS support

- Migrated from CourierBuddy to MedTrack architecture
- Added 8 DynamoDB tables for complete healthcare management
- Integrated SNS notifications for all critical events
- Added AI chatbot framework
- Updated requirements.txt with AWS dependencies
- Added comprehensive README with deployment guide
- All features maintained: appointments, medical vault, blood bank, chat, mood tracking"
```

### Step 7: Pull Latest Changes (to avoid conflicts)
```bash
git pull origin main --rebase
```

If you're using a different branch (like `master`):
```bash
git pull origin master --rebase
```

### Step 8: Push to GitHub
```bash
git push -u origin main
```

Or if using master branch:
```bash
git push -u origin master
```

If you encounter authentication issues on Windows:
```bash
git config --global credential.helper wincred
```

---

## Alternative: Force Push (if needed)

⚠️ **Warning:** Only use if you want to overwrite remote repository completely

```bash
git push -u origin main --force
```

---

## Verify on GitHub

After pushing, visit:
https://github.com/prasannabme2022/AWS-Captone-project

You should see:
- ✅ Updated `aws_setup.py`
- ✅ Updated `requirements.txt` and `requirements-lite.txt`
- ✅ New `README.md`
- ✅ Commit message with timestamp

---

## Troubleshooting

### Error: "Permission denied (publickey)"
**Solution:** Configure SSH key or use HTTPS with personal access token

```bash
# Use HTTPS instead
git remote set-url origin https://github.com/prasannabme2022/AWS-Captone-project.git

# Or set up SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"
cat ~/.ssh/id_ed25519.pub
# Add this key to GitHub Settings > SSH Keys
```

### Error: "Remote contains work that you do not have locally"
**Solution:** Pull and merge first

```bash
git pull origin main --allow-unrelated-histories
git push origin main
```

### Error: "fatal: not a git repository"
**Solution:** Initialize git

```bash
git init
git remote add origin https://github.com/prasannabme2022/AWS-Captone-project.git
```

---

## Create .gitignore (Important!)

Make sure you have a `.gitignore` file to exclude sensitive files:

```gitignore
# Environment variables (contains AWS credentials)
.env
.env.local
.env.production

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Uploads (medical files)
uploads/*
!uploads/.gitkeep

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Database
*.db
*.sqlite3

# ML Models (large files)
models/*.h5
models/*.pkl
*.ckpt

# AWS
.aws/
```

---

## Best Practices

1. **Never commit `.env` file** - Contains AWS credentials
2. **Commit often** - Small, focused commits
3. **Write clear commit messages** - Use conventional commits format
4. **Pull before push** - Always sync with remote first
5. **Use branches** - For new features or experiments

---

## Useful Git Commands

```bash
# View commit history
git log --oneline

# View changes before committing
git diff

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Create and switch to new branch
git checkout -b feature/new-feature

# View all branches
git branch -a

# Delete local branch
git branch -d branch-name

# Rename branch
git branch -m old-name new-name
```

---

## GitHub Actions (Optional CI/CD)

Create `.github/workflows/deploy.yml` for automatic deployment:

```yaml
name: Deploy to AWS EC2

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to EC2
      env:
        PRIVATE_KEY: ${{ secrets.EC2_SSH_KEY }}
        HOST: ${{ secrets.EC2_HOST }}
        USER: ec2-user
      run: |
        echo "$PRIVATE_KEY" > private_key.pem
        chmod 600 private_key.pem
        ssh -o StrictHostKeyChecking=no -i private_key.pem ${USER}@${HOST} '
          cd ~/AWS-Captone-project &&
          git pull origin main &&
          pip3 install -r requirements-lite.txt &&
          sudo systemctl restart medtrack
        '
```

---

**Happy Coding! 🚀**
