from sqlalchemy import Column, String, ForeignKey, Text, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Conversation(Base):
    __tablename__ = "conversations"
    conversation_id = Column(String(100), primary_key=True)
    agent_id = Column(String(100))
    project_id = Column(String(100))

    transcriptions = relationship("Transcription", back_populates="conversation")

class Transcription(Base):
    __tablename__ = "transcriptions"
    transcription_id = Column(String(100), primary_key=True)
    conversation_id = Column(String(100), ForeignKey("conversations.conversation_id"))
    transcript_text = Column(Text)
    diarized_segments = Column(JSONB)

    # ✅ Relationship to Conversation (you had `backref`, now fixed to `back_populates`)
    conversation = relationship("Conversation", back_populates="transcriptions")

class Keyword(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    keyword = Column(String, nullable=False)
