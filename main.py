from builtins import enumerate, input, int, len, min, next, print, sorted
import sys
import io
import os
import random

# ensure utf-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import spacy
from nlp.tokenizer import extract_keywords
from nlp.translator import translate_words
from nlp.example_generator import generate_example_sentences
from utils.saver import save_to_json, save_to_excel
from speech.text_to_speech import speak
from deep_translator import GoogleTranslator

# load spaCy model for POS tagging
nlp = spacy.load("en_core_web_sm")

# define spaced repetition buckets (in days)
SR_SCHEDULE = {0: 1, 1: 2, 2: 4, 3: 7, 4: 14}


def main():
    print("=== 📚 Ứng dụng Flashcard Tiếng Anh ===")

    # 1. Nhập bài đọc (1 dòng)
    sample_text = input("\n📝 Nhập bài đọc tiếng Anh: ")
    # Dịch toàn câu ngay đầu
    try:
        sentence_translation = GoogleTranslator(source="en", target="vi").translate(
            sample_text
        )
        print(f"🔄 Dịch câu: {sentence_translation}\n")
    except:
        print("🔄 Không dịch được câu đầu.\n")

    # 2. Tách từ khóa và lấy POS
    keywords = extract_keywords(sample_text)
    if not keywords:
        print("⛔ Không tìm được từ khóa nào. Thử lại với đoạn văn khác.")
        return
    # get POS for each keyword
    pos_map = {
        token.text: token.pos_
        for token in nlp(sample_text)
        if token.lemma_.lower() in keywords
    }

    # 3. Dịch từ khóa
    translations = translate_words(keywords)

    # 4. Tạo câu ví dụ
    examples = generate_example_sentences(keywords)

    # 5. Lưu flashcards
    flashcards = []
    for word in keywords:
        flashcards.append(
            {
                "word": word,
                "pos": pos_map.get(word, "X"),
                "meaning": translations.get(word, "⛔ Không dịch được"),
                "example": examples.get(word, "Không có câu ví dụ"),
                "wrong_count": 0,
            }
        )
    # save
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    save_to_json(flashcards, os.path.join(output_dir, "flashcards.json"))
    save_to_excel(flashcards, os.path.join(output_dir, "flashcards.xlsx"))
    print("📁 Đã lưu flashcards vào 'output'.\n")

    # 6. Hiển thị từ mới với POS and meaning
    print("=== 📖 TỪ MỚI (word [POS] -> meaning) ===")
    for idx, fc in enumerate(flashcards, 1):
        print(f"{idx}. {fc['word']} [{fc['pos']}] -> {fc['meaning']}")
    print()

    # 7. Quiz multiple-choice before input
    print("=== 🧠 QUIZ MC: Chọn nghĩa đúng (EN -> VI) ===")
    total_questions = 0
    correct = []
    wrong = []
    # multiple choice quiz
    for idx, fc in enumerate(flashcards, 1):
        total_questions += 1
        word, pos, meaning = fc["word"], fc["pos"], fc["meaning"]
        # prepare choices
        other_meanings = [f["meaning"] for f in flashcards if f["word"] != word]
        choices = random.sample(other_meanings, min(3, len(other_meanings))) + [meaning]
        random.shuffle(choices)
        print(f"{idx}. {word} [{pos}]")
        for i, opt in enumerate(choices, 1):
            print(f"  {i}. {opt}")
        ans = input("Chọn (1-4) or 'exit': ").strip()
        if ans.lower() == "exit":
            break
        if ans.isdigit() and choices[int(ans) - 1] == meaning:
            print("✅ Chính xác!\n")
            correct.append(word)
            speak(word)
        else:
            print(f"❌ Sai. Đáp án đúng: {meaning}\n")
            fc["wrong_count"] += 1
            wrong.append(word)

    # 8. Quiz: tự nhập nghĩa VN cho từ EN
    print("\n=== 🧠 QUIZ: Hãy nhập nghĩa tiếng Việt cho từ tiếng Anh ===")
    total_questions = 0
    correct = []
    wrong = []
    # quiz chính
    for idx, fc in enumerate(flashcards, 1):
        total_questions += 1
        word, meaning = fc["word"], fc["meaning"]
        print(f"{idx}. {word}")
        ans = input("👉 Nghĩa (hoặc 'exit' để dừng): ").strip()
        if ans.lower() == "exit":
            break
        if meaning.lower() in ans.lower():
            print("✅ Chính xác!\n")
            correct.append(word)
            speak(word)
        else:
            print(f"❌ Sai. Đáp án đúng: {meaning}\n")
            wrong.append(word)

    # quiz phụ: hỏi lại các từ sai
    if wrong:
        print("\n=== 🔄 QUIZ LẠI TỪ ĐÃ SAI ===")
        for word in wrong:
            total_questions += 1
            print(f"Từ: {word}")
            ans = input("👉 Nghĩa: ").strip()
            if ans.lower() == "exit":
                break
            if translations[word].lower() in ans.lower():
                print("✅ Đúng lần 2!\n")
                correct.append(word)
                speak(word)
            else:
                print(f"❌ Vẫn sai! Nghĩa đúng: {translations[word]}\n")

    # 9. Final results and spaced repetition schedule
    score = len(correct)
    pct = int(score / total_questions * 100) if total_questions else 0
    print(f"🎯 Tổng: {score}/{total_questions} = {pct}%\n")
    print("✅ Đúng:", correct)
    print("❌ Sai:", [fc["word"] for fc in flashcards if fc["word"] not in correct])
    # spaced repetition suggestion
    print("\n💡 Gợi ý Spaced Repetition:")
    for fc in sorted(flashcards, key=lambda x: x["wrong_count"], reverse=True):
        days = SR_SCHEDULE.get(fc["wrong_count"], 30)
        print(f"- {fc['word']} sai {fc['wrong_count']} lần: xem lại sau {days} ngày.")


if __name__ == "__main__":
    main()
