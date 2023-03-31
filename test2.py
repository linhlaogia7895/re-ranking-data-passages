import os

import subprocess

result = subprocess.run(['python', 'trecgen2007_score.py', 'gold-standard-07.txt', 'output-format-method-1.txt'], capture_output=True, text=True)
#result = os.system("trecgen2007_score.py gold-standard-07.txt output-format-method-1.txt")
print(result.stdout)
