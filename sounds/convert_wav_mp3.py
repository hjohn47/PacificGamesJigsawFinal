import os
from pathlib import Path


os.system("""FOR /F "tokens=*" %G IN ('dir /b *.wav') DO ffmpeg -i "%G" -acodec mp3 "%~nG.mp3" """)


