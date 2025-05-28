from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from rag import ShopManualRAG

app = FastAPI(title="RAG API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG system
rag = ShopManualRAG()

class Query(BaseModel):
    text: str
    num_docs: Optional[int] = 3

class QueryResponse(BaseModel):
    answer: str
    relevant_docs: List[str]

@app.post("/query", response_model=QueryResponse)
async def query_manuals(query: Query):
    try:
        # Get the answer
        answer = rag.query(query.text)
        
        # Get relevant document snippets
        relevant_docs = rag.get_relevant_documents(query.text, query.num_docs)
        
        return QueryResponse(
            answer=answer,
            relevant_docs=relevant_docs
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "index_loaded": rag.index is not None}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 