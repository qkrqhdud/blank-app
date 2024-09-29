import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login

login(token='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')

@st.cache_resource
def load_model():
  model_name = "unsloth/gemma-2-9b-it-bnb-4bit"
  tokenizer = AutoTokenizer.from_pretrained(model_name)
  generator = pipeline("text-generation", model=model_name, tokenizer=tokenizer)
  return tokenizer, model

tokenizer, model = load_model()

st.title("Gemma-2 데모")

prompt = st.text_input("프롬프트를 입력하세요.")
if st.button("생성"):
  inputs = tokenizer(prompt, return_tensors="pt")
  outputs = model.generate(**inputs)
  response = tokenizer.decode(outputs[0], skip_special_tokens=True)
  st.write(response)
