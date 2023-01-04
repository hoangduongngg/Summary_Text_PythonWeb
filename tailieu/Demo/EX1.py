import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config

model=T5ForConditionalGeneration.from_pretrained('t5-small')
tokenizer=T5Tokenizer.from_pretrained('t5-small')
device=torch.device('cpu')

text="""
Artificial intelligence AI is intelligence demonstrated by machines as opposed to the natural intelligence displayed by humans or animals Leading AI textbooks define the field as the study of intelligent agents any system that perceives its environment and takes actions that maximize its chance of achieving its goals a Some popular accounts use the term artificial intelligence to describe machines that mimic cognitive functions that humans associate with the human mind such as learning and prob
"""

preprocessed_text=text.strip().replace('\n','')
t5_input_text='summarize: ' + preprocessed_text
print(t5_input_text)

tokenized_text=tokenizer.encode(t5_input_text, return_tensors='pt', max_length=512).to(device)

summary_ids=model.generate(tokenized_text, min_length=30, max_length=120)
summary=tokenizer.decode(summary_ids[0], skip_special_tokens=True)

print(summary)