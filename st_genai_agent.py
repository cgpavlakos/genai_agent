import streamlit as st
import oci
import genai_agent_service_bmc_python_client

# OCI Configuration
CONFIG_PROFILE = "DEFAULT"
config = oci.config.from_file()
#endpoint = "https://agent-runtime.generativeai.us-chicago-1.oci.oraclecloud.com"
#agent_endpoint_id = "ocid1.genaiagentendpoint.oc1.us-chicago-1.12345"
endpoint = st.secrets["endpoint"] #make sure to put these in secrets.toml file
agent_endpoint_id = st.secrets["agent_endpoint_id"] #make sure to put these in secrets.toml file

# Streamlit UI
st.set_page_config(page_title="GenAI Agent", 
                   page_icon="🤖", layout="centered", 
                   initial_sidebar_state="auto", menu_items=None)
st.title("Oracle GenAI Agent Chat")
st.subheader("Powered by Oracle Generative AI Agents (Beta)")
st.info("Check out the [architecure diagram](https://www.oracle.com/a/ocom/img/rc24full-diagram-how-generative-ai-agents-work.png) and [product page](https://www.oracle.com/artificial-intelligence/generative-ai/agents/) to see how the Oracle Data Platform and Generative AI come together for this demo of a fully secure and private RAG chatbot.")

# Sidebar
with st.sidebar:
    if st.button("Reset Chat", type="primary", use_container_width=True, help="Reset chat history and clear screen"):
        st.session_state.messages = []  
        st.session_state.session_id = None  
        st.rerun()  
st.sidebar.markdown(
    """
    ## About

    This demo leverages the power of **Oracle's Cloud Data Platform** to provide you with a seamless and informative retrieval-augmented generation (RAG) chat experience 
    through **Generative AI Agents**, which is currently in beta. The UI is Streamlit, an open-source Python framework.

    ## Features
    - **Secure & Private:** All data remains confidential within your Oracle Cloud tenancy, benefiting from all of the built-in security features.
    - **Chat with the GenAI Agent:** Have a conversation - ask questions and get insightful answers.
    - **View Citations:** Explore the sources behind the agent's responses to validate the responses are grounded. 
    - **Reset Chat:** A button to clear the session history and start fresh. 

    ## Underlying Oracle Cloud Data Platform Services
    - **Object Storage:** Stores private data files with AES256 encryption.
    - **Generative AI Agents (Beta):** Provides the RAG pipeline as a PaaS service. 
    - **Open Search:** Knowledge base holding the private data files for fast search. 
    - **Generative AI Service:** Can be either shared or dedicated hosting, with your choice of Cohere and Meta for Large Language Model (LLM).
    - **Compute:** A virtual machine hosts the Streamlit app to provide the UI. 

    ## Data Sources 
    - **Executive Orders:** Including Executive Order 14028 - Improving the Nation's Cybersecurity
    - **Government Memos and Guidance:** Documents such as M-21-31 and guidance from CISA and NIST
    - **Oracle Product Documentation:** Technical documentation or Oracle Cloud Services 
    - **Oracle Whitepapers:** Created by Federal Civilian the field team regarding topics such as TIC 3.0
    
    *Created by chris.pavlakos@oracle.com*
    """
)

# Initialize chat history and session ID in session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = None

# Create GenAI Agent Runtime Client (only if session_id is None)
if st.session_state.session_id is None:
    genai_agent_runtime_client = genai_agent_service_bmc_python_client.GenerativeAiAgentRuntimeClient(
        config=config,
        service_endpoint=endpoint,
        retry_strategy=oci.retry.NoneRetryStrategy(),
        timeout=(10, 240)
    )

    # Create session
    create_session_details = genai_agent_service_bmc_python_client.models.CreateSessionDetails(
        display_name="display_name", idle_timeout_in_seconds=10, description="description"
    )
    create_session_response = genai_agent_runtime_client.create_session(create_session_details, agent_endpoint_id)
    
    # Store session ID
    st.session_state.session_id = create_session_response.data.id

    # Check if welcome message exists and append to message history
    if hasattr(create_session_response.data, 'welcome_message'):
        st.session_state.messages.append({"role": "assistant", "content": create_session_response.data.welcome_message})


# Display chat messages from history (including initial welcome message, if any)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
if user_input := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Execute session (re-use the existing session)
    genai_agent_runtime_client = genai_agent_service_bmc_python_client.GenerativeAiAgentRuntimeClient(
            config=config, 
            service_endpoint=endpoint,
            retry_strategy=oci.retry.NoneRetryStrategy(), 
            timeout=(10, 240)
        )
    # Display a spinner while waiting for the response
    with st.spinner("Working..."):  # Spinner for visual feedback 
        execute_session_details = genai_agent_service_bmc_python_client.models.ExecuteSessionDetails(
        user_message=str(user_input), should_stream=False  # You can set this to True for streaming responses
     )
        execute_session_response = genai_agent_runtime_client.execute_session(agent_endpoint_id, st.session_state.session_id, execute_session_details)

    # Display agent response
    if execute_session_response.status == 200:
        response_content = execute_session_response.data.message.content
        st.session_state.messages.append({"role": "assistant", "content": response_content.text})
        with st.chat_message("assistant"):
            st.markdown(response_content.text)
     # Display citations
        if response_content.citations:
         with st.expander("Citations"):  # Collapsable section
            for i, citation in enumerate(response_content.citations, start=1):
                st.write(f"**Citation {i}:**")  # Add citation number
                st.markdown(f"**Source:** [{citation.source_location.url}]({citation.source_location.url})") 
                st.text_area("Citation Text", value=citation.source_text, height=200) # Use st.text_area for better formatting   
    else:
        st.error(f"API request failed with status: {execute_session_response.status}")
