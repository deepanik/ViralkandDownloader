# Deployment Guide for Viralkand Bot

This guide will help you deploy your Telegram bot to free hosting platforms.

## 🎯 BEST OPTIONS: Free, Always-On, No Credit Card Required

### 🥇 Option 1: Koyeb (Recommended - No Credit Card)

**Free Tier:** ✅ Always-on, ✅ No credit card required

### Steps:
1. **Sign up** at [koyeb.com](https://www.koyeb.com) (use GitHub/Google - no credit card needed)
2. **Create App** → Deploy from GitHub
3. **Settings:**
   - **Name:** viralkand-bot
   - **Type:** Web Service
   - **Build Command:** `pip install -r requirements.txt`
   - **Run Command:** `python main.py`
4. **Add Environment Variables:**
   - Go to App → Settings → Environment Variables
   - Add:
     ```
     BOT_TOKEN=your_bot_token
     API_ID=your_api_id
     API_HASH=your_api_hash
     ADMIN_IDS=[6254260120]
     GROUP_IDS=[-1003328022346]
     MONGODB_URI=your_mongodb_uri
     MONGODB_DB_NAME=viralkand_bot
     ```
5. **Deploy** - Koyeb will automatically deploy
6. **Check logs** to ensure bot is running

**Note:** Koyeb free tier is always-on and doesn't require credit card!

---

### 🥈 Option 2: Fly.io (No Credit Card for Free Tier)

**Free Tier:** ✅ Always-on, ✅ No credit card for free tier

### Steps:
1. **Install Fly CLI:**
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   ```
2. **Sign up** at [fly.io](https://fly.io) (no credit card needed for free tier)
3. **Login:**
   ```bash
   fly auth login
   ```
4. **Deploy:**
   ```bash
   fly launch
   ```
   - Follow prompts
   - Don't deploy a database (you're using MongoDB Atlas)
5. **Set Environment Variables:**
   ```bash
   fly secrets set BOT_TOKEN=your_bot_token
   fly secrets set API_ID=your_api_id
   fly secrets set API_HASH=your_api_hash
   fly secrets set ADMIN_IDS="[6254260120]"
   fly secrets set GROUP_IDS="[-1003328022346]"
   fly secrets set MONGODB_URI=your_mongodb_uri
   fly secrets set MONGODB_DB_NAME=viralkand_bot
   ```
6. **Deploy:**
   ```bash
   fly deploy
   ```

**Note:** Free tier gives you 3 shared VMs that are always-on!

---

### 🥉 Option 3: Always Free Oracle Cloud (Truly Free Forever)

**Free Tier:** ✅ Always-on, ✅ Truly free forever, ✅ No credit card (but may ask for verification)

### Steps:
1. **Sign up** at [cloud.oracle.com](https://cloud.oracle.com) (free tier available)
2. **Create a VM Instance:**
   - Choose "Always Free" shape
   - Select Ubuntu 22.04
   - Create SSH keys
3. **SSH into your VM:**
   ```bash
   ssh opc@your-vm-ip
   ```
4. **Install Python and dependencies:**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip git -y
   ```
5. **Clone your repo:**
   ```bash
   git clone your-repo-url
   cd ViralkandDownloader
   ```
6. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```
7. **Set environment variables:**
   ```bash
   export BOT_TOKEN="your_bot_token"
   export API_ID="your_api_id"
   export API_HASH="your_api_hash"
   export ADMIN_IDS="[6254260120]"
   export GROUP_IDS="[-1003328022346]"
   export MONGODB_URI="your_mongodb_uri"
   export MONGODB_DB_NAME="viralkand_bot"
   ```
8. **Run with screen/tmux (to keep it running):**
   ```bash
   sudo apt install screen -y
   screen -S bot
   python3 main.py
   # Press Ctrl+A then D to detach
   ```

**Note:** Oracle Cloud Always Free is truly free forever, but setup is more complex.

---

### Option 4: Replit (Free but Limited Always-On)

**Free Tier:** ⚠️ Always-on requires Replit Hacker plan (paid), but free tier works for testing

### Steps:
1. **Sign up** at [replit.com](https://replit.com) (no credit card)
2. **Import from GitHub** your repo
3. **Add Environment Variables** in Secrets tab (lock icon)
4. **Run** the bot
5. **Note:** Free tier may sleep, but you can use "Keep Alive" services or upgrade

---

## ❌ Options That Require Credit Card:

- **Railway** - Requires credit card for free tier
- **Render** - Free tier sleeps (not always-on)
- **Heroku** - No longer has free tier

---

## 🚀 Option 1: Railway (Requires Credit Card)

**Free Tier:** $5 credit/month (usually enough for a small bot)

### Steps:
1. **Sign up** at [railway.app](https://railway.app) (use GitHub)
2. **Create New Project** → Deploy from GitHub
3. **Connect your GitHub repo** with the bot code
4. **Add Environment Variables:**
   - Go to your project → Variables tab
   - Add these variables:
     ```
     BOT_TOKEN=your_bot_token
     API_ID=your_api_id
     API_HASH=your_api_hash
     ADMIN_IDS=[6254260120]
     GROUP_IDS=[-1003328022346]
     MONGODB_URI=your_mongodb_uri
     MONGODB_DB_NAME=viralkand_bot
     ```
5. **Deploy** - Railway will automatically detect Python and deploy
6. **Check logs** to ensure bot is running

**Note:** Railway auto-detects `main.py` as the entry point.

---

## 🚀 Option 2: Render

**Free Tier:** ⚠️ Sleeps after 15 min (not always-on)

### Steps:
1. **Sign up** at [render.com](https://render.com) (use GitHub)
2. **New** → Background Worker
3. **Settings:**
   - **Name:** viralkand-bot
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python main.py`
4. **Add Environment Variables** (same as Railway)
5. **Deploy**

**Note:** Free tier sleeps after inactivity, so first request after sleep may be slow. Not recommended for always-on bots.

---

## 📝 Important Notes:

1. **Environment Variables:** Make sure all variables from `config.py` are set in your hosting platform
2. **MongoDB:** Your MongoDB Atlas connection should work from any platform
3. **Logs:** Check logs regularly to ensure bot is running
4. **Updates:** Push to GitHub to trigger automatic redeployment (Railway, Render, Koyeb)

---

## 🔧 Troubleshooting:

- **Bot not responding:** Check logs for errors
- **Connection errors:** Verify MongoDB URI is correct
- **Import errors:** Ensure all dependencies are in `requirements.txt`
- **Timeout errors:** Some platforms have request timeouts - your bot should handle this

---

## 💡 Recommendation:

**Start with Railway** - it's the easiest and most reliable free option for Telegram bots.

