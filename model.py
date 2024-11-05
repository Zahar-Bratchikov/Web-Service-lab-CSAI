from typing import Dict
from pydantic import BaseModel
from datetime import datetime

class CreateNoteResponse(BaseModel):
    id: int

class NoteTextResponse(BaseModel):
    id: int
    text: str

class NoteInfoResponse(BaseModel):
    created_at: datetime
    updated_at: datetime

class NoteListResponse(BaseModel):
    notes: Dict[int, int]

class CountLettersResponse(BaseModel):
    counted_at: datetime
    counters: Dict[str, int]
