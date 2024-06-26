# Allow traffic on port 8502 (replace with your desired port if needed)
echo "** Opening port 8502 for incoming traffic..."
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8502 -j ACCEPT

# Activate virtual environment and navigate to app directory
cd /home/ubuntu/src/genai_agent-main/genai_agent_env/bin
source activate
cd /home/ubuntu/src/genai_agent-main

# Run the application in the background
echo "** Running application in the background..."
nohup streamlit run st_genai_agent.py &
