from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import os
import logging
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
    question_type = Column(String, default="Multiple Choice")

class ScoreHistory(Base):
    __tablename__ = 'score_history'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, default=1)
    score = Column(Integer, default=0)
    max_score = Column(Integer, default=0)
    mode = Column(String)
    timestamp = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    details = Column(Text, nullable=True)

class UserStats(Base):
    __tablename__ = 'user_stats'
    id = Column(Integer, primary_key=True)
    current_level = Column(Integer, default=3) # Global adaptive level
    total_score = Column(Integer, default=0)
    streak = Column(Integer, default=0)
    badges = Column(Text, default="[]") # JSON list of badges

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
    evidence_text = Column(String, nullable=True) # Exact evidence snippet

    passage = relationship("ComprehensionPassage", back_populates="questions")

class UserErrors(Base):
    __tablename__ = 'user_errors'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, default=1)
    question_id = Column(Integer, nullable=False)
    mode = Column(String, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))

class VerbalReasoningQuestion(Base):
    __tablename__ = 'verbal_reasoning_questions'
    id = Column(Integer, primary_key=True)
    question_type = Column(String, nullable=False) # e.g. "move_one_letter"
    question_text = Column(String, nullable=False)
    content = Column(Text, nullable=True) # JSON or text data needed for question
    options = Column(Text, nullable=True) # JSON options
    answer = Column(String, nullable=False)
    difficulty = Column(Integer, default=3)
    explanation = Column(Text, nullable=True)

# Init DB
db_path = os.path.join(os.path.dirname(__file__), 'vocab.db')
engine = create_engine(f'sqlite:///{db_path}', connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def migrate_db():
    """Simple migration to add missing columns/tables."""
    from sqlalchemy import text
    with engine.connect() as conn:
        # Check for word_type column
        try:
            conn.execute(text("SELECT word_type FROM words LIMIT 1"))
        except Exception:
            logging.info("Migrating: Adding word_type column...")
            conn.execute(text("ALTER TABLE words ADD COLUMN word_type VARCHAR"))

        # Check for synonym column
        try:
            conn.execute(text("SELECT synonym FROM words LIMIT 1"))
        except Exception:
            logging.info("Migrating: Adding synonym column...")
            conn.execute(text("ALTER TABLE words ADD COLUMN synonym VARCHAR"))

        try:
            conn.execute(text("SELECT explanation FROM math_questions LIMIT 1"))
        except Exception:
            logging.info("Migrating: Adding explanation column to math_questions...")
            conn.execute(text("ALTER TABLE math_questions ADD COLUMN explanation VARCHAR"))

        try:
            conn.execute(text("SELECT question_type FROM math_questions LIMIT 1"))
        except Exception:
            logging.info("Migrating: Adding question_type column to math_questions...")
            conn.execute(text("ALTER TABLE math_questions ADD COLUMN question_type VARCHAR DEFAULT 'Multiple Choice'"))

        # Create TopicProgress table if it doesn't exist
        try:
            conn.execute(text("SELECT mastery_level FROM topic_progress LIMIT 1"))
        except Exception:
            pass

        # Create Comprehension tables if they don't exist
        try:
            conn.execute(text("SELECT title FROM comprehension_passages LIMIT 1"))
        except Exception:
            # Tables are created by create_all, but this checks connectivity
            pass

        try:
            conn.execute(text("SELECT image_url FROM comprehension_passages LIMIT 1"))
        except Exception:
            logging.info("Migrating: Adding image_url column to comprehension_passages...")
            conn.execute(text("ALTER TABLE comprehension_passages ADD COLUMN image_url VARCHAR"))

        try:
            conn.execute(text("SELECT evidence_text FROM comprehension_questions LIMIT 1"))
        except Exception:
            logging.info("Migrating: Adding evidence_text column to comprehension_questions...")
            conn.execute(text("ALTER TABLE comprehension_questions ADD COLUMN evidence_text VARCHAR"))

        # Check for badges column
        try:
            conn.execute(text("SELECT badges FROM user_stats LIMIT 1"))
        except Exception:
            logging.info("Migrating: Adding badges column to user_stats...")
            conn.execute(text("ALTER TABLE user_stats ADD COLUMN badges TEXT DEFAULT '[]'"))

        # Create ScoreHistory table if it doesn't exist
        try:
            conn.execute(text("SELECT score FROM score_history LIMIT 1"))
        except Exception:
            # Table created by create_all usually, but here just in case
            pass

        # Create UserErrors table if it doesn't exist
        try:
            conn.execute(text("SELECT question_id FROM user_errors LIMIT 1"))
        except Exception:
             # If table doesn't exist, create it via metadata or raw SQL.
             # Since Base.metadata.create_all handles creation, this check is mostly for schema updates on existing DBs.
             # But if create_all ran before UserErrors was defined, we need to create it now.
             logging.info("Migrating: Creating user_errors table...")
             UserErrors.__table__.create(engine)

        conn.commit()

migrate_db()
