from typing import Optional
import asyncio

from fastapi import FastAPI
from pydantic import BaseModel

from categorizer.classifier import EmailClassifier
from utils.url_checker import (
    check_url,
    extract_urls,
    URLCheckResult,
)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Email Secure API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

classifier = EmailClassifier()


class ClassifyRequest(BaseModel):
    sender: str
    subject: str
    body: str = ""
    has_attachment: bool = False
    attachment_ext: Optional[str] = None

class CheckUrlRequest(BaseModel):
    url: str

@app.get("/health")
def health():
    return {
        "status": "ok"
    }

@app.post("/check-url")
async def check_single_url(
    request: CheckUrlRequest):

        result = await check_url(
            request.url
        )

        return {
            "url": result.url,
            "is_safe": result.is_safe,
            "threat_type": result.threat_type,
            "confidence": result.confidence,
            "reasons": result.reasons,
        }

@app.post("/classify")
async def classify_email(request: ClassifyRequest):

    urls = extract_urls(
        request.body
    )
    result = classifier.classify(
        sender=request.sender,
        subject=request.subject,
        body=request.body,
        has_attachment=request.has_attachment,
        attachment_ext=request.attachment_ext,
    )

    if urls:

        url_checks = await asyncio.gather(

            *[
                check_url(url)
                for url in urls
            ]

        )

    else:

        url_checks = []

    return {

        # ---------- NEW ----------

        "brand": result.brand,

        "intent": result.intent,

        "category_score": result.category_score,
        
        "risk_label": result.risk_label,

        "url_results": [

            {

                "url": u.url,

                "is_safe": u.is_safe,

                "threat_type": u.threat_type,

                "confidence": u.confidence,

                "reasons": u.reasons,

            }

            for u in url_checks

        ],

        # ---------- EXISTING ----------

        "primary": {

            "id": result.primary.category.id,

            "name": result.primary.category.name,

            "color": result.primary.category.color,

            "text_color": result.primary.category.text_color,

            "priority": result.primary.category.priority.value,

            "confidence": result.primary.confidence,

            "matched_keywords": result.primary.matched_keywords,

            "matched_sender": result.primary.matched_sender,

            "matched_subject": result.primary.matched_subject,

        },

        "all_matches": [

            {

                "id": match.category.id,

                "name": match.category.name,

                "color": match.category.color,

                "text_color": match.category.text_color,

                "priority": match.category.priority.value,

                "confidence": match.confidence,

                "matched_keywords": match.matched_keywords,

                "matched_sender": match.matched_sender,

                "matched_subject": match.matched_subject,

            }

            for match in result.all_matches

        ]

    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )