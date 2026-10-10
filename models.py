"""Request schema shared by every EduGenie endpoint."""
from pydantic import BaseModel


class UserRequest(BaseModel):
    text: str            # the topic, question or study material
    context: str = ""    # the previous answer, used for follow-up questions on /qa
