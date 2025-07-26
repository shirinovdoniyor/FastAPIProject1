from fastapi import FastAPI
from pydantic import BaseModel
from collections import Counter
import re

app = FastAPI()

class InputText(BaseModel):
    text: str

class OutputResult(BaseModel):
    result: str
    explanation: str

def split_sentences(text: str):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s for s in sentences if len(s.strip()) > 3]

def analyze_topic_count(text: str) -> OutputResult:
    sentences = split_sentences(text)

    if len(sentences) == 0:
        return OutputResult(result="aniqlanmadi", explanation="Jumlalar ajratishda xatolik.")

    all_words = []
    for sentence in sentences:
        words = re.findall(r'\b\w{4,}\b', sentence.lower())
        all_words.extend(words)

    freq = Counter(all_words).most_common(5)
    main_keywords = [word for word, _ in freq]

    if len(sentences) == 1 or len(main_keywords) <= 2:
        return OutputResult(result="birlik", explanation="")
    else:
        return OutputResult(result="ko‘plik", explanation=f"")

@app.post("/check", response_model=OutputResult)
async def check_text(input_text: InputText):
    return analyze_topic_count(input_text.text)

@app.get("/")
def root():
    return {"message": "Mavzular sonini aniqlovchi API ishga tushdi!"}


