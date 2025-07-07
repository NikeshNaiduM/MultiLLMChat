import asyncio
import subprocess
from typing import List

import chainlit as cl
from chainlit.input_widget import Select, Slider, Switch, TextInput

"""Ollama × Chainlit chat app with:
- Dynamic ChatProfiles per local model
- Chat Settings panel (model, temperature, streaming, system prompt)
- Async streaming of tokens
- Toast notifications for user feedback
- Windows‑safe UTF‑8 decoding for all subprocess output
"""

# --------------------------------------------------
# Utils
# --------------------------------------------------

def list_local_models() -> List[str]:
    """Return the list of local Ollama model names ("ollama list")."""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        )
        lines = result.stdout.strip().splitlines()
        # Skip header row
        return [line.split()[0] for line in lines[1:] if line.strip()]
    except Exception as e:
        print(f"[ERROR] Could not list Ollama models: {e}")
        return []


# --------------------------------------------------
# Chat Profiles
# --------------------------------------------------

def build_chat_profiles() -> List[cl.ChatProfile]:
    """Build a Chainlit ChatProfile for every local Ollama model."""
    models = list_local_models()

    starters_tpl = [
        ("SQL Join", "Write a SQL query to join two tables"),
        ("Explain Like 5", "Explain superconductors like I'm five years old."),
    ]

    if not models:
        return [
            cl.ChatProfile(
                name="no-models",
                markdown_description="No local Ollama models found.",
                icon="https://picsum.photos/seed/empty/210",
            )
        ]

    profiles: List[cl.ChatProfile] = []
    for model in models:
        starters = [
            cl.Starter(
                label=label,
                message=msg,
                icon=f"https://picsum.photos/seed/{model.replace(':','_')}_{i}/200",
            )
            for i, (label, msg) in enumerate(starters_tpl)
        ]
        profiles.append(
            cl.ChatProfile(
                name=model,
                markdown_description=f"**{model}** running through Ollama.",
                icon=f"https://picsum.photos/seed/{model.replace(':','_')}/210",
                starters=starters,
            )
        )
    return profiles


@cl.set_chat_profiles
async def chat_profile():
    return build_chat_profiles()


# --------------------------------------------------
# Ollama call helpers
# --------------------------------------------------

async def run_ollama(model: str, prompt: str, stream: bool):
    """Run Ollama with the chosen model and prompt. Stream tokens if requested."""
    if stream:
        proc = await asyncio.create_subprocess_exec(
            "ollama",
            "run",
            model,
            prompt,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        msg = cl.Message(content="")
        buffer = b""
        while True:
            chunk = await proc.stdout.read(1)
            if not chunk:
                break
            buffer += chunk
            if chunk in b" \n":
                await msg.stream_token(buffer.decode("utf-8", errors="ignore"))
                buffer = b""
        if buffer:
            await msg.stream_token(buffer.decode("utf-8", errors="ignore"))
        await proc.wait()
        if proc.returncode != 0:
            stderr = (
                await proc.stderr.read()
            ).decode("utf-8", errors="ignore").strip()
            await msg.update(content=f"[Ollama Error] {stderr}")
        else:
            await msg.send()
    else:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        content = (
            result.stdout.strip()
            if result.returncode == 0
            else f"[Ollama Error] {result.stderr.strip()}"
        )
        await cl.Message(content).send()


# --------------------------------------------------
# Chat Life‑Cycle Hooks
# --------------------------------------------------

@cl.on_chat_start
async def start_chat():
    """Create settings panel & greet user."""
    models = list_local_models()
    if not models:
        await cl.Message("⚠️ No local Ollama models detected.").send()
        return

    default_settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="Ollama Model",
                values=models,
                initial_index=0,
                tooltip="Select the Ollama model to chat with.",
            ),
            Slider(
                id="Temperature",
                label="Temperature",
                initial=0.7,
                min=0.0,
                max=1.0,
                step=0.1,
                tooltip="Controls randomness of the model output.",
            ),
            Switch(
                id="Streaming",
                label="Stream Tokens",
                initial=True,
            ),
            TextInput(
                id="SystemPrompt",
                label="System Prompt (optional)",
                initial="",
            ),
        ]
    ).send()

    # Persist in session
    cl.user_session.set("settings", default_settings)
    cl.user_session.set("chat_profile", default_settings["Model"])

    # Toast feedback
    await cl.context.emitter.emit(
        "ui:toast",
        {
            "title": "Model Loaded",
            "description": f"You are now chatting with {default_settings['Model']}",
            "type": "success",
        },
    )

    await cl.Message(
        content=f"👋 Hi! I'm **{default_settings['Model']}**. Ask me anything!",
    ).send()


@cl.on_settings_update
async def handle_settings_update(settings):
    """Store updated settings and notify user."""
    cl.user_session.set("settings", settings)
    cl.user_session.set("chat_profile", settings["Model"])

    await cl.context.emitter.emit(
        "ui:toast",
        {
            "title": "Settings Updated",
            "description": "Your preferences have been saved.",
            "type": "success",
        },
    )


@cl.on_message
async def main(message: cl.Message):
    settings = cl.user_session.get("settings") or {}
    model = settings.get("Model") or cl.user_session.get("chat_profile")
    stream = settings.get("Streaming", True)
    system_prompt = settings.get("SystemPrompt", "").strip()

    prompt = f"{system_prompt}\n{message.content}" if system_prompt else message.content

    await run_ollama(model, prompt, stream)
