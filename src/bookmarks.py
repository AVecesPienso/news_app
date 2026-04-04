import os
import json

def load_bookmark():
    """
    Loads all bookmarks from data/bookmarks.json.
    Returns an empty list if the file doesn't exist or is empty.
    """
    if not os.path.exists("data/bookmarks.json"):
        return []
    with open("data/bookmarks.json", "r") as f:
        content = f.read()
        if not content:
            return []
        return json.loads(content)
        
def save_bookmark(name, steam_ids, franchise_id, collection_id):
    """
    Saves a new bookmark to data/bookmarks.json.
    Detects duplicates by franchise_id or collection_id to avoid saving the same franchise twice.
    Returns True if saved successfully, False if the bookmark already exists.
    """
    bookmarks = load_bookmark()
    already_exists = False
    for bookmark in bookmarks:
        if franchise_id and bookmark["franchise_id"] == franchise_id:
            print("Bookmark already exists")
            already_exists = True
            break
        elif collection_id and bookmark["collection_id"] == collection_id:
            print("Bookmark already exists")
            already_exists = True
            break
    if not already_exists:
        bookmarks.append({
            "name": name, 
            "steam_ids": steam_ids,
            "franchise_id": franchise_id,
            "collection_id": collection_id
            })
        with open("data/bookmarks.json", "w") as f:
            json.dump(bookmarks, f)
        return True
    return False

def delete_bookmark(name):
    """
    Deletes a bookmark from data/bookmarks.json by name.
    Rewrites the file without the deleted bookmark.
    """
    bookmarks = load_bookmark()
    b_list = []
    for bookmark in bookmarks:
        if bookmark["name"] != name:
            b_list.append(bookmark)
    with open("data/bookmarks.json", "w") as f:
        json.dump(b_list, f)