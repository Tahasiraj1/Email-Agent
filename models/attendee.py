from pydantic import BaseModel, EmailStr

class Attendee(BaseModel):
    email: EmailStr