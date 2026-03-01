from typing import TypedDict, Optional

class RPGState(TypedDict):
    user_message: str
    narration: Optional[str]
    validated: Optional[bool]
    validation_feedback: Optional[str]