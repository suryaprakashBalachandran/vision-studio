# Git Setup and Push Guide

## Step 1: Check Git Status

First, see what files will be committed:

```bash
git status
```

## Step 2: Add Files to Git

Add all files (respecting .gitignore):

```bash
git add .
```

Or add specific files:

```bash
git add app/
git add tests/
git add requirements.txt
git add README.md
git add .env.example
```

## Step 3: Commit Your Changes

Create a commit with a message:

```bash
git commit -m "Initial commit: Vision Studio API with Gemini integration"
```

Or with a more detailed message:

```bash
git commit -m "feat: Add Vision Studio API

- FastAPI application for document data extraction
- Google Gemini AI integration
- Support for PDF, PNG, JPG, JPEG files
- Reference-based and instruction-based extraction
- 30 comprehensive test scenarios
- Complete API documentation"
```

## Step 4: Create a GitHub Repository

### Option A: Using GitHub Website

1. Go to https://github.com
2. Click the "+" icon → "New repository"
3. Name it: `vision-studio` (or your preferred name)
4. Choose Public or Private
5. **DO NOT** initialize with README (you already have one)
6. Click "Create repository"

### Option B: Using GitHub CLI (if installed)

```bash
gh repo create vision-studio --public --source=. --remote=origin
```

## Step 5: Link Local Repository to GitHub

Copy the repository URL from GitHub, then:

```bash
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/vision-studio.git
```

Or if using SSH:

```bash
git remote add origin git@github.com:YOUR_USERNAME/vision-studio.git
```

## Step 6: Push to GitHub

Push your code to the main branch:

```bash
git branch -M main
git push -u origin main
```

---

## Complete Command Sequence

Here's the full sequence to copy and paste:

```bash
# 1. Check status
git status

# 2. Add all files
git add .

# 3. Commit
git commit -m "Initial commit: Vision Studio API with Gemini integration"

# 4. Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/vision-studio.git

# 5. Push to GitHub
git branch -M main
git push -u origin main
```

---

## Important: Verify .gitignore

Make sure your `.gitignore` file excludes sensitive data:

```bash
cat .gitignore
```

Should include:
```
.env
__pycache__/
*.pyc
venv/
.DS_Store
```

**NEVER commit your `.env` file with API keys!**

---

## Troubleshooting

### Error: "remote origin already exists"

```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/vision-studio.git
```

### Error: "failed to push some refs"

```bash
git pull origin main --rebase
git push -u origin main
```

### Error: "Permission denied (publickey)"

Use HTTPS instead of SSH:

```bash
git remote set-url origin https://github.com/YOUR_USERNAME/vision-studio.git
```

---

## After Pushing

Your repository will be available at:
```
https://github.com/YOUR_USERNAME/vision-studio
```

### Add a README Badge

Add this to your README.md:

```markdown
# Vision Studio API

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
```

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `git status` | Check what files changed |
| `git add .` | Stage all files |
| `git commit -m "message"` | Commit changes |
| `git push` | Push to remote |
| `git pull` | Pull from remote |
| `git log` | View commit history |

---

## Next Steps

1. ✅ Push code to GitHub
2. Add repository description on GitHub
3. Add topics/tags: `fastapi`, `gemini-api`, `document-extraction`, `ocr`
4. Enable GitHub Actions for CI/CD (optional)
5. Add a LICENSE file (MIT recommended)

---

**Ready to push!** Just replace `YOUR_USERNAME` with your GitHub username and run the commands. 🚀
