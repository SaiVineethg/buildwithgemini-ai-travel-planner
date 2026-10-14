from pathlib import Path
from dotenv import load_dotenv

env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    load_dotenv(env_file)
