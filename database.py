import json

def load_database(name):
    try:
        with open(name) as f:
            try:
                database = json.loads(f.read())
                return database
            except:
                print('[ ERRO ] Base corrompida, criando do zero.')
                return json.loads('{}')
    except:
        print('[ ERRO ] Base nao existe, criando novo arquivo.')
        save_database(name, {})
        return load_database(name)

def insert(database, username, content):
    database[username] = content

def save_database(name, database):
    with open(name, 'w') as f:
        f.write(json.dumps(database, indent=4))
