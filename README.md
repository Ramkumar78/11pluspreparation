# 🦁 ScholarQuest: The Ultimate 11+ Prep Adventure!

**ScholarQuest** (formerly VocabQuest) is a dual-subject learning tool designed to master 11+ preparation. It keeps young minds (ages 8-12) engaged with high-octane challenges in both Vocabulary and Mathematics.

---

## 🚀 Features That Make Learning Fun

*   **🎮 Gamified Experience:** Earn points, build streaks, and level up! The more you play, the harder it gets.
*   **🧠 Adaptive Difficulty:**
    *   **Vocab Mode:** Adjusts word difficulty based on performance.
    *   **Maths Mode:** Scales arithmetic complexity and introduces tricky word problems.
*   **📚 Dual Modes:**
    *   **VocabQuest:** Visual clues, synonyms, and definitions to expand vocabulary.
    *   **MathsQuest:** Rapid-fire arithmetic (Stage 1) and multi-step word problems (Stage 2) tailored for 11+ exams (e.g., Wilson's School).
*   **🎨 Visual Clues:** Stuck on a word? High-quality cartoons and images provide hints.
*   **🔊 Audio Pronunciation:** Learn how to say it right!
*   **✨ Flashy Animations:** Confetti for wins, bouncing text, and slick transitions make every interaction feel rewarding.
*   **🛡️ Kid-Safe Environment:** Secure, sanitized inputs, and curated content.

---

## 📸 Screenshots

| Start Your Adventure | Master The Challenge |
| :---: | :---: |
| ![Start Screen](https://via.placeholder.com/400x250/indigo/white?text=ScholarQuest+Home) | ![Game Screen](https://via.placeholder.com/400x250/white/indigo?text=In-Game+Action) |
| *Choose between Vocab and Maths to begin!* | *Solve problems, guess words, and win big!* |

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
