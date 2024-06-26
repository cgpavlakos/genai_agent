# Oracle Generative AI Agents Sample

Demo Streamlit App for Oracle Cloud Generative AI Agents. 

## Overview of the App

- Provides an external UI front end for Oracle Cloud Generative AI Agents, currently in beta.

![diagram](RAG%20Demo%20Diagram.png)

## Live Demo App

http://rag.pavlakos.me


## Try out the demo in your Oracle Cloud Tenancy

0. Set up Generative AI Agents service and note the agent_endpoint_id
1. Make sure you have port 8502 open on security list
2. Launch a VM with ubuntu base image and attach setup.sh as cloud-init script
4. SSH into your VM (ubuntu@ipaddress) and check the log at /home/ubuntu/genai_agent_setup.log
5. Run setup.sh if you did not add it as cloud-init script
6. Set up OCI config
7. Update .streamlit/secrets.toml with your agent_endpoint_id
8. Use run.sh to run the demo
9. Your application will be running on http://server-ip-address:8502
