import os
import json
from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from model import CreateNoteResponse, NoteTextResponse, NoteInfoResponse, NoteListResponse

api_router = APIRouter()

NOTES_DIR = "notes"
TOKENS_FILE = "tokens.txt"

# Ensure notes directory exists
os.makedirs(NOTES_DIR, exist_ok=True)

# Проверка токена
def load_tokens():
    if not os.path.exists(TOKENS_FILE):
        return set()
    with open(TOKENS_FILE, "r") as file:
        return set(line.strip() for line in file)

def check_token(token: str):
    tokens = load_tokens()
    if token not in tokens:
        raise HTTPException(status_code=403, detail="Invalid token")

# Создать новую заметку
@api_router.post("/note", response_model=CreateNoteResponse)
def create_note(text: str, token: str = Query(...)):
    check_token(token)
    note_id = len(os.listdir(NOTES_DIR)) + 1
    note_file = os.path.join(NOTES_DIR, f"{note_id}.txt")
    with open(note_file, "w") as file:
        json.dump({
            "text": text,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }, file)
    return CreateNoteResponse(id=note_id)

# Получить текст заметки
@api_router.get("/note/{id}", response_model=NoteTextResponse)
def get_note_text(id: int, token: str = Query(...)):
    check_token(token)
    note_file = os.path.join(NOTES_DIR, f"{id}.txt")
    if not os.path.exists(note_file):
        raise HTTPException(status_code=404, detail="Note not found")
    with open(note_file, "r") as file:
        data = json.load(file)
    return NoteTextResponse(id=id, text=data["text"])

# Получить информацию о времени создания и изменения заметки
@api_router.get("/note/{id}/info", response_model=NoteInfoResponse)
def get_note_info(id: int, token: str = Query(...)):
    check_token(token)
    note_file = os.path.join(NOTES_DIR, f"{id}.txt")
    if not os.path.exists(note_file):
        raise HTTPException(status_code=404, detail="Note not found")
    with open(note_file, "r") as file:
        data = json.load(file)
    return NoteInfoResponse(
        created_at=data["created_at"],
        updated_at=data["updated_at"]
    )

# Обновить текст заметки
@api_router.patch("/note/{id}", response_model=NoteTextResponse)
def update_note_text(id: int, new_text: str, token: str = Query(...)):
    check_token(token)
    note_file = os.path.join(NOTES_DIR, f"{id}.txt")
    if not os.path.exists(note_file):
        raise HTTPException(status_code=404, detail="Note not found")
    with open(note_file, "r+") as file:
        data = json.load(file)
        data["text"] = new_text
        data["updated_at"] = datetime.now().isoformat()
        file.seek(0)
        json.dump(data, file)
        file.truncate()
    return NoteTextResponse(id=id, text=new_text)

# Удалить заметку
@api_router.delete("/note/{id}")
def delete_note(id: int, token: str = Query(...)):
    check_token(token)
    note_file = os.path.join(NOTES_DIR, f"{id}.txt")
    if not os.path.exists(note_file):
        raise HTTPException(status_code=404, detail="Note not found")
    os.remove(note_file)
    return {"detail": "Note deleted"}

# Получить список id заметок
@api_router.get("/notes", response_model=NoteListResponse)
def list_notes(token: str = Query(...)):
    check_token(token)
    note_ids = [int(filename.split(".")[0]) for filename in os.listdir(NOTES_DIR) if filename.endswith(".txt")]
    return NoteListResponse(notes={i: note_id for i, note_id in enumerate(note_ids)})
