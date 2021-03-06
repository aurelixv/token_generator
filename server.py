#!/usr/bin/env python3

import sys
from datetime import datetime
import hashing_algorithms as ha
import database as db

DATABASE = 'server_data.json'

args = sys.argv[1:]

if len(args) < 1 or len(args) > 2:
    print('Para cadastrar novo usuario: [user] [senha semente]')
    print('Para validar tokens: [user]')
    sys.exit()

print('Abrindo base...')
database = db.load_database(DATABASE)
print('Base aberta com sucesso.')

if len(args) == 2:
    username = args[0]
    seed_password = args[1]
    if username not in database:
        print('Cadastrando novo usuario...')
        salt = ha.salt_generator()
        hashed_seed = ha.hash_password(seed_password)
        content = {
            'senha_semente':ha.hash_password(hashed_seed + salt),
            'salt':salt
        }
        db.insert(database, username, content)
        print('Usuario cadastrado com sucesso.')
        print('Salt: ' + (database[username])['salt'])
        print('Salvando base...')
        db.save_database(DATABASE, database)
        print('Base salva com sucesso.')
    else:
        print('Usuario ja cadastrado.')
    sys.exit()

if len(args) == 1:
    username = args[0]
    if username not in database:
        print('Usuario nao cadastrado.')
    else:
        tokens = ha.generate_tokens((database[username])['senha_semente'])
        old_time = datetime.now().strftime('%H:%M')
        while(True):
            token = input('Digite o token: ')
            new_time = datetime.now().strftime('%H:%M')
            if old_time != new_time:
                tokens = ha.generate_tokens((database[username])['senha_semente'])
                old_time = new_time
            if token in tokens:
                tokens = tokens[:tokens.index(token)]
                print('Token valido.')
            else:
                print('Token invalido.')
    sys.exit()
