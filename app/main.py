from fastapi import FastAPI

app = FastAPI(title="Alphabet Converter")


@app.get("/")
async def root():
    return {"status": "ok"}
