from transformers import pipeline, AutoTokenizer

model_name = "unsloth/gemma-2-9b-it-bnb-4bit"
tokenizer = AutoTokenizer.from_pretrained(model_name,use_auth_token='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')
generator = pipeline("text-generation", model=model_name, tokenizer=tokenizer,use_auth_token='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')

def get_output(input):
  # 프롬프트
  post_prompt = """Please rate the following blog post from 1 to 10 on each of the following category: Topic "Relevance", "Value Provision", "Storytelling", "Expertise","Conciseness","Paragraph Structure","Attention-Grabbing Opening", "Call-to-Action (CTA)","Balance of Professionalism and Personal Touch" and "Hashtag Usage"
  Please also provide a brief comment explaining your score for each criterion.

  ### Input:
  {}

  ### Instruction:
  "Evaluate and Comment the blog post below and only provide the response."

  ### Response example:

  "category": "Topic Relevance",
  "score": 8,
  "explanation": "The post is relevant to LinkedIn's professional environment, focusing on company growth, leadership, and recruitment, which are commonly discussed topics in the business world.",
  "improvement_suggestion": "To enhance relevance, the post could explicitly connect these insights to broader industry trends or professional development topics, making it more universally appealing."

  ### Response:
  {}"""

  # 프롬프트 생성 및 모델 실행
  outputs = generator(post_prompt.format(
        post_input, # input
        ""# output - leave this blank for generation!
  ))
  generated_text = outputs[0]["generated_text"]
  response_start = generated_text[0].find("### Response:")
  if response_start != -1:
    ouput = generated_text[0][response_start + len("### Response:"):].strip()

  # 결과 출력
  return ouput
