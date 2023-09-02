from fastapi import FastAPI, Request, status
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

import pke
import re

import datetime

class Source(BaseModel):
    base_text: str

# トークナイザーとモデルの準備
#tokenizer = AutoTokenizer.from_pretrained('sonoisa/t5-base-japanese')
#model = AutoModelForSeq2SeqLM.from_pretrained('/output/')

app = FastAPI()

# CORSを回避するために追加（今回の肝）
app.add_middleware(GZipMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)

f = open('log.txt', 'a')

def write_log(log_text):
    dt_now = datetime.datetime.now()
    datetime_str = dt_now.strftime('%Y/%m/%d %H:%M:%S')
    f = open('log.txt', 'a')
    f.write(datetime_str + " " + log_text + "\r\n")
    f.close()

@app.exception_handler(RequestValidationError)
async def handler(request:Request, exc:RequestValidationError):
    print(exc)
    return JSONResponse(content={}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.get("/")
def index():
    f = open('log.txt', 'w')
    f.write('get')
    f.close()
    return {'summary_text':'hello'}

@app.post("/")
def summary(data: Source):
#def summary():
    write_log("post")
    write_log(data.base_text)

    # テキストをテンソルに変換
    input = tokenizer.encode(data.base_text.lower(), return_tensors='pt', max_length=512, truncation=True)

    write_log("eval start")
    # 推論
    model.eval()
    with torch.no_grad():
        summary_ids = model.generate(input, max_new_tokens=2048)
        summary_text = tokenizer.decode(summary_ids[0])

    keyword_array = []

    write_log("keyword start")

    extractor = pke.unsupervised.MultipartiteRank()
    # language='ja' とする
    extractor.load_document(input=data.base_text, language='ja', normalization=None)
    extractor.candidate_selection(pos={'NOUN', 'PROPN'})
    extractor.candidate_weighting(threshold=0.74, method='average', alpha=1.1)
    for best in extractor.get_n_best(5):
        m = re.search(r'\'.*\'', best.__str__())
        keyword_array.append(m.group().replace('\'',''))

    return {'summary_text': summary_text, 'keyword_array': keyword_array}
