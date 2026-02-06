# 🦁 ScholarQuest: The Ultimate 11+ Prep Adventure!

[![CI](https://github.com/Ramkumar78/11pluspreparation/actions/workflows/ci.yml/badge.svg)](https://github.com/Ramkumar78/11pluspreparation/actions/workflows/ci.yml)

**ScholarQuest** (formerly VocabQuest) is a dual-subject learning tool designed to master 11+ preparation. It keeps young minds (ages 8-12) engaged with high-octane challenges in Vocabulary, Mathematics, and Comprehension.

**Focused on the specific requirements of:**
*   Wilson's School
*   Wallington County Grammar School
*   Sutton Grammar School
*   Nonsuch High School for Girls

---

## 🚀 Syllabus Focus

### Stage 1 (SET - Selective Eligibility Test)
*   **Format:** Multiple choice (mostly).
*   **Focus:** KS2 English & Math with a requirement for speed and accuracy.
*   **Topics:** Number, Algebra, Ratio, Geometry (angles, area), Data (mean, mode), and Fractions/Decimals/Percentages.
*   **ScholarQuest:** Provides rapid-fire arithmetic and targeted multiple-choice style questions.

### Stage 2
*   **Format:** Standard written answers.
*   **Focus:** Harder, multi-step problems requiring working out, and English Comprehension.
*   **ScholarQuest:** Includes complex word problems and explains the "how-to" when an answer is incorrect to teach the methodology. Now also includes classic English comprehension passages with evidence-based questions.

---

## 🚀 Features That Make Learning Fun

*   **🎮 Gamified Experience:** Earn points, build streaks, and level up! The more you play, the harder it gets.
*   **🧠 Adaptive Difficulty:**
    *   **Vocab Mode:** Adjusts word difficulty based on performance.
    *   **Maths Mode:** Scales arithmetic complexity and introduces tricky word problems.
*   **📚 Triple Modes:**
    *   **VocabQuest:** Visual clues, synonyms, and definitions to expand vocabulary.
    *   **MathsQuest:** Covers key 11+ topics like Algebra, Ratios, Logic, and Geometry.
    *   **Comprehension:** Read classic passages (e.g., The Secret Garden, Oliver Twist) and answer analysis questions.
*   **💡 Instant Explanations:** Got a math question wrong? We show you exactly how to solve it.
*   **🎨 Visual Clues:** Stuck on a word? High-quality cartoons and images provide hints.
*   **🔊 Audio Pronunciation:** Learn how to say it right!
*   **✨ Flashy Animations:** Confetti for wins, bouncing text, and slick transitions make every interaction feel rewarding.
*   **🛡️ Kid-Safe Environment:** Secure, sanitized inputs, and curated content.

---

## 📸 Screenshots

| Start Your Adventure | Master The Challenge |
| :---: | :---: |
| ![Start Screen](https://via.placeholder.com/400x250/indigo/white?text=ScholarQuest+Home) | ![Game Screen](https://via.placeholder.com/400x250/white/indigo?text=In-Game+Action) |
| *Choose between Vocab, Maths, and Comprehension to begin!* | *Solve problems, guess words, and win big!* |

---

## 🛠️ How to Run

ScholarQuest is built with **Docker** for easy setup.

### Prerequisites
*   Docker & Docker Compose

### Start the Game
1.  Clone the repository.
2.  Run the following command in your terminal:
    ```bash
    docker-compose up --build
    ```
3.  Open your browser and navigate to:
    👉 **http://localhost:5173**

---

## 🧪 Testing & Security

We take quality seriously. ScholarQuest comes brim-full of tests and security features.

### Running Tests
**Backend:**
```bash
cd VocabQuest/backend
pip install -r requirements.txt
pytest
```

**Frontend:**
```bash
cd VocabQuest/frontend
npm install
npm test
```

### Security Features
*   **Rate Limiting:** Prevents spam and abuse of the API.
*   **Input Sanitization:** All user inputs are cleaned to prevent injection attacks.
*   **Secure Headers:** Best practices for web security.

---

## 🌟 Why Kids Love It?
> "It's like a video game, but I'm actually learning for my 11+ exams!" - *Future Scholar*

Start your **ScholarQuest** today!
