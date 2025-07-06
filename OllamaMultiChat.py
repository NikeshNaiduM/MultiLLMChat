import chainlit as cl
import subprocess
from chainlit.input_widget import Select


def build_chat_profiles() -> list[cl.ChatProfile]:
    """Dynamically fetches Ollama model list using subprocess and builds ChatProfiles."""
    profiles = []
    try:
        # Run ollama list command and decode output
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
        output_lines = result.stdout.strip().splitlines()

        if len(output_lines) <= 1:
            raise ValueError("No models found in output.")

        # Skip header row and parse each model line
        for line in output_lines[1:]:
            if not line.strip():
                continue
            parts = line.split()
            model_name = parts[0]  # example: qwen2.5:latest

            generic_starters = [
                ("SQL Join", "Write a SQL query to join two tables"),
                ("Explain Like 5", "Explain superconductors like I'm five years old."),
            ]

            starters = [
                cl.Starter(
                    label=label,
                    message=msg,
                    icon=f"https://picsum.photos/seed/{model_name.replace(':', '_')}_{i}/200",
                )
                for i, (label, msg) in enumerate(generic_starters)
            ]

            profiles.append(
                cl.ChatProfile(
                    name=model_name,
                    markdown_description=f"The underlying LLM model is **{model_name}**.",
                    icon=f"https://picsum.photos/seed/{model_name.replace(':', '_')}/210",
                    starters=starters,
                )
            )

    except Exception as e:
        print(f"[ERROR] Failed to fetch models: {e}")
        profiles.append(
            cl.ChatProfile(
                name="no-models",
                markdown_description="No local Ollama models found or error occurred.",
                icon="https://picsum.photos/seed/empty/200",
                starters=[],
            )
        )

    return profiles


@cl.set_chat_profiles
async def chat_profile():
    return build_chat_profiles()


async def get_response_from_ollama(prompt: str) -> str:
    model_name = cl.user_session.get("chat_profile")

    if not model_name:
        return "No model selected. Please choose a profile from the sidebar."

    try:
        result = subprocess.run(
            ["ollama", "run", model_name, prompt],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"[Ollama Error] {e.stderr.strip()}"
    except Exception as e:
        return f"[Exception] {str(e)}"


async def tool(prompt: str) -> str:
    return await get_response_from_ollama(prompt)


@cl.on_message
async def main(message: cl.Message):
    waiting_msg = await cl.Message("Generating response...").send()
    response_text = await tool(message.content)
    waiting_msg.content = response_text
    await waiting_msg.update()
