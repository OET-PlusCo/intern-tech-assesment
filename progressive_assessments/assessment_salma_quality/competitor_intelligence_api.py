"""
Competitor Intelligence API  –  v1.2.0
======================================
An AI-powered competitor analysis service used daily by strategic analysts
to track competitors in the fertilizer and agriculture sector.

Your task (DO NOT fix the code — test it and document what you find):
  1. Write a test plan BEFORE running anything
  2. Run the API and explore it using the exploration script or Postman/curl
  3. Document every issue as a proper bug report
  4. BONUS: write automated regression tests for the issues you found

Time: ~20 minutes
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import random
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Competitor Intelligence API",
    description="AI-powered competitor analysis for strategic decision-making",
    version="1.2.0",
)

# ──────────────────────────────────────────────────────────────
# Internal Knowledge Base  (simulates a retrieval / RAG store)
# ──────────────────────────────────────────────────────────────

COMPETITOR_DATABASE = {
    "PhosphoTech": {
        "market_share": 23.4,
        "key_products": ["PhosMax Pro", "NitroBoost", "AgroShield"],
        "recent_moves": "Launched PhosMax Pro in MENA region Q3 2026",
        "pricing_tier": "premium",
        "headquarters": "Amsterdam, Netherlands",
    },
    "AgriGlobal": {
        "market_share": 18.7,
        "key_products": ["GrowFast", "SoilGuard", "RainMaker"],
        "recent_moves": "Partnership with FarmTech announced October 2026",
        "pricing_tier": "mid-market",
        "headquarters": "São Paulo, Brazil",
    },
    "NutriCorp": {
        "market_share": 15.2,
        "key_products": ["NutriMax", "FieldFlex", "CropBoost"],
        "recent_moves": "Expanding to West Africa Q4 2026",
        "pricing_tier": "budget",
        "headquarters": "Nairobi, Kenya",
    },
}


# ──────────────────────────────────────────────────────────────
# AI Engine  (mock LLM-based analysis)
# ──────────────────────────────────────────────────────────────

def generate_analysis(query: str, competitor: str, response_format: str = "detailed") -> dict:
    """
    Simulates LLM-generated competitor analysis.
    Returns structured insights based on the query and competitor name.
    """

    # ── BUG #2: Silent failure on unknown competitor ─────────────────────────
    # When the competitor is not in the knowledge base the function returns
    # an empty success payload instead of raising an error.
    # Callers receive HTTP 200 with blank data and no indication of failure.
    if competitor not in COMPETITOR_DATABASE:
        return {
            "summary": "",
            "insights": [],
            "confidence": 0.0,
            "data_source": "knowledge_base",
        }
    # ─────────────────────────────────────────────────────────────────────────

    data = COMPETITOR_DATABASE[competitor]

    # Build insights based on detected query intent
    query_lower = query.lower()
    if any(w in query_lower for w in ["recent", "news", "move", "launch", "announce"]):
        insights = [
            data["recent_moves"],
            "Source: Internal market intelligence, updated November 2026",
        ]
    elif any(w in query_lower for w in ["product", "portfolio", "offering"]):
        insights = [
            f"Core product portfolio: {', '.join(data['key_products'])}",
            f"Market positioning: {data['pricing_tier'].title()} segment",
        ]
    elif any(w in query_lower for w in ["price", "pricing", "cost", "tier"]):
        insights = [
            f"Pricing tier: {data['pricing_tier'].title()}",
            f"Competing in {data['market_share']}% of the market",
        ]
    else:
        insights = [
            f"Market share: {data['market_share']}% of global fertilizer market",
            data["recent_moves"],
            f"Headquartered in {data['headquarters']}",
        ]

    # ── BUG #1: Data corruption in "brief" format ────────────────────────────
    # In "brief" mode the display name is randomly replaced with a *different*
    # competitor's name.  Analysts reading the brief summary see the wrong
    # company name, while the underlying data (market share, insights) belongs
    # to the requested competitor.
    if response_format == "brief":
        others = [c for c in COMPETITOR_DATABASE if c != competitor]
        wrong_name = random.choice(others)              # BUG: should be `competitor`
        summary = (
            f"{wrong_name} holds {data['market_share']}% market share "
            f"in the global fertilizer sector."
        )
    else:
        summary = (
            f"{competitor} holds {data['market_share']}% market share "
            f"in the global fertilizer sector."
        )
    # ─────────────────────────────────────────────────────────────────────────

    # ── BUG #3: Non-reproducible confidence score ────────────────────────────
    # Confidence is re-generated randomly on every call.
    # The same query run twice will produce different confidence values,
    # making it impossible to reproduce user-reported issues or track quality.
    confidence = round(random.uniform(0.60, 0.98), 2)
    # ─────────────────────────────────────────────────────────────────────────

    return {
        "summary": summary,
        "insights": insights,
        "confidence": confidence,
        "data_source": "knowledge_base",
    }


# ──────────────────────────────────────────────────────────────
# Request / Response Models
# ──────────────────────────────────────────────────────────────

class AnalysisRequest(BaseModel):
    query: str
    competitor: str
    # ── BUG #4: No validation on `format` ────────────────────────────────────
    # The field accepts any arbitrary string.  Passing "executive", "quick",
    # or "BRIEF" silently falls through to "detailed" behaviour with no warning.
    # API consumers don't know their format preference was ignored.
    format: str = "detailed"
    # ─────────────────────────────────────────────────────────────────────────
    analyst_id: Optional[str] = None


class AnalysisResponse(BaseModel):
    competitor: str
    query: str
    summary: str
    insights: List[str]
    confidence: float
    format: str
    generated_at: str


class BatchAnalysisRequest(BaseModel):
    queries: List[AnalysisRequest]


# ──────────────────────────────────────────────────────────────
# Endpoints
# ──────────────────────────────────────────────────────────────

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_competitor(request: AnalysisRequest):
    """
    Generate AI-powered analysis for a competitor based on a natural language query.

    - **query**: What you want to know (e.g. "What are their recent moves?")
    - **competitor**: Competitor name — use GET /competitors to list valid values
    - **format**: "detailed" (default) or "brief"
    - **analyst_id**: Optional tracking identifier
    """
    try:
        result = generate_analysis(request.query, request.competitor, request.format)

        return AnalysisResponse(
            competitor=request.competitor,
            query=request.query,
            summary=result["summary"],
            insights=result["insights"],
            confidence=result["confidence"],
            format=request.format,
            generated_at=datetime.now().isoformat(),
        )

    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/batch")
async def analyze_batch(request: BatchAnalysisRequest):
    """
    Analyze multiple competitors in a single request.
    Useful for generating comparison reports across all tracked competitors.
    """
    results = []

    for q in request.queries:
        result = generate_analysis(q.query, q.competitor, q.format)
        results.append(
            {
                "competitor": q.competitor,
                "query": q.query,
                "summary": result["summary"],
                "insights": result["insights"],
                "confidence": result["confidence"],
                "format": q.format,
                "generated_at": datetime.now().isoformat(),
            }
        )

    return {"analyses": results, "total": len(results)}


@app.get("/competitors")
async def list_competitors():
    """List all competitors available in the knowledge base."""
    return {
        "competitors": list(COMPETITOR_DATABASE.keys()),
        "total": len(COMPETITOR_DATABASE),
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.2.0",
        "knowledge_base_entries": len(COMPETITOR_DATABASE),
    }


@app.get("/")
async def root():
    return {
        "api": "Competitor Intelligence API",
        "version": "1.2.0",
        "docs": "/docs",
        "endpoints": {
            "analyze": "POST /analyze",
            "batch_analyze": "POST /analyze/batch",
            "list_competitors": "GET /competitors",
            "health": "GET /health",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
