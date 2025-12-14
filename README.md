# 🦁 VocabQuest: The Ultimate Word Adventure!

**VocabQuest** is not just a learning tool; it's a high-octane journey into the world of words, designed specifically to keep young minds (ages 8-12) engaged, challenged, and gluing them to the screen (in a good way!).

---

## 🚀 Features That Make Learning Fun

*   **🎮 Gamified Experience:** Earn points, build streaks, and level up! The more you play, the harder it gets.
*   **🧠 Adaptive Difficulty:** The game gets smarter as you do. It adjusts the word difficulty based on your performance, ensuring you are always challenged but never overwhelmed.
*   **🎨 Visual Clues:** Stuck on a word? High-quality cartoons and images provide hints to jog your memory.
*   **🔊 Audio Pronunciation:** Learn how to say it right! Native browser-based pronunciation helps with listening and speaking skills.
*   **✨ Flashy Animations:** Confetti for wins, bouncing text, and slick transitions make every interaction feel rewarding.
*   **🛡️ Kid-Safe Environment:** Secure, sanitized inputs, and curated content mean parents can relax while kids learn.

---

## 📸 Screenshots

| Start Your Adventure | Master The Challenge |
| :---: | :---: |
| ![Start Screen](https://via.placeholder.com/400x250/indigo/white?text=VocabQuest+Home) | ![Game Screen](https://via.placeholder.com/400x250/white/indigo?text=In-Game+Action) |
| *Colorful, inviting home screen to get you pumped!* | *Guess the word, see the clues, and win big!* |

---

## 🛠️ How to Run

VocabQuest is built with **Docker** for easy setup.

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

We take quality seriously. VocabQuest comes brim-full of tests and security features.

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
> "It's like a video game, but I'm actually learning new words for school!" - *Beta Tester, Age 10*

Start your **VocabQuest** today!
