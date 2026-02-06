import json
from sqlalchemy import text
from database import Session, engine, Word, UserStats, MathQuestion, TopicProgress, ComprehensionPassage, ComprehensionQuestion
import logging
from seed_list import WORD_LIST
from math_seed import MATH_LIST
from comprehension_seed import COMPREHENSION_LIST

def migrate_db():
    """Simple migration to add missing columns/tables."""
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
            print("Migrating: Adding image_url column to comprehension_passages...")
            conn.execute(text("ALTER TABLE comprehension_passages ADD COLUMN image_url VARCHAR"))

        # Check for badges column
        try:
            conn.execute(text("SELECT badges FROM user_stats LIMIT 1"))
        except Exception:
            print("Migrating: Adding badges column to user_stats...")
            conn.execute(text("ALTER TABLE user_stats ADD COLUMN badges TEXT DEFAULT '[]'"))

        conn.commit()

def init_db():
    # Run migrations first
    migrate_db()

    session = Session()
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_database():
    session = Session()
    logger.info("Starting database seeding...")

    # 1. Init User Stats if not exists
    if not session.query(UserStats).first():
        session.add(UserStats(current_level=3, total_score=0, streak=0))

    # 2. Seed Words (Standard logic)
    existing_words = {word.text: word for word in session.query(Word).all()}
    for w in WORD_LIST:
        existing_word = existing_words.get(w["text"])
        w_type = w.get("type")
        if isinstance(w_type, list):
            w_type = ", ".join(w_type)

        if existing_word:
            existing_word.difficulty = w["diff"]
            existing_word.definition = w["def"]
            existing_word.word_type = w_type
            existing_word.synonym = w.get("synonym")
        else:
            session.add(Word(
                text=w["text"],
                difficulty=w["diff"],
                definition=w["def"],
                word_type=w_type,
                synonym=w.get("synonym")
            ))

    # 3. Seed Math Questions
    print("Seeding Math Questions...")
    logger.info("Seeding Math Questions...")
    existing_math = {m.text: m for m in session.query(MathQuestion).all()}

    # Track topics for TopicProgress init
    unique_topics = set()

    for m in MATH_LIST:
        unique_topics.add(m["topic"])
        existing_q = existing_math.get(m["text"])
        if existing_q:
            existing_q.answer = m["answer"]
            existing_q.difficulty = m["diff"]
            existing_q.topic = m["topic"]
            existing_q.explanation = m.get("explanation", "")
        else:
            session.add(MathQuestion(
                text=m["text"],
                answer=m["answer"],
                difficulty=m["diff"],
                topic=m["topic"],
                explanation=m.get("explanation", "")
            ))

    # 4. Init Topic Progress for new topics
    existing_progress = {p.topic: p for p in session.query(TopicProgress).all()}
    for topic in unique_topics:
        if topic not in existing_progress:
            session.add(TopicProgress(topic=topic, mastery_level=1))

    if "Mental Maths" not in existing_progress:
        session.add(TopicProgress(topic="Mental Maths", mastery_level=1))

    # 5. Seed Comprehension Passages
    print("Seeding Comprehension Passages...")
    logger.info("Seeding Comprehension Passages...")
    existing_passages = {p.title: p for p in session.query(ComprehensionPassage).all()}

    for c in COMPREHENSION_LIST:
        passage = existing_passages.get(c["title"])
        if not passage:
            passage = ComprehensionPassage(
                title=c["title"],
                content=c["content"],
                topic=c["topic"]
            )
            session.add(passage)
            session.flush() # Flush to get the ID for questions
        else:
            # Update content/topic if needed
            passage.content = c["content"]
            passage.topic = c["topic"]

        # Seed Questions for this passage
        # Simple check: delete existing and re-add or check by text. Re-adding is safer for updates.
        # For simplicity in this script, we'll check by text.
        existing_qs = {q.question_text: q for q in session.query(ComprehensionQuestion).filter_by(passage_id=passage.id).all()}

        for q_data in c["questions"]:
            if q_data["text"] not in existing_qs:
                new_q = ComprehensionQuestion(
                    passage_id=passage.id,
                    question_text=q_data["text"],
                    options=json.dumps(q_data["options"]),
                    correct_answer=q_data["answer"],
                    explanation=q_data["explanation"]
                )
                session.add(new_q)
            else:
                # Update existing
                q_obj = existing_qs[q_data["text"]]
                q_obj.options = json.dumps(q_data["options"])
                q_obj.correct_answer = q_data["answer"]
                q_obj.explanation = q_data["explanation"]

    session.commit()
    session.close()
    logger.info("Database seeding completed.")
