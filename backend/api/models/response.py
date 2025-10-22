from pydantic import BaseModel
from typing import Any, Optional


class ResponseModel(BaseModel):
	message: str
	data: Optional[Any] = None
