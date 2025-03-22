import streamlit as st
import requests
import json
import time
from requests.exceptions import RequestException

# Set up the page with a more polished configuration
st.set_page_config(
    page_title="Ollama Chat Interface", 
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .chat-container {
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .stTextInput>div>div>input {
        background-color: #f0f2f6;
    }
    .status-indicator {
        height: 10px;
        width: 10px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 5px;
    }
    .status-online {
        background-color: #28a745;
    }
    .status-offline {
        background-color: #dc3545;
    }
</style>
""", unsafe_allow_html=True)

# App title with logo
st.title("🤖 Ollama Chat Interface")
st.markdown("Connect with your local Ollama models for interactive conversations")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_model" not in st.session_state:
    st.session_state.current_model = None
if "connection_status" not in st.session_state:
    st.session_state.connection_status = "unknown"
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = "You are a helpful AI assistant."
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7
if "max_tokens" not in st.session_state:
    st.session_state.max_tokens = 2000

def check_ollama_connection():
    """Check if Ollama service is running and return status"""
    try:
        response = requests.get("http://localhost:11434", timeout=3)
        if response.status_code == 200:
            return "online"
        return "offline"
    except RequestException:
        return "offline"

def get_available_models():
    """Fetch available models from Ollama"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models_data = response.json()
            model_names = [model["name"] for model in models_data.get("models", [])]
            return model_names or ["No models found"]
        return ["Error fetching models"]
    except RequestException:
        return ["Connection error"]

def format_message(message):
    """Format message with proper styling based on role"""
    return message

def generate_response(prompt, model, system_prompt=None, temperature=0.7, max_tokens=2000):
    """Generate a streaming response using selected Ollama model with parameters"""
    try:
        # Prepare the request payload with advanced parameters
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": float(temperature),
                "num_predict": int(max_tokens)
            }
        }
        
        # Add system prompt if provided
        if system_prompt:
            payload["system"] = system_prompt
            
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            stream=True,
            timeout=120
        )
        
        if response.status_code == 404:
            yield "⚠️ Model not found. Please verify the model exists using 'ollama list'."
            return
            
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                try:
                    chunk_data = json.loads(line.decode("utf-8"))
                    chunk = chunk_data.get("response", "")
                    
                    # Check for completion
                    if chunk_data.get("done", False) and not chunk:
                        # Yield stats about the generation if available
                        stats = chunk_data.get("eval_count", 0)
                        if stats:
                            yield f"\n\n---\n*Generated {stats} tokens*"
                    else:
                        yield chunk
                        
                except json.JSONDecodeError:
                    continue
    
    except RequestException as e:
        yield f"⚠️ API Error: {str(e)}"

# Sidebar for settings and controls
with st.sidebar:
    # Connection status indicator
    st.session_state.connection_status = check_ollama_connection()
    status_color = "status-online" if st.session_state.connection_status == "online" else "status-offline"
    status_text = "Connected" if st.session_state.connection_status == "online" else "Disconnected"
    
    st.markdown(f"<div><span class='status-indicator {status_color}'></span> <b>Status:</b> {status_text}</div>", 
                unsafe_allow_html=True)
    
    if st.session_state.connection_status == "offline":
        st.error("Ollama is not running. Please start the Ollama service.")
        
        with st.expander("Troubleshooting"):
            st.markdown("""
            1. Make sure Ollama is installed
            2. Open a terminal and run `ollama serve`
            3. Refresh this page
            """)
        st.stop()
    
    # Model selection
    st.subheader("Model Selection")
    available_models = get_available_models()
    
    selected_model = st.selectbox(
        "Choose a model",
        available_models,
        index=0 if not st.session_state.current_model else available_models.index(st.session_state.current_model) 
        if st.session_state.current_model in available_models else 0
    )
    
    if selected_model != st.session_state.current_model:
        st.session_state.current_model = selected_model
    
    # Advanced settings
    st.subheader("Advanced Settings")
    
    with st.expander("Generation Parameters"):
        st.session_state.system_prompt = st.text_area(
            "System Prompt",
            value=st.session_state.system_prompt,
            help="Instructions that define model behavior"
        )
        
        st.session_state.temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=st.session_state.temperature,
            step=0.1,
            help="Higher values make output more random, lower more deterministic"
        )
        
        st.session_state.max_tokens = st.number_input(
            "Max Tokens",
            min_value=10,
            max_value=8192,
            value=st.session_state.max_tokens,
            step=10,
            help="Maximum number of tokens to generate"
        )
    
    # Chat management
    st.subheader("Chat Management")
    
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.success("Chat history cleared!")
        time.sleep(1)
        st.rerun()
    
    # Information about the app
    with st.expander("About"):
        st.markdown("""
        This app provides a chat interface for Ollama, allowing you to interact with 
        locally running LLMs. The interface connects to the Ollama API running on 
        your local machine.
        
        For more information about Ollama, visit [ollama.ai](https://ollama.ai)
        """)

# Main chat interface
chat_container = st.container()

with chat_container:
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input for new messages
    if prompt := st.chat_input("Send a message...", key="chat_input"):
        if not st.session_state.current_model or st.session_state.current_model in ["No models found", "Error fetching models", "Connection error"]:
            st.error("Please select a valid model first")
            st.stop()
            
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            
            # Stream the response with a blinking cursor effect
            for chunk in generate_response(
                prompt, 
                st.session_state.current_model,
                st.session_state.system_prompt,
                st.session_state.temperature,
                st.session_state.max_tokens
            ):
                full_response += chunk
                response_placeholder.markdown(full_response + "▌")
                time.sleep(0.005)  # Small delay for smoother streaming
            
            # Display the final response
            response_placeholder.markdown(full_response)
            
            # Add complete response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# Add a footer
st.markdown("---")
st.markdown("*Powered by Streamlit and Ollama*")