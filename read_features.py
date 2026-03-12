import sys
import subprocess
try:
    import pypdf
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pypdf"])
    import pypdf

reader = pypdf.PdfReader('Career path_features.pdf')
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"

print(text)
