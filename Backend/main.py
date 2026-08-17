from fastapi import FastAPI
app = FastAPI(title="CreatorPulse AI")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}