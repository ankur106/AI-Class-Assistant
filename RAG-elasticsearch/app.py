from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from tools.elastic_index import getEngine

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace '*' with specific origins like ["http://localhost:3000"] for security
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

hyde_query_engine = None
vector_store = None

@app.on_event("startup")
def setup():
    global hyde_query_engine, vector_store
    if hyde_query_engine is None or vector_store is None:
        hyde_query_engine, vector_store = getEngine()

@app.post("/query")
async def process_query(request: Request):
    data = await request.json()
    query = data.get("query")
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")

    async def generate():
        streaming_response = hyde_query_engine.query(query)
        for token in streaming_response.response_gen:
            yield token
            
    return StreamingResponse(generate(), media_type="text/plain")