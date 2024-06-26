#!/bin/bash

# This can be executed on an ubuntu base image, or you can do steps manually with necessary changes on other OS. 
# Make sure your oci setup is correct

# Define a log file
LOG_FILE=/home/ubuntu/genai_agent_setup.log

# Redirect standard output (stdout) and standard error (stderr) to the log file
exec &>> "$LOG_FILE"

# Update and upgrade system packages
echo "** Starting system update and upgrade (check log for details)..."
sudo apt update -y && sudo apt upgrade -y

# Install required python libraries
echo "** Installing python libraries (check log for details)..."
sudo apt install python3-virtualenv unzip -y

# Create directories
echo "** Creating directories..."
mkdir /home/ubuntu/src
mkdir /home/ubuntu/src/genai_agent

# Navigate to gen_ai directory
cd /home/ubuntu/src/genai_agent

# Create virtual environment and activate it
echo "** Creating and activating virtual environment..."
virtualenv genai_agent_env
source genai_agent_env/bin/activate

# Download sample application and SDK
cd /home/ubuntu/
echo "** Downloading sample application..."
wget https://github.com/cgpavlakos/GenAI-Demo/archive/refs/heads/main.zip
unzip main.zip -d src

# Install python libraries using pip
cd /home/ubuntu/src/gen_ai_agent
echo "** Installing python libraries with pip (check log for details)..."
pip install streamlit oci genai_agent_service_bmc_python_client-0.1.77-py2.py3-none-any.whl

# OCI CLI setup (commented out, replace with your own setup)
# bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)"
# oci setup config

echo "** Application installed. Make sure to edit your secrets.toml. Check the log file (~/genai_agent_setup.log) for details."

# Deactivate virtual environment (optional)
# deactivate
