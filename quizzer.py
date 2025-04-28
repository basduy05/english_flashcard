from builtins import enumerate, input, len, print
import random
from speech.text_to_speech import speak


def start_quiz(flashcards, mode="en_to_vi"):
    """
    Bắt đầu bài quiz luyện tập từ vựng.
    - mode: 'en_to_vi' (Tiếng Anh -> Tiếng Việt) hoặc 'vi_to_en' (Tiếng Việt -> Tiếng Anh)
    """
    if not flashcards:
        print("⛔ Không có từ vựng để luyện tập.")
        return

    print("\n=== 🧠 BẮT ĐẦU QUIZ ===\n")
    questions = flashcards.copy()
    random.shuffle(questions)  # Trộn ngẫu nhiên câu hỏi

    score = 0
    total = len(questions)
    wrong_words = []  # danh sách từ sai

    for idx, fc in enumerate(questions, 1):
        if mode == "en_to_vi":
            print(f"{idx}. Nghĩa của từ '{fc['word']}' là gì?")
            user_answer = input("👉 Trả lời (hoặc gõ 'exit' để thoát): ").strip()
            if user_answer.lower() == "exit":
                print("\n👋 Bạn đã thoát quiz. Kết thúc tại đây!")
                break

            if user_answer.lower() in fc["meaning"].lower():
                print("✅ Chính xác!\n")
                score += 1
                # Phát âm từ nếu trả lời đúng
                speak(fc["word"])
            else:
                print(f"❌ Sai. Đáp án đúng là: {fc['word']} ({fc['meaning']})\n")
                wrong_words.append(fc["word"])
                # Yêu cầu người dùng nhập lại chính xác từ
                while True:
                    retry = input("🔄 Nhập lại chính xác từ tiếng Anh: ").strip()
                    if retry.lower() == fc["word"].lower():
                        print("✅ Đúng rồi! Tốt lắm!\n")
                        speak(fc["word"])
                        break
                    else:
                        print("❌ Chưa đúng. Thử lại nhé!")

        elif mode == "vi_to_en":
            print(f"{idx}. Từ tiếng Anh cho nghĩa '{fc['meaning']}' là gì?")
            user_answer = input("👉 Trả lời (hoặc gõ 'exit' để thoát): ").strip()
            if user_answer.lower() == "exit":
                print("\n👋 Bạn đã thoát quiz. Kết thúc tại đây!")
                break

            if user_answer.lower() == fc["word"].lower():
                print("✅ Chính xác!\n")
                score += 1
                # Phát âm từ nếu đúng
                speak(fc["word"])
            else:
                print(f"❌ Sai. Đáp án đúng là: {fc['word']} ({fc['meaning']})\n")
                wrong_words.append(fc["word"])
                # Bắt nhập lại đúng
                while True:
                    retry = input("🔄 Nhập lại chính xác từ tiếng Anh: ").strip()
                    if retry.lower() == fc["word"].lower():
                        print("✅ Đúng rồi! Tốt lắm!\n")
                        speak(fc["word"])
                        break
                    else:
                        print("❌ Chưa đúng. Thử lại nhé!")

        else:
            print("⛔ Chế độ quiz không hợp lệ.")
            break

    # Kết quả tổng kết
    print(f"\n📊 Kết quả: {score}/{total} câu đúng.")

    # Sau Quiz: Gợi ý ôn tập từ sai
    if wrong_words:
        print("\n📋 Các từ bạn đã trả lời sai:")
        for idx, word in enumerate(wrong_words, 1):
            print(f"{idx}. {word}")

        choice = (
            input("\n🤔 Bạn có muốn phát âm lại các từ sai không? (y/n): ")
            .strip()
            .lower()
        )
        if choice == "y":
            for word in wrong_words:
                print(f"🔈 {word}")
                speak(word)
    else:
        print("\n🎉 Bạn đã trả lời đúng tất cả! Xuất sắc!")
