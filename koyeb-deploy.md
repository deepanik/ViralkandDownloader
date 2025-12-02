# Quick Deploy Guide: Koyeb (Free, Always-On, No Credit Card)

## ✅ Why Koyeb?
- ✅ **100% Free** - No credit card required
- ✅ **Always-On** - Never sleeps
- ✅ **Easy Setup** - GitHub integration
- ✅ **Perfect for Telegram Bots**

## 🚀 Step-by-Step Deployment

### Step 1: Prepare Your Code
1. Make sure all your code is on GitHub
2. Ensure `requirements.txt` exists
3. Ensure `main.py` is your entry point

### Step 2: Sign Up
1. Go to [koyeb.com](https://www.koyeb.com)
2. Click **"Get Started"** or **"Sign Up"**
3. Sign up with **GitHub** (easiest) or Google
4. **No credit card required!**

### Step 3: Create App
1. Click **"Create App"** button
2. Select **"GitHub"** as source
3. Choose your repository: `ViralkandDownloader`
4. Click **"Deploy"**

### Step 4: Configure App
1. **App Name:** `viralkand-bot` (or any name)
2. **Type:** Select **"Web Service"**
3. **Build Command:** `pip install -r requirements.txt`
4. **Run Command:** `python main.py`
5. Click **"Deploy"**

### Step 5: Add Environment Variables
1. Go to your app dashboard
2. Click **"Settings"** tab
3. Scroll to **"Environment Variables"**
4. Click **"Add Variable"** for each:

```
BOT_TOKEN = 8528138443:AAEmFwE0KAmrA4v0H2zRfZJ_a9l9kratcd8
API_ID = 36998260
API_HASH = db67579e13f426a10f4d8dcff6d2ced2
ADMIN_IDS = [6254260120]
GROUP_IDS = [-1003328022346]
MONGODB_URI = mongodb+srv://dropmail880_db_user:lqXiGLNkEowwcOo9@cluster0.aw9jwfg.mongodb.net/?appName=Cluster0
MONGODB_DB_NAME = viralkand_bot
```

**Important:** 
- For `ADMIN_IDS` and `GROUP_IDS`, use JSON format: `[6254260120]` (with brackets)
- Or comma-separated: `6254260120` (config.py will handle both)

### Step 6: Deploy
1. After adding variables, Koyeb will automatically redeploy
2. Go to **"Logs"** tab to see deployment progress
3. Wait for: `Bot is starting...` message
4. Your bot is now live! 🎉

### Step 7: Verify
1. Check **"Logs"** tab - should show bot is running
2. Test your bot in Telegram
3. Send a viralkand.com link to test

## 🔧 Troubleshooting

### Bot Not Starting?
- Check **Logs** tab for errors
- Verify all environment variables are set correctly
- Make sure `requirements.txt` has all dependencies

### Import Errors?
- Check that all files are in your GitHub repo
- Verify `config.py`, `bot.py`, `kand.py`, `database.py` are all present

### Connection Errors?
- Verify `MONGODB_URI` is correct
- Check MongoDB Atlas allows connections from anywhere (0.0.0.0/0)

### Bot Not Responding?
- Check logs for timeout errors
- Verify `BOT_TOKEN` is correct
- Make sure bot is added to your Telegram group

## 📝 Notes

- **Free Tier Limits:** 
  - 2 apps per account
  - 512 MB RAM per app
  - Sufficient for Telegram bots!

- **Always-On:** 
  - Koyeb free tier is truly always-on
  - No sleeping, no downtime
  - Perfect for polling bots

- **Updates:**
  - Push to GitHub = Auto-deploy
  - Changes are live in ~2-3 minutes

## 🎉 You're Done!

Your bot is now running 24/7 for free on Koyeb!

