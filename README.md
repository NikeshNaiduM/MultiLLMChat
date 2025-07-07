# OllamaMultiChat

A modern, interactive chat application built with Chainlit that provides a seamless interface for chatting with local Ollama language models.

## Features

- **Dynamic Model Selection**: Automatically detects and creates chat profiles for all locally installed Ollama models
- **Interactive Chat Settings**: Real-time configuration panel with model selection, temperature control, streaming toggle, and system prompt customization
- **Streaming Support**: Real-time token streaming for responsive conversations
- **Chat Profiles**: Dedicated profiles for each model with custom icons and starter prompts
- **Toast Notifications**: User-friendly feedback for setting updates and model loading
- **Windows Compatible**: UTF-8 safe encoding for cross-platform compatibility

## Prerequisites

- **Ollama**: Must be installed and running on your system
  - Download from: https://ollama.com/
  - Ensure you have at least one model installed (e.g., `ollama pull llama2`)
- **Python 3.7+**

## Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify Ollama installation**:
   ```bash
   ollama list
   ```
   This should show your installed models.

## Usage

1. **Start the application**:
   ```bash
   chainlit run OllamaMultiChat.py
   ```

2. **Open your browser** and navigate to the URL shown in the terminal (typically `http://localhost:8000`)

3. **Select a model** from the chat profiles or use the settings panel to configure:
   - **Model**: Choose from your locally installed Ollama models
   - **Temperature**: Control randomness (0.0 = deterministic, 1.0 = creative)
   - **Streaming**: Enable/disable real-time token streaming
   - **System Prompt**: Optional system-level instructions for the model

4. **Start chatting** with your selected model!

## Chat Settings

The application provides a comprehensive settings panel:

- **Model Selection**: Switch between any locally installed Ollama models
- **Temperature Control**: Slider from 0.0 to 1.0 for output randomness
- **Streaming Toggle**: Enable for real-time response streaming
- **System Prompt**: Add custom system instructions (optional)

## Starter Prompts

Each model profile comes with built-in starter prompts:
- **SQL Join**: "Write a SQL query to join two tables"
- **Explain Like 5**: "Explain superconductors like I'm five years old."

## Troubleshooting

**No models detected:**
- Ensure Ollama is installed and running
- Verify models are installed with `ollama list`
- Try pulling a model: `ollama pull llama2`

**Connection issues:**
- Check if Ollama service is running
- Verify firewall settings
- Ensure port 11434 (default Ollama port) is available

**UTF-8 encoding errors:**
- The application handles Windows UTF-8 encoding automatically
- If issues persist, check your system locale settings

## Architecture

The application consists of several key components:

- **Model Detection**: Automatically scans for local Ollama models
- **Chat Profiles**: Dynamic profile generation for each model
- **Settings Management**: Real-time settings persistence and updates
- **Streaming Handler**: Asynchronous token streaming for responsive chat
- **Error Handling**: Graceful error management with user feedback

## Development

To modify or extend the application:

1. The main chat logic is in the `@cl.on_message` handler
2. Model detection happens in `list_local_models()`
3. Chat profiles are built in `build_chat_profiles()`
4. Settings are managed in `@cl.on_settings_update`

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application.

## License

This project is open source. Please check the license file for details.
