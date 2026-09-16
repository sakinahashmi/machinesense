import sys
from pathlib import Path
import pytest

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.database import init_db


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    init_db()
