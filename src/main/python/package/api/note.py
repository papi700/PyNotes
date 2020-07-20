import json
import os
from uuid import uuid4
from glob import glob

from package.api.constants import NOTES_DIR


def get_notes() :
    notes = []
    files = glob(os.path.join(NOTES_DIR, "*.json"))
    for file in files :
        with open(file, "r") as f :
            note_data = json.load(f)
            note_uuid = os.path.splitext(os.path.basename(file))[0]
            note_title = note_data.get("title")
            note_content = note_data.get("content")
            note = Note(uuid=note_uuid, title=note_title, content=note_content)
            notes.append(note)
    return notes


class Note :
    def __init__(self, title="", content="", uuid=None) :
        if uuid :
            self.uuid = uuid
        else :
            self.uuid = str(uuid4())
        self.title = title
        self.content = content

    def __repr__(self) :
        return f"{self.title} ({self.uuid})"

    def __str__(self) :
        return self.title

    @property
    def content(self) :
        return self._content

    @content.setter
    def content(self, value) :
        if isinstance(value, str) :
            self._content = value
        else :
            raise TypeError("Valeur invalide besoin d'une chaine de caracteres")

    def delete(self) :
        os.remove(self.path)
        if os.path.exists(self.path) :
            return False
        else :
            return True

    @property
    def path(self) :
        return os.path.join(NOTES_DIR, self.uuid + ".json")

    def save(self) :
        if not os.path.exists(NOTES_DIR) :
            os.makedirs(NOTES_DIR)

        data = {"title" : self.title, "content" : self.content}
        with open(self.path, "w") as f :
            json.dump(data, f, indent=4)


if __name__ == '__main__' :
    n = Note(title="Ceci est un titre", content="Ceci est un contenu")
    print(n.path)
    # print(n.content)
