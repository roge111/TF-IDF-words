from FileProcessing import FileProcessing
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

file_process = FileProcessing()

@app.get("/")
def root():
    return FileResponse('frontend/index.html')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

@app.post("/tf_idf")
async def file_processing(file: UploadFile = File(...)):
    # Передаем файл напрямую в функцию tfidf
    tf, idf = file_process.tfidf(file)
    
    word_info = {}
    for key in tf:
        word_info[key] = {
            'tf': tf[key],
            'idf': idf[key]
        }
    
    return dict(list(sorted(word_info.items(), key=lambda x: x[1]['idf'], reverse=True))[:50])
