from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from sqlalchemy.orm import Session
from app.models import Transcription, Keyword
from database import TranscriptionSessionLocal
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Comparative Transcription Service",
    description="Compare diarization text with categorized keywords from DB",
    version="1.0.0"
)

class KeywordEntry(BaseModel):
    category: str
    keyword: str

def get_categorized_keywords(session: Session) -> Dict[str, List[str]]:
    keywords = session.query(Keyword).all()
    categorized = {}
    for kw in keywords:
        cat = kw.category.strip()
        val = kw.keyword.strip()
        if cat not in categorized:
            categorized[cat] = []
        categorized[cat].append(val)
    return categorized

#matching the keywords with the diarized text
@app.get("/Match_keywords/{conversation_id}", summary="Fetch diarization and matched categorized keywords")
def fetch_conversation(conversation_id: str):
    with TranscriptionSessionLocal() as session:
        try:
            transcription = session.query(Transcription).filter_by(conversation_id=conversation_id).first()

            if not transcription:
                raise HTTPException(status_code=404, detail="No transcription found for this conversation_id")

            if not transcription.conversation:
                raise HTTPException(status_code=404, detail="Conversation not linked")

            diarized_segments = transcription.diarized_segments or []
            if not isinstance(diarized_segments, list):
                raise HTTPException(status_code=400, detail="Invalid diarized_segments format")

            result = []

            categorized_keywords = get_categorized_keywords(session)

            for category, keywords in categorized_keywords.items():
                matched_keyword_data = []

                for keyword in keywords:
                    keyword_lower = keyword.casefold()
                    agent_count = 0
                    customer_count = 0
                    agent_texts = []
                    customer_texts = []

                    for segment in diarized_segments:
                        speaker = segment.get("speaker", "")
                        text = segment.get("text", "")
                        if not isinstance(text, str) or not isinstance(speaker, str):
                            continue

                        segment_text_lower = text.casefold()
                        speaker_lower = speaker.casefold()

                        if keyword_lower in segment_text_lower:
                            segment_entry = {"text": text, "speaker": speaker}
                            if "agent" in speaker_lower or speaker_lower == "speaker_0":
                                agent_count += 1
                                agent_texts.append(segment_entry)
                            elif "customer" in speaker_lower or speaker_lower == "speaker_1":
                                customer_count += 1
                                customer_texts.append(segment_entry)

                    matched_keyword_data.append({
                        "keyword": keyword,
                        "countBySpeaker": {
                            "Agent": {"count": agent_count, "text": agent_texts},
                            "Customer": {"count": customer_count, "text": customer_texts}
                        }
                    })

                result.append({
                    "category": category,
                    "keywords": matched_keyword_data
                })

            return {
                "agent_id": transcription.conversation.agent_id,
                "conversation_id": transcription.conversation_id,
                "project_id": transcription.conversation.project_id,
                "builder_name": "Working on it",
                "matched_Keywords": result,
                "diarized_text": diarized_segments
            }

        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            logger.exception("Unhandled error while processing fetch")
            raise HTTPException(status_code=500, detail="Internal server error")
#to list all the keywords in the database
@app.get("/Show_keywords", summary="List all keywords by category")
def list_keywords():
    with TranscriptionSessionLocal() as session:
        try:
            return {"keywords": get_categorized_keywords(session)}
        except Exception as e:
            logger.exception("Error while listing keywords")
            raise HTTPException(status_code=500, detail="Failed to retrieve keywords")
#adding the Keyword to The Database
@app.post("/Add_keywords", summary="Add a keyword to a category")
def add_keyword(entry: KeywordEntry):
    with TranscriptionSessionLocal() as session:
        try:
            existing = session.query(Keyword).filter(
                Keyword.category.ilike(entry.category.strip()),
                Keyword.keyword.ilike(entry.keyword.strip())
            ).first()

            if existing:
                raise HTTPException(status_code=400, detail="Keyword already exists in this category")

            keyword = Keyword(category=entry.category.strip(), keyword=entry.keyword.strip())
            session.add(keyword)
            session.commit()
            return {"message": "Keyword added successfully"}
        except Exception as e:
            logger.exception("Error adding keyword")
            raise HTTPException(status_code=500, detail="Failed to add keyword")
#deleting The Keyword from The Database
@app.delete("/Delete_keywords", summary="Delete a keyword from a category")
def delete_keyword(entry: KeywordEntry):
    with TranscriptionSessionLocal() as session:
        try:
            keyword = session.query(Keyword).filter(
                Keyword.category.ilike(entry.category.strip()),
                Keyword.keyword.ilike(entry.keyword.strip())
            ).first()

            if not keyword:
                raise HTTPException(status_code=404, detail="Keyword not found")

            session.delete(keyword)
            session.commit()
            return {"message": "Keyword deleted successfully"}
        except Exception as e:
            logger.exception("Error deleting keyword")
            raise HTTPException(status_code=500, detail="Failed to delete keyword")
