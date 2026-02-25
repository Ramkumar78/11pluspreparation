import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'VocabQuest', 'backend'))

from database import Session, MathQuestion

session = Session()

# Delete the old question that gives away the answer
old_question_text = "Calculate 2/3 + 1/6. Give your answer as a simple fraction (e.g. 5/6)."
q = session.query(MathQuestion).filter_by(text=old_question_text).first()
if q:
    session.delete(q)
    session.commit()
    print("Deleted old question.")
else:
    print("Old question not found.")
    
session.close()
