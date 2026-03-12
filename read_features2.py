import fitz

doc = fitz.open('Career path_features.pdf')
text = ""
for page in doc:
    text += page.get_text() + "\n"

print("--- PDF CONTENT ---")
print(text)
