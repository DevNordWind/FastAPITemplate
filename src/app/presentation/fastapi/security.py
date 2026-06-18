from typing import Final

from fastapi.security import HTTPBearer

SECURITY: Final[HTTPBearer] = HTTPBearer()
