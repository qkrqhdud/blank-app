import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer

@st.cache_resource
def load_model():
  tokenizer = AutoTokenizer.from_pretrained("unsloth/gemma-2-9b-it-bnb-4bit",use_auth_token='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')
  model = AutoModelForCausalLM.from_pretrained("unsloth/gemma-2-9b-it-bnb-4bit",use_auth_token='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')
  return tokenizer, model

tokenizer, model = load_model()

st.title("Gemma-2 데모")

prompt = st.text_input("프롬프트를 입력하세요.")
if st.button("생성"):
  inputs = tokenizer(prompt, return_tensors="pt")
  outputs = model.generate(**inputs)
  response = tokenizer.decode(outputs[0], skip_special_tokens=True)
  st.write(response)
