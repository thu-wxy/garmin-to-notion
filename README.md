[![Sync Garmin to Notion](https://github.com/thu-wxy/garmin-to-notion/actions/workflows/sync_garmin_to_notion.yml/badge.svg?branch=main)](https://github.com/thu-wxy/garmin-to-notion/actions/workflows/sync_garmin_to_notion.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

# Garmin to Notion Integration :watch:

Automatically sync your **Garmin Connect** activities, personal records, steps, and sleep data into a **Notion** database — with rich visual indicators so you can spot trends at a glance.

---

## ✨ Features

| Script | What it syncs |
|---|---|
| `garmin-activities.py` | All activities: run, ride, swim, yoga, strength … |
| `personal-records.py` | Fastest 1K/5K/10K, longest run/ride, power PRs |
| `daily-steps.py` | Daily step count and goal progress *(optional)* |
| `sleep-data.py` | Sleep stages, resting HR, bedtime/wake times *(optional)* |

**Visual enhancements included in every activity entry:**

- 🏃 **Activity icon** — per-type icon rendered directly on the Notion page
- 📏 **Avg Pace** — formatted as `5:30 min/km`
- 💓 **Avg HR / Max HR** — numerical, filterable
- 🔴 **HR Zone** — auto-derived label (`Zone 2 · Easy` … `Zone 5 · Max`)
- ⚡ **Intensity** — emoji label derived from Garmin's Aerobic Training Effect
  (`😴 Recovery` → `🟢 Minor Benefit` → `🟡 Maintaining` → `🟠 Improving` → `🔴 Overreaching`)
- ⛰️ **Elevation Gain (m)** — recorded when the activity includes GPS altitude data
- 🏅 **PR / Fav** checkboxes, Training Effect select, Aerobic / Anaerobic TE scores

> **Backward-compatible:** The five new optional columns (`Avg HR`, `Max HR`, `HR Zone`, `Intensity`, `Elevation Gain (m)`) are written only when they exist in your Notion database schema. If they are absent the script silently falls back to the original core fields — your existing database keeps working without any changes.

---

## 🚀 Quick Start

```bash
# 1 · Fork this repo, then clone your fork
git clone https://github.com/<your-username>/garmin-to-notion
cd garmin-to-notion

# 2 · Install dependencies
pip install -r requirements.txt

# 3 · Copy the example env file and fill in your credentials
cp .example.env .env
# Edit .env with your GARMIN_EMAIL, GARMIN_PASSWORD, NOTION_TOKEN, …

# 4 · Run manually
python garmin-activities.py   # sync activities
python personal-records.py    # sync PRs
python daily-steps.py         # sync steps  (requires NOTION_STEPS_DB_ID)
python sleep-data.py          # sync sleep  (requires NOTION_SLEEP_DB_ID)
```

Automated daily sync via GitHub Actions is configured in `.github/workflows/sync_garmin_to_notion.yml` and runs at **01:00 UTC** by default.

---

## 🛠️ Prerequisites

- A **Garmin Connect** account
- A **Notion** account with API access
- Python 3.11+

*Optional: sync Peloton workouts into Garmin first with [peloton-to-garmin](https://github.com/philosowaffle/peloton-to-garmin).*

---

## 📋 Setup Guide

### 1. Fork this Repository

### 2. Duplicate the Notion Template

Duplicate the free [Fitness Tracker template](https://www.notion.so/templates/fitness-tracker-738) to your workspace.

- **Activities DB** — copy the database ID from the URL: `notion.so/<username>/<database-id>?v=…`
- **Personal Records DB** — same process
- *(Optional)* **Daily Steps DB** and **Sleep DB**

### 3. Create a Notion Integration Token

1. Go to [Notion Integrations](https://www.notion.so/profile/integrations) and create a new integration.
2. Copy the **Internal Integration Token**.
3. [Share each database](https://www.notion.so/help/add-and-manage-connections-with-the-api) with your integration.

### 4. Configure Repository Secrets

Set these in **Settings → Secrets and variables → Actions**:

| Secret / Variable | Required | Description |
|---|---|---|
| `GARMIN_EMAIL` | ✅ | Garmin Connect login email |
| `GARMIN_PASSWORD` | ✅ | Garmin Connect password |
| `NOTION_TOKEN` | ✅ | Notion integration token |
| `NOTION_DB_ID` | ✅ | Activities database ID |
| `NOTION_PR_DB_ID` | ✅ | Personal Records database ID |
| `NOTION_STEPS_DB_ID` | ☑️ optional | Daily Steps database ID |
| `NOTION_SLEEP_DB_ID` | ☑️ optional | Sleep database ID |
| `GARMIN_ACTIVITIES_FETCH_LIMIT` | ☑️ optional | Max activities to fetch (default: 1000) |

### 5. (Optional) Add Visual Columns to Your Activities DB

To see the new visual fields, add these columns to your Notion Activities database:

| Column name | Type | Notes |
|---|---|---|
| `Avg HR` | Number | Average heart rate (bpm) |
| `Max HR` | Number | Peak heart rate (bpm) |
| `HR Zone` | Select | Auto-set: Zone 1–5 with label |
| `Intensity` | Select | Emoji label from Aerobic Training Effect |
| `Elevation Gain (m)` | Number | Cumulative elevation gain |

If these columns are absent the script works exactly as before.

---

## 🖼️ What it Looks Like

Here is a screenshot of the Notion dashboard using this integration:

![garmin-to-notion-template](https://github.com/user-attachments/assets/b37077cc-fe87-466f-9424-8ba9e4efa909)

**Example activity entry** (Activities database row):

| Field | Example value |
|---|---|
| Activity Name | Morning Run |
| Activity Type | Running |
| Date | 2024-05-10 07:30 |
| Distance (km) | 10.23 |
| Duration (min) | 54.10 |
| Avg Pace | 5:17 min/km |
| Calories | 612 |
| Avg HR | 148 |
| Max HR | 172 |
| HR Zone | Zone 4 · Threshold |
| Intensity | 🟠 Improving |
| Aerobic | 3.4 |
| Aerobic Effect | Impacting |
| Elevation Gain (m) | 85 |
| PR | ☑ |

---

## 🙏 Acknowledgements

- Garmin API client: [cyberjunky/python-garminconnect](https://github.com/cyberjunky/python-garminconnect)
- Original concept: [n-kratz/garmin-notion](https://github.com/n-kratz/garmin-notion)

## 🤝 Contributing

Contributions are welcome! Open an issue or submit a pull request.
Financial support is also appreciated 😊

<a href="https://www.buymeacoffee.com/cvoyer" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

## 📄 License

MIT — see [LICENSE](LICENSE) for details.
