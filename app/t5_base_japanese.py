from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

# トークナイザーとモデルの準備
tokenizer = AutoTokenizer.from_pretrained('sonoisa/t5-base-japanese')
#model = AutoModelForSeq2SeqLM.from_pretrained('/output/')
