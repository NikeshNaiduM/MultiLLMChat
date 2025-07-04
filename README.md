# MultiLLMChat 🤖

A sleek, modern chat interface for interacting with local Ollama models. Built with Streamlit, this application provides an intuitive way to chat with various Large Language Models running on your local machine.

## ✨ Features

- **🎯 Interactive Chat Interface**: Clean, responsive chat UI with streaming responses
- **🔌 Live Connection Status**: Real-time monitoring of Ollama service status
- **🎛️ Advanced Settings**: 
  - Customizable system prompts
  - Temperature control (0.0 - 2.0)
  - Token limit configuration
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices
- **⚡ Streaming Responses**: Real-time response generation with typing indicators
- **🗂️ Multiple Model Support**: Automatically detects and allows switching between available Ollama models
- **💾 Chat History**: Persistent conversation history during your session
- **🎨 Modern UI**: Custom styling with status indicators and smooth animations

## 🚀 Quick Start

### Prerequisites

1. **Install Ollama**: Download and install Ollama from [ollama.ai](https://ollama.ai)
2. **Python 3.7+**: Ensure you have Python installed on your system

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/NikeshNaiduM/MultiLLMChat.git
   cd MultiLLMChat
   ```

2. **Install dependencies**:
   ```bash
   pip install streamlit requests
   ```

3. **Start Ollama service**:
   ```bash
   ollama serve
   ```

4. **Download a model** (if you haven't already):
   ```bash
   ollama pull llama2        # or any other model you prefer
   ollama pull codellama     # for coding assistance
   ollama pull mistral       # lightweight alternative
   ```

5. **Run the application**:
   ```bash
   streamlit run DeepChatWin.py
   ```

6. **Open your browser**: The app will automatically open at `http://localhost:8501`

## 🎮 Usage

### Basic Chat
1. Select a model from the sidebar dropdown
2. Type your message in the chat input at the bottom
3. Press Enter to send and receive streaming responses

### Advanced Configuration
- **System Prompt**: Define the AI's behavior and personality
- **Temperature**: Control randomness (0.0 = deterministic, 2.0 = very creative)
- **Max Tokens**: Set the maximum response length

### Chat Management
- Use the "Clear Chat History" button to start fresh conversations
- Chat history persists during your session but resets when you refresh

## 🛠️ Technical Details

### Architecture
- **Frontend**: Streamlit with custom CSS styling
- **Backend**: Ollama API integration via HTTP requests
- **Streaming**: Real-time response streaming with chunk processing

### API Endpoints Used
- `GET /`: Health check for Ollama service
- `GET /api/tags`: Fetch available models
- `POST /api/generate`: Generate responses with streaming support

### Configuration Options
```python
# Default settings (customizable via UI)
temperature = 0.7          # Response randomness
max_tokens = 2000         # Maximum response length
system_prompt = "You are a helpful AI assistant."
```

## 🔧 Troubleshooting

### Common Issues

**"Ollama is not running"**
- Ensure Ollama is installed and running: `ollama serve`
- Check if the service is accessible at `http://localhost:11434`

**"No models found"**
- Download models using: `ollama pull <model-name>`
- Verify models are available: `ollama list`

**Connection timeout**
- Increase timeout in the code if needed
- Check firewall settings
- Ensure Ollama is running on the default port (11434)

**Model not found (404 error)**
- Verify the model name is correct
- Use `ollama list` to see available models
- Try pulling the model again: `ollama pull <model-name>`

## 📚 Supported Models

Any model available in Ollama can be used with this interface. Popular options include:

- **llama2**: Meta's Llama 2 model
- **codellama**: Specialized for code generation
- **mistral**: Efficient and capable model
- **dolphin-mistral**: Fine-tuned for conversation
- **neural-chat**: Optimized for dialogue
- **starling-lm**: Advanced reasoning capabilities

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai) for providing the local LLM runtime
- [Streamlit](https://streamlit.io) for the excellent web framework
- The open-source community for various model implementations

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/NikeshNaiduM/MultiLLMChat/issues) page
2. Create a new issue with detailed information
3. Include your OS, Python version, and error messages

---

**Made with ❤️ by [Nikesh Naidu](https://github.com/NikeshNaiduM)**

*Powered by Streamlit and Ollama*