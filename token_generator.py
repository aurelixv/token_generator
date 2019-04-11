#!/usr/bin/env python3

import sys
import random
import hashing_algorithms as ha
import database as db

DATABASE = 'users_data.json'

args = sys.argv[1:]

if len(args) < 2 or len(args) > 3:
    print('Para cadastrar novo usuario: [user] [senha semente] [senha local]')
    print('Para consultar tokens: [user] [senha local]')
    sys.exit()

print('Abrindo base...')
database = db.load_database(DATABASE)
print('Base aberta com sucesso.')

if len(args) == 3:
    username = args[0]
    seed_password = args[1]
    password = args[2]
    if username not in database:
        print('Cadastrando novo usuario...')
        salt = random.random()
        content = {
            'senha_semente':ha.hash_password(seed_password, salt),
            'senha_local':ha.hash_password(password, salt)
        }
        db.insert(database, username, content)
        print('Usuario cadastrado com sucesso.')
        print('Seed: ' + (database[username])['senha_semente'])
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
        else:
            print('Falha na autenticacao.')
    sys.exit()
