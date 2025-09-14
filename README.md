# WORKSHOP BUILDING AI AGENTS WEEKEND
# AI_agent_profile and other notebooks/scripts of the workshop

# AI Agent Orchestrator — Health Reporting
# inside sandbox folder a streamlit app.py

A minimal Streamlit app that demonstrates an AI Agent Orchestrator between **patients**, **healthcare professionals**, and **insurance companies** to improve **structured medical reporting**, **transparency**, and **human‑in‑the‑loop** review.


### Quick Start (cloud)

You can run this app directly on [Streamlit Community Cloud](https://streamlit.io/cloud):

1. **Fork or clone** this repository into your own GitHub account.  
2. Go to [Streamlit Community Cloud](https://streamlit.io/cloud) and click **New app**.  
3. Select your repository, choose the **main** branch, and set `app.py` as the entry file.  
4. Deploy — Streamlit will build the environment automatically and give you a publ

ic URL.
## Quick Start (Local)
**Requirements:** Python 3.10+ (3.11 recommended), pip, and Graphviz (for the Architecture view).

```bash
git clone https://github.com/pedroMoya/AI_agent_profile.git
cd AI_agent_profile

python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

# dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# launch mockup
streamlit run app.py  # from sandbox directory
streamlit run sandbox/app.py  # from root

# If you see a Graphviz error on the Architecture page, install it:
# Ubuntu/Debian:   sudo apt-get update && sudo apt-get install -y graphviz
# macOS (Homebrew): brew install graphviz
# Windows (winget): winget install Graphviz.Graphviz