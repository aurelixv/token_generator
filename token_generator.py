#!/usr/bin/env python3

import sys
import random
import time
from datetime import datetime
import hashing_algorithms as ha
import database as db

DATABASE = 'token_generator_data.json'

args = sys.argv[1:]

if len(args) < 2 or len(args) > 4:
    print('Para cadastrar novo usuario: [user] [senha semente] [senha local] [salt]')
    print('Para consultar tokens: [user] [senha local]')
    sys.exit()

print('Abrindo base...')
database = db.load_database(DATABASE)
print('Base aberta com sucesso.')

if len(args) == 4:
    username = args[0]
    seed_password = args[1]
    password = args[2]
    seed_salt = args[3]
    if username not in database:
        print('Cadastrando novo usuario...')
        hashed_seed = ha.hash_password(seed_password)
        hashed_password = ha.hash_password(password)
        password_salt = ha.salt_generator()
        content = {
            'senha_semente':ha.hash_password(hashed_seed + seed_salt),
            'senha_local':ha.hash_password(hashed_password + password_salt),
            'salt':password_salt
        }
        db.insert(database, username, content)
        print('Usuario cadastrado com sucesso.')
        print('Salvando base...')
        db.save_database(DATABASE, database)
        print('Base salva com sucesso.')
    else:
        print('Usuario ja cadastrado.')
    sys.exit()

if len(args) == 2:
    username = args[0]
    password = args[1]
    if username not in database:
        print('Usuario nao cadastrado.')
    else:
        print('Verificando senha...')
        if ha.verify_password(password, (database[username])['senha_local'], (database[username])['salt']):
            print('Usuario autenticado com sucesso.')
            print('Gerando tokens...')
            tokens = ha.generate_tokens((database[username])['senha_semente'])
            old_time = datetime.now().strftime('%H:%M')
            while(True):
                print(tokens)
                for token in tokens[::-1]:
                    print(token)
                    input()
                while old_time == datetime.now().strftime('%H:%M'):
                    time.sleep(1)     
                tokens = ha.generate_tokens((database[username])['senha_semente'])
                old_time = datetime.now().strftime('%H:%M')
        else:
            print('Falha na autenticacao.')
    sys.exit()
