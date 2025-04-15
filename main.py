import os
import subprocess
import webbrowser

# start jupyter notebook server
notebook_path = os.path.abspath("notebooks/generate_cy2.ipynb")

subprocess.Popen(["jupyter", "notebook", notebook_path])