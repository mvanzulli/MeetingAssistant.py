#!/bin/bash
source .venv/bin/activate

# Activate virtual environment and start the model API in the background
cd model
source .venv/bin/activate
nohup python api.py > api.log 2>&1 &
cd ..

# Wait for the model API to start up (modify the sleep time as needed)
sleep 5

# Activate virtual environment and start the web app in the background
cd web_app
source .venv/bin/activate
streamlit run web_app.py
cd ..
