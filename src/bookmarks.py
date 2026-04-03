import os, json

def load_bookmark():
    if not os.path.exists("data/bookmarks.json"):
        return []
    with open("data/bookmarks.json", "r") as f:
        content = f.read()
        if not content:
            return []
        return json.loads(content)
        
def save_bookmark(name, steam_ids, franchise_id, collection_id):
    bookmarks = load_bookmark()
    find = False
    for bookmark in bookmarks:
        if franchise_id and bookmark["franchise_id"] == franchise_id:
            print("Bookmark already exists")
            find = True
            break
        elif collection_id and bookmark["collection_id"] == collection_id:
            print("Bookmark already exists")
            find = True
            break
    if not find:
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
    bookmarks = load_bookmark()
    b_list = []
    for bookmark in bookmarks:
        if bookmark["name"] != name:
            b_list.append(bookmark)
    with open("data/bookmarks.json", "w") as f:
        json.dump(b_list, f)