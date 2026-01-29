from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import os
import datetime

Base = declarative_base()

class Word(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True)
    text = Column(String, unique=True, nullable=False)
    definition = Column(String)
    image_url = Column(String, nullable=True)
    difficulty = Column(Integer, default=3)
    word_type = Column(String, nullable=True)
    synonym = Column(String, nullable=True)

class MathQuestion(Base):
    __tablename__ = 'math_questions'
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    options = Column(String, nullable=True) # JSON string for MCQ
    difficulty = Column(Integer, default=3)
    topic = Column(String) # e.g., "Algebra", "Fractions"
    explanation = Column(String, nullable=True)

class UserStats(Base):
    __tablename__ = 'user_stats'
    id = Column(Integer, primary_key=True)
    current_level = Column(Integer, default=3) # Global adaptive level
    total_score = Column(Integer, default=0)
    streak = Column(Integer, default=0)
    badges = Column(Text, default="[]") # JSON list of badges

class ScoreHistory(Base):
    __tablename__ = 'score_history'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, default=1)
    score = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    mode = Column(String, nullable=True)

class TopicProgress(Base):
    __tablename__ = 'topic_progress'
    id = Column(Integer, primary_key=True)
    topic = Column(String, unique=True, nullable=False)
    mastery_level = Column(Integer, default=1) # 1 to 10
    questions_answered = Column(Integer, default=0)
    questions_correct = Column(Integer, default=0)

class ComprehensionPassage(Base):
    __tablename__ = 'comprehension_passages'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    topic = Column(String) # e.g., "English Classical", "Sports"
    image_url = Column(String, nullable=True)

    questions = relationship("ComprehensionQuestion", back_populates="passage")

class ComprehensionQuestion(Base):
    __tablename__ = 'comprehension_questions'
    id = Column(Integer, primary_key=True)
    passage_id = Column(Integer, ForeignKey('comprehension_passages.id'))
    question_text = Column(String, nullable=False)
    options = Column(String, nullable=False) # JSON string of options
    correct_answer = Column(String, nullable=False)
    explanation = Column(String, nullable=True) # Evidence from text

    passage = relationship("ComprehensionPassage", back_populates="questions")

# Init DB
db_path = os.path.join(os.path.dirname(__file__), 'vocab.db')
engine = create_engine(f'sqlite:///{db_path}', connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
