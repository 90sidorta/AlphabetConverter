from fastapi import FastAPI

from app.avestan.routers import avestan_router
from app.scipt_families.routers import script_families_router
from app.alphabets.routers import alphabets_router

app = FastAPI(title="Alphabet Converter")

# Routers
app.include_router(
    script_families_router,
    tags=["ScriptFamily"],
    prefix="/api/script_family",
)
app.include_router(
    alphabets_router,
    tags=["Alphabet"],
    prefix="/api/alphabet",
)
app.include_router(
    avestan_router,
    tags=["Avestan"],
    prefix="/api/avestan",
)


@app.get("/")
async def root():
    return {"status": "ok"}
