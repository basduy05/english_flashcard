import spacy

# Load mô hình ngôn ngữ tiếng Anh
nlp = spacy.load("en_core_web_sm")

# Đoạn văn mẫu
text = "Artificial Intelligence is changing how students learn languages."

# Phân tích ngữ pháp
doc = nlp(text)

# In thông tin từng từ
print("Token | Part of Speech | Is Stopword")
for token in doc:
    print(f"{token.text} | {token.pos_} | {token.is_stop}")
