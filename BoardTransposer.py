#!/usr/bin/env python3

import json
import os
import uuid
import hashlib
import sqlite3
import requests

class Board:
    def __init__(self):
        self.name = ""
        self.id = ""
        self.desc = ""
        self.closed = False
        self.starred = False
        self.labelNames = {}
        self.dateLastActivity = ""
        self.cards = []
        self.labels = []
        self.lists = []
        self.checklists = []


    ### INTERFACE METHODS ###
    def import_from_trello(self, data):
        ## descriptions ##
        
        # $id$
        # *example*
        # `6674e6e2f15e83ede06731e5`
        
        # $name$
        # *example*
        # `Concise Testy Boardy`
        
        # $desc$
        # *example*
        # `**description**`
        
        # $closed$
        # *example*
        # `False`
        
        # $starred$
        # *example*
        # `False`
        
        # $labelNames{}$
        # *example*
        # `{"green": "","yellow": "ura","orange": "","red": "","purple": "","blue": "","sky": "","lime": "","pink": "","black": "","green_dark": "","yellow_dark": "","orange_dark": "","red_dark": "","purple_dark": "","blue_dark": "","sky_dark": "","lime_dark": "","pink_dark": "","black_dark": "","green_light": "","yellow_light": "","orange_light": "","red_light": "","purple_light": "","blue_light": "","sky_light": "","lime_light": "","pink_light": "","black_light": ""}`
        
        # $dateLastActivity$
        # *example*
        # `2024-06-21T02:38:23.543Z`
        
        # $cards[{}]$
        # *example*
        # ``` { 
        #     "id": "6674e6ed32bed9581058ad99",
        #     "checkItemStates": [{"idCheckItem": "6674e7901c8e6c6f87ac31cb","state": "complete"}],
        #     "closed": false,
        #     "dueComplete": true,
        #     "dateLastActivity": "2024-06-21T02:38:23.543Z",
        #     "desc": "**meowwww** rawr :clock3: :3 .sdf sdfsd",
        #     "due": "2024-06-22T02:35:45.929Z",
        #     "idBoard": "6674e6e2f15e83ede06731e5",
        #     "idChecklists": ["6674e7780d3b2b267b5a1863"],
        #     "idLabels": ["6674e6e21dc51400eb89f31a"],
        #     "idList": "6674e6e83915bf80d1bc5c3e",
        #     "idAttachmentCover": "6674e7267046ebc41e124f19",
        #     "labels": [{"id": "6674e6e21dc51400eb89f31a","idBoard": "6674e6e2f15e83ede06731e5","name": "ura","color": "yellow","uses": 1}],
        #     "name": "Cardy",
        #     "attachments": [{"id": "6674e7267046ebc41e124f19","bytes": 585005,"idMember": "64f9ed59007bb6365ad99abd",mimeType": "image/jpeg","name": "celeste2.jpg","url": "https://trello.com/1/cards/6674e6ed32bed9581058ad99/attachments/6674e7267046ebc41e124f19/download/celeste2.jpg","fileName": "celeste2.jpg"},{"id": "6674e7431cad571ef493dc8d","bytes": 1323,"date": "2024-06-21T02:36:51.161Z","idMember": "64f9ed59007bb6365ad99abd","mimeType": "text/x-python","name": "goofight.py","url": "https://trello.com/1/cards/6674e6ed32bed9581058ad99/attachments/6674e7431cad571ef493dc8d/download/goofight.py","fileName": "goofight.py"}]
        # } ```
        
        # $labels[{}]$
        # *example*
        # `{"id": "6674e6e21dc51400eb89f31a","idBoard": "6674e6e2f15e83ede06731e5","name": "ura","color": "yellow","uses": 1}`
        
        # $lists[{}]$
        # *example*
        # ``` {
        #     "id": "6674e6e83915bf80d1bc5c3e",
        #     "name": "Listy",
        #     "closed": false,
        #     "idBoard": "6674e6e2f15e83ede06731e5",
        # } ```
        
        # $checklists[{}]$
        # *example*
        # ``` {
        # "id": "6674e7780d3b2b267b5a1863",
        #     "name": "Checky",
        #     "idBoard": "6674e6e2f15e83ede06731e5",
        #     "idCard": "6674e6ed32bed9581058ad99",
        #     "checkItems": [
        #         {
        #             "id": "6674e7901c8e6c6f87ac31cb",
        #             "name": "tres **:3**",
        #             "state": "complete",
        #             "due": null,
        #             "idChecklist": "6674e7780d3b2b267b5a1863"
        #         }
        #     ]
        # } ```
        
        ## setting them ##
        
        self.name = data.get('name', "")
        self.id = data.get('id', "")
        self.desc = data.get('desc', "")
        self.closed = data.get('closed', False)
        self.starred = data.get('starred', False)
        self.labelNames = data.get('labelNames', {})
        self.dateLastActivity = data.get('dateLastActivity', "")
        self.cards = data.get('cards', [])
        self.labels = data.get('labels', [])
        self.lists = data.get('lists', [])
        self.checklists = data.get('checklists', [])

    def json_to_db(self):
        ## declarations ##
        
        # $attachments table$
        # *fields*
        # id, item_id, file_type, file_name, file_size, file_path
        # *example*
        # `49f47907-9c69-46ae-bd19-414b5d7fa362`, `7a31fa0a-68af-47f3-bd87-492025f7a3cb`, `image/jpeg`, `discavatar.jpg`, `4250447`, `file:///home/raven/Documents/Media/discavatar.jpg`
        attachments = []
        
        # $items table$
        # *fields*
        # id, content, description, due, added_at, completed_at, updated_at, section_id, project_id, parent_id, priority, child_order, checked, is_deleted, day_order, collapsed, pinned, labels, extra_data
        # *example*
        # `67aef85e-ee74-4c9d-ad33-408250a00575`, `asdfasdf`, `:3`, `{"date":"","timezone":"","is_recurring":false,"recurrency_type":"6","recurrency_interval":"0","recurrency_weeks":"","recurrency_count":"0","recurrency_end":""}`, `2024-06-19T00:11:28-0400`, `2024-06-19T00:00:00-0400`, `2024-06-19T00:11:36-0400`, `0c6d1837-c20f-4cfe-bf49-3de2f2a49192`, `4b4fdf68-5b50-4427-a01d-0ac63dd316b7`, `850edee8-da6b-4b90-bede-af4be5585bb4`, `1`, `0`, `1`, `0`, `0`, `0`, `0   43ee5301-e1eb-4b3d-a945-6557d84d463d;fb8e570f-b578-4db7-b94a-72505c3a7a6b`
        items = []
        
        # $labels table$
        # *fields*
        # id, name, color, item_order, is_deleted, is_favorite, backend_type
        # *example*
        # `43ee5301-e1eb-4b3d-a945-6557d84d463d`, `pizza`, `charcoal`, `0`, `0`, `0`, `local`
        labels = []
        
        # $projects table$
        # *fields*
        # id, name, color, backend_type, inbox_project, team_inbox, child_order, is_deleted, is_archived, is_favorite, shared, view_style, sort_order, parent_id, collapsed, icon_style, emoji, show_completed, description, due_date, inbox_section_hidded, sync_id
        # *example*
        # `4b4fdf68-5b50-4427-a01d-0ac63dd316b7`, `testy`, `sky_blue`, `local`, `0`, `0`, `1`, `0`, `0`, `0`, `0`, `board`, `0`, ``, `0`, `emoji`, `🔷`, `0`, `gam.`, ``, `1`, ``
        projects = []
        
        # $sections table$
        # *fields*
        # id, name, archived_at, added_at, project_id, section_order, collapsed, is_deleted, is_archived, color, description, hidded
        # *example*
        # `0c6d1837-c20f-4cfe-bf49-3de2f2a49192`, `Currently Considering`, ``, `2024-06-12T22:48:03-0400`, `4b4fdf68-5b50-4427-a01d-0ac63dd316b7`, `2`, `1`, `0`, `0`, `salmon`, `For things not yet started, but considering for this current version`, `0`
        sections = []
        
        ## logic ##
        
        attachment_dir = os.path.join(os.path.expanduser('~'), '.local', 'planify-attachments')
        if not os.path.exists(attachment_dir):
            os.makedirs(attachment_dir)
            
        for card in self.cards:
            #new item
            new_item = {
                'id': short_uuid_to_uuid(card['id']),
                'content': card['name'],
                'description': card['desc'],
                'due': iso_date_to_due(card['due']),
                'added_at': card['dateLastActivity'],
                'completed_at': card['dateLastActivity'] if card['closed'] else "",
                'updated_at': card['dateLastActivity'],
                'section_id': short_uuid_to_uuid(card['idList']),
                'project_id': short_uuid_to_uuid(card['idBoard']),
                'parent_id': "",
                'priority': 1,
                'child_order': 0,
                'checked': card['closed'],
                'is_deleted': 0,
                'day_order': 0,
                'collapsed': 0,
                'pinned': 0,
                'labels': ';'.join([short_uuid_to_uuid(label['id']) for label in card['labels']]),
                'extra_data': ""
            }
            items.append(new_item)
        
            #new attachment
            for attachment in card['attachments']:
                file_path = os.path.join(attachment_dir, attachment['fileName'])
                response = requests.get(attachment['url'], stream=True)
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                new_attachment = {
                    'id': short_uuid_to_uuid(attachment['id']),
                    'item_id': short_uuid_to_uuid(card['id']),
                    'file_type': attachment['mimeType'],
                    'file_name': attachment['fileName'],
                    'file_size': attachment['bytes'],
                    'file_path': file_path
                }
                attachments.append(new_attachment)
                
        for checklist in self.checklists:
            for checkItem in checklist['checkItems']:
                card = None
                for c in self.cards:
                    if c['id'] == checklist['idCard']:
                        card = c
                        break
                #new checkitem
                new_item = {
                    'id': short_uuid_to_uuid(checkItem['id']),
                    'content': checkItem['name'],
                    'description': '',
                    'due': checkItem['due'] if checkItem['due'] else '',
                    'added_at': card['dateLastActivity'],
                    'completed_at': iso_date_to_due(checkItem['id'] + 'T00:00:00-0400') if checkItem['state'] == 'complete' else '',
                    'updated_at': card['dateLastActivity'],
                    'section_id': short_uuid_to_uuid(card['idList']),
                    'project_id': short_uuid_to_uuid(checklist['idBoard']),
                    'parent_id': short_uuid_to_uuid(checklist['idCard']),
                    'priority': 1,
                    'child_order': 0,
                    'checked': 1 if checkItem['state'] == 'complete' else 0,
                    'is_deleted': 0,
                    'day_order': 0,
                    'collapsed': 0,
                    'pinned': 0,
                    'labels': "",
                    'extra_data': ""
                }
                items.append(new_item)
        
        for label in self.labels:
            #new label
            new_label = {
                'id': short_uuid_to_uuid(label['id']),
                'name': label['name'],
                'color': color_trello_to_planify(label['color']),
                'item_order': 0,
                'is_deleted': 0,
                'is_favorite': 0,
                'backend_type': 'local'
            }
            labels.append(new_label)
        
        #new project
        new_project = {
            'id': short_uuid_to_uuid(self.id),
            'name': self.name,
            'color': 'sky_blue',
            'backend_type': 'local',
            'inbox_project': 0,
            'team_inbox': 0,
            'child_order': 0,
            'is_deleted': 0,
            'is_archived': 0,
            'is_favorite': 1 if self.starred else 0,
            'shared': 0,
            'view_style': 'board',
            'sort_order': 0,
            'parent_id': '',
            'collapsed': 0,
            'icon_style': '',
            'emoji': '',
            'show_completed': 0,
            'description': self.desc,
            'due_date': self.dateLastActivity,
            'inbox_section_hidded': 0,
            'sync_id': ''
        }
        projects.append(new_project)
        
        for trello_list in self.lists:
            #new section
            new_section = {
                'id': short_uuid_to_uuid(trello_list['id']),
                'name': trello_list['name'],
                'archived_at': '',
                'added_at': self.dateLastActivity,
                'project_id': short_uuid_to_uuid(trello_list['idBoard']),
                'section_order': 0,
                'collapsed': 0,
                'is_deleted': 0,
                'is_archived': 0,
                'color': 'salmon',
                'description': '',
                'hidded': 0
            }
            sections.append(new_section)
        
        return (attachments,items,labels,projects,sections)
            

    ### GET METHODS ###
    def get_card(self,ind):
        if ind < 0 or ind >= len(self.cards): return None
        return self.cards[ind]

    def get_label(self,ind):
        if ind < 0 or ind >= len(self.labels): return None
        return self.labels[ind]

    def get_list(self,ind):
        if ind < 0 or ind >= len(self.lists): return None
        return self.lists[ind]

    def get_checklist(self,ind):
        if ind < 0 or ind >= len(self.checklists): return None
        return self.checklists[ind]


    ### DUNDY DUNDERS ###
    def __str__(self):
        return f"Board:\nCards: {len(self.cards)}\nLabels: {len(self.labels)}\nLists: {len(self.lists)}\nChecklists: {len(self.checklists)}"


    ### GENERIC METHODS ###
def iso_date_to_due(iso_date):
    if iso_date is None:
        return '{"date":"","timezone":"","is_recurring":false,"recurrency_type":"6","recurrency_interval":"0","recurrency_weeks":"","recurrency_count":"0","recurrency_end":""}'
    return '{"date":"' + iso_date + '","timezone":"","is_recurring":false,"reccurrency_type":"6","recurrency_interval":"0","recurrency_weeks":"","recurrency_count":"0","recurrency_end":""}'

def short_uuid_to_uuid(short_uuid):
    short_uuid_bytes = bytes.fromhex(short_uuid)
    hash_object = hashlib.sha256()
    hash_object.update(short_uuid_bytes)
    hash_digest = hash_object.digest()
    uuid_bytes = hash_digest[:16]
    uuid_object = uuid.UUID(bytes=uuid_bytes)
    uuid_str = f"{uuid_object.hex[:8]}-{uuid_object.hex[8:12]}-{uuid_object.hex[12:16]}-{uuid_object.hex[16:20]}-{uuid_object.hex[20:]}"
    return uuid_str
    
def color_planify_to_trello(color):
    colors_planify = ["berry_red", "red", "orange", "yellow", "olive_green", "lime_green", "green", "mint_green", "teal", "sky_blue", "light_blue", "blue", "grape", "violet", "lavender", "magenta", "salmon", "charcoal", "grey", "taupe"]
    color_planify_to_trello_map = ["red_dark", "red", "orange", "yellow", "green_dark", "lime", "green", "green_light", "sky_dark", "sky", "blue_light", "blue", "purple_dark", "purple", "purple_light", "pink_dark", "pink", "black", "black_light", "yellow_dark"]
    try:
        return color_planify_to_trello_map[colors_planify.index(color)]
    except ValueError:
        return "black"  # default color if not found

def color_trello_to_planify(color):
    colors_trello = ["green", "yellow", "orange", "red", "purple", "blue", "sky", "lime", "pink", "black", "green_dark", "yellow_dark", "orange_dark", "red_dark", "purple_dark", "blue_dark", "sky_dark", "lime_dark", "pink_dark", "black_dark", "green_light", "yellow_light", "orange_light", "red_light", "purple_light", "blue_light", "sky_light", "lime_light", "pink_light", "black_light"]
    color_trello_to_planify_map = ["green", "yellow", "orange", "red", "violet", "sky_blue", "lime_green", "magenta", "charcoal", "olive_green", "taupe", "orange", "berry_red", "grape", "blue", "teal", "green", "magenta", "charcoal", "mint_green", "yellow", "orange", "red", "lavender", "light_blue", "sky_blue", "mint_green", "salmon", "grey"]
    try:
        return color_trello_to_planify_map[colors_trello.index(color)]
    except ValueError:
        return "charcoal"  # default color if not found
            

def write_to_db(db_file_path, attachments, items, labels, projects, sections):
    conn = sqlite3.connect(db_file_path)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS attachments
                 (id TEXT PRIMARY KEY, item_id TEXT, file_type TEXT, file_name TEXT, file_size NUMBER, file_path TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS items
                 (id TEXT PRIMARY KEY, content TEXT, description TEXT, due TEXT, added_at TEXT, completed_at TEXT, updated_at TEXT, section_id TEXT, project_id TEXT, parent_id TEXT, priority INTEGER, child_order INTEGER, checked INTEGER, is_deleted INTEGER, day_order INTEGER, collapsed INTEGER, pinned INTEGER, labels TEXT, extra_data TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS labels
                 (id TEXT PRIMARY KEY, name TEXT, color TEXT, item_order INTEGER, is_deleted INTEGER, is_favorite INTEGER, backend_type TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS projects
                 (id TEXT PRIMARY KEY, name TEXT, color TEXT, backend_type TEXT, inbox_project INTEGER, team_inbox INTEGER, child_order INTEGER, is_deleted INTEGER, is_archived INTEGER, is_favorite INTEGER, shared INTEGER, view_style TEXT, sort_order INTEGER, parent_id TEXT, collapsed INTEGER, icon_style TEXT, emoji TEXT, show_completed INTEGER, description TEXT, due_date TEXT, inbox_section_hidded INTEGER, sync_id TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS sections
                 (id TEXT PRIMARY KEY, name TEXT, archived_at TEXT, added_at TEXT, project_id TEXT, section_order INTEGER, collapsed INTEGER, is_deleted INTEGER, is_archived INTEGER, color TEXT, description TEXT, hidded INTEGER)''')

    for a in attachments:
        if not c.execute('''SELECT 1 FROM attachments WHERE id =?''', (a['id'],)).fetchone():
            c.execute('''INSERT INTO attachments (id, item_id, file_type, file_name, file_size, file_path) VALUES (?,?,?,?,?,?)''', (a['id'], a['item_id'], a['file_type'], a['file_name'], a['file_size'], a['file_path']))
    for i in items:
        if not c.execute('''SELECT 1 FROM items WHERE id =?''', (i['id'],)).fetchone():
            c.execute('''INSERT INTO items (id, content, description, due, added_at, completed_at, updated_at, section_id, project_id, parent_id, priority, child_order, checked, is_deleted, day_order, collapsed, pinned, labels, extra_data) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (i['id'], i['content'], i['description'], i['due'], i['added_at'], i['completed_at'], i['updated_at'], i['section_id'], i['project_id'], i['parent_id'], i['priority'], i['child_order'], i['checked'], i['is_deleted'], i['day_order'], i['collapsed'], i['pinned'], i['labels'], i['extra_data']))
    for l in labels:
        if not c.execute('''SELECT 1 FROM labels WHERE id =?''', (l['id'],)).fetchone() and not c.execute('''SELECT 1 FROM labels WHERE name =?''', (l['name'],)).fetchone():
            c.execute('''INSERT INTO labels (id, name, color, item_order, is_deleted, is_favorite, backend_type) VALUES (?,?,?,?,?,?,?)''', (l['id'], l['name'], l['color'], l['item_order'], l['is_deleted'], l['is_favorite'], l['backend_type']))
    for p in projects:
        if not c.execute('''SELECT 1 FROM projects WHERE id =?''', (p['id'],)).fetchone():
            c.execute('''INSERT INTO projects (id, name, color, backend_type, inbox_project, team_inbox, child_order, is_deleted, is_archived, is_favorite, shared, view_style, sort_order, parent_id, collapsed, icon_style, emoji, show_completed, description, due_date, inbox_section_hidded, sync_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (p['id'], p['name'], p['color'], p['backend_type'], p['inbox_project'], p['team_inbox'], p['child_order'], p['is_deleted'], p['is_archived'], p['is_favorite'], p['shared'], p['view_style'], p['sort_order'], p['parent_id'], p['collapsed'], p['icon_style'], p['emoji'], p['show_completed'], p['description'], p['due_date'], p['inbox_section_hidded'], p['sync_id']))
    for s in sections:
        if not c.execute('''SELECT 1 FROM sections WHERE id =?''', (s['id'],)).fetchone():
            c.execute('''INSERT INTO sections (id, name, archived_at, added_at, project_id, section_order, collapsed, is_deleted, is_archived, color, description, hidded) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''', (s['id'], s['name'], s['archived_at'], s['added_at'], s['project_id'], s['section_order'], s['collapsed'], s['is_deleted'], s['is_archived'], s['color'], s['description'], s['hidded']))

    conn.commit()
    conn.close()


    ### MAIN ###
def main():
    board = None
    while True:
        print("Select an option:")
        print("1. Import from Trello's .json")
        print("2. Export to Planify's .db")
        print("3. Print Board")
        print("4. Get Card")
        print("5. Get Label")
        print("6. Get List")
        print("7. Get Checklist")
        print("Q. Quit")
        option = input("> ").lower()

        if option == "1":
            json_file_path = input("Enter the path to the JSON file: ")
            if os.path.isfile(json_file_path):
                try:
                    with open(json_file_path, 'r') as f:
                        data = json.load(f)
                    board = Board()
                    board.import_from_trello(data)
                    print("Board imported successfully!")
                except json.JSONDecodeError:
                    print("Invalid JSON file. Please try again.")
            else:
                print("Invalid file path. Please try again.")
        elif option == "2":
            if board is None:
                print("Please import a board first.")
            else:
                try:
                    db_file_path = input("Enter the path to the .db file (perhaps check: ~/.var/app/io.github.alainm23.planify/data/io.github.alainm23.planify/database.db): ")
                    if db_file_path.startswith('~'):
                        db_file_path = os.path.join(os.path.expanduser('~'), db_file_path[1:])
                    if not os.path.exists(db_file_path):
                        os.makedirs(os.path.dirname(db_file_path), exist_ok=True)
                    attachments, items, labels, projects, sections = board.json_to_db()
                    write_to_db(db_file_path, attachments, items, labels, projects, sections)
                    print("Board exported successfully!")
                except Exception as e:
                    print("Error exporting board, likely incorrect path or insufficient permissions. Please try again.")
                    print("\tError:", e.args)
        elif option == "3":
            if board is not None:
                print(board)
            else:
                print("No board data available. Please import from Trello first.")
        elif option == "4":
            if board is not None:
                try:
                    ind = int(input("Enter the index: "))
                    print(board.get_card(ind))
                except:
                    print("Invalid index. Please try again.")
            else:
                print("No board data available. Please import from Trello first.")
        elif option == "5":
            if board is not None:
                try:
                    ind = int(input("Enter the index: "))
                    print(board.get_label(ind))
                except:
                    print("Invalid index. Please try again.")
            else:
                print("No board data available. Please import from Trello first.")
        elif option == "6":
            if board is not None:
                try:
                    ind = int(input("Enter the index: "))
                    print(board.get_list(ind))
                except:
                    print("Invalid index. Please try again.")
            else:
                print("No board data available. Please import from Trello first.")
        elif option == "7":
            if board is not None:
                try:
                    ind = int(input("Enter the index: "))
                    print(board.get_checklist(ind))
                except:
                    print("Invalid index. Please try again.")
            else:
                print("No board data available. Please import from Trello first.")
        elif option == "q":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
