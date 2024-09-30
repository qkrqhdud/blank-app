from transformers import pipeline
from unsloth import FastLanguageModel
import re

def load_model():
    finetune_model,tokenizer = FastLanguageModel.from_pretrained(
    model_name = "yunho123/lora_model", # YOUR MODEL YOU USED FOR TRAINING
    max_seq_length = 2048,
    dtype = None,
    load_in_4bit = True,
    )

    return finetune_model,tokenizer

def get_output(post_input,finetune_model,tokenizer):
  # 프롬프트
  post_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

  ### Input:
  {}

  ### Instruction:
  "Please rate the following blog post from 1 to 10 on each of the following category and provide a brief comment explaining your score for each criterion: "Topic Relevance", "Value Provision", "Storytelling", "Expertise","Conciseness","Paragraph Structure","Attention-Grabbing Opening", "Call-to-Action (CTA)","Balance of Professionalism and Personal Touch" and "Hashtag Usage"
   Please provide the output in the following format."

    "category": "Topic Relevance",
    "score": 5,
    "explanation": "comment",              
    "improvement_suggestion": "comment"   
    #next category
    "category": ,
    "score": ,
    "explanation": "comment",              
    "improvement_suggestion": "comment"   

    
  ### Response:
  {}"""
  inputs = tokenizer(
  [
      post_prompt.format(
          post_input,
          ""
      )
  ], return_tensors = "pt").to("cuda")

  outputs = tokenizer.batch_decode(finetune_model.generate(**inputs, max_new_tokens = 516, use_cache = True))

  response_start = outputs[0].find("### Response:")
  if response_start != -1:
    output = outputs[0][response_start+len("### Response:"):].strip()
    
  result = []
  matches = re.findall(r'"category":\s*"(.*?)",\s*\n\s*"score":\s*(.*?),\s*\n\s*"explanation":\s*"(.*?)",\s*\n\s*"improvement_suggestion":\s*"(.*?)"', output)

  for match in matches:
      category, score, explanation, improvement_suggestion = match
      result.append({"category": category, "score": int(score), "explanation": explanation, "improvement_suggestion": improvement_suggestion})


  # 결과 출력
  return result
