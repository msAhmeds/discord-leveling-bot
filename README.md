# 🤖 Discord Economy & Level Bot

A Discord bot written in Python that includes an XP system, economy system, and gambling features.  
The bot stores all user data permanently using SQLite.

---

## 🚀 Features

- 💬 XP system (gain XP by chatting)
- 📈 Level system (level up automatically)
- 💰 Economy system (coins for activity)
- 🎁 Daily rewards
- 🎰 Gambling system (risk coins for rewards)
- 🗃 Persistent database (SQLite)

---

## ⚙️ How it works (Explanation)

This bot uses:

### 🧠 XP System
- Every message gives random XP (5–15)
- When XP reaches a threshold (`level * 100`), the user levels up
- XP resets partially after leveling

### 💰 Economy System
- Users earn coins automatically by chatting
- Coins are stored in a database
- Coins can be used in gambling

### 🗃 Database (SQLite)
- All user data is stored in `database.db`
- Data includes:
  - user_id
  - xp
  - level
  - coins
- Data persists even after bot restart

### 🎰 Gambling System
- Users can gamble coins using:

!gamble <amount>


- 50% chance to win or lose
- If win → coins are added
- If lose → coins are removed

---

## 📌 Commands

!balance → Show your coins
!daily → Get random daily coins


### 📈 Level System

!level → Show your XP and level


### 🎰 Gambling

!gamble <amount> → Gamble your coins


---

## 🔧 Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/discord-bot.git
cd discord-bot
2. Install dependencies
pip install -r requirements.txt
3. Set up environment variable

This bot uses an environment variable for security:

Create a .env file OR set system variable:
DISCORD_TOKEN=your_bot_token_here

OR directly in terminal:

Windows (CMD):
set DISCORD_TOKEN=your_bot_token
Mac/Linux:
export DISCORD_TOKEN=your_bot_token
4. Run the bot
python bot.py
