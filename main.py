from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
import gradio as gr
from dotenv import load_dotenv

load_dotenv()

# Model: Qwen/Qwen2.5-72B-Instruct | Provider: huggingface

prompt_template_str = """
Given the English word {word}, create a sentence in {language} using this word.

The sentence should:
1. Contain up to 8 words.
2. Use simple vocabulary and grammar for a language learner.
3. Be direct and useful to focus on the English word meaning.
4. Be realistic.

Do not include the English phrase.
"""

prompt_template = PromptTemplate.from_template(prompt_template_str)

_llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-72B-Instruct",
    task="text-generation",
)
model = ChatHuggingFace(llm=_llm)

def generate_phrase(word, language):
  if not word or not word.strip():
    return "Please enter an English word."

  prompt = prompt_template.format(word=word.strip(), language=language)

  response = model.invoke(prompt)

  return response.text

demo = gr.Interface(
  fn=generate_phrase,
  inputs=[
    gr.Textbox(label="English word", lines=1),
    gr.Dropdown(
      choices=["Spanish", "French", "German", "Korean", "Japanese", "Portuguese"],
      label="Target Language",
      value="Korean"
    )
  ],
  outputs=[gr.Textbox(label="Phrase", lines=3)],
  flagging_mode="never",
  title="Contextify",
  description="Enter an English word and get a simple contextual phrase in another language"
)

demo.launch()
