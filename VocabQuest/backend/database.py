from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float
from sqlalchemy.orm import declarative_base, sessionmaker
import os

Base = declarative_base()

class Word(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True)
    text = Column(String, unique=True, nullable=False)
    definition = Column(String)
    image_url = Column(String, nullable=True)
    difficulty = Column(Integer, default=3) # 1 (Easy) to 10 (Hard)
    word_type = Column(String, nullable=True)
    synonym = Column(String, nullable=True)

class MathQuestion(Base):
    __tablename__ = 'math_questions'
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False) # The question itself
    answer = Column(String, nullable=False) # The correct answer
    options = Column(String, nullable=True) # JSON string for multiple choice options (optional)
    difficulty = Column(Integer, default=3)
    topic = Column(String) # e.g., "Algebra", "Geometry", "Word Problem"

class UserStats(Base):
    __tablename__ = 'user_stats'
    id = Column(Integer, primary_key=True)
    current_level = Column(Integer, default=3) # Adaptive level
    total_score = Column(Integer, default=0)
    streak = Column(Integer, default=0)

# Init DB
db_path = os.path.join(os.path.dirname(__file__), 'vocab.db')
engine = create_engine(f'sqlite:///{db_path}', connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def migrate_db():
    """Simple migration to add missing columns if they don't exist."""
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
        conn.commit()

migrate_db()
