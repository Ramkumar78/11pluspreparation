from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import os

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

class TopicProgress(Base):
    __tablename__ = 'topic_progress'
    id = Column(Integer, primary_key=True)
    topic = Column(String, unique=True, nullable=False)
    mastery_level = Column(Integer, default=1) # 1 to 10
    questions_answered = Column(Integer, default=0)
    questions_correct = Column(Integer, default=0)

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
            print("Migrating: Adding word_type column...")
            conn.execute(text("ALTER TABLE words ADD COLUMN word_type VARCHAR"))

        # Check for synonym column
        try:
            conn.execute(text("SELECT synonym FROM words LIMIT 1"))
        except Exception:
            print("Migrating: Adding synonym column...")
            conn.execute(text("ALTER TABLE words ADD COLUMN synonym VARCHAR"))

        try:
            conn.execute(text("SELECT explanation FROM math_questions LIMIT 1"))
        except Exception:
            print("Migrating: Adding explanation column to math_questions...")
            conn.execute(text("ALTER TABLE math_questions ADD COLUMN explanation VARCHAR"))

        # Create TopicProgress table if it doesn't exist (handled by create_all usually, but good for safety)
        try:
            conn.execute(text("SELECT mastery_level FROM topic_progress LIMIT 1"))
        except Exception:
            # Table creation is usually handled by Base.metadata.create_all,
            # but this block ensures safety if adding to existing DB file
            pass

        conn.commit()

migrate_db()
