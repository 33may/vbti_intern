import sys
import os

from app.utils.core.fastapiConfig import get_application

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = get_application()

