#!/usr/bin/env python3

import sys
import json
import hashlib
import random

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

def hash_password(password, salt):
    hashed_password = hashlib.sha512(password.encode('utf-8')).hexdigest()
    hashed_salt = hashlib.sha512(str(salt).encode('utf-8')).hexdigest()
    hashed_password = hashlib.sha512(
        str(hashed_password).encode('utf-8') + str(hashed_salt).encode('utf-8')
        ).hexdigest()
    return hashed_password

def insert(database, content):
    salt = int(random.random()*1000)
    hashed_seed = hash_password(content[1], salt)
    hashed_password = hash_password(content[2], salt)
    database[content[0]] = {'senha_semente':hashed_seed, 'senha_local':hashed_password, 'salt':salt}

def verify_password(password, hashed_password, salt):
    password = hash_password(password, salt)
    if password == hashed_password:
        return 1
    return 0

def save_database(name, database):
    with open(name, 'w') as f:
        f.write(json.dumps(database))

args = sys.argv[1:]

if len(args) < 2 or len(args) > 3:
    print('Para cadastrar novo user: [user] [senha semente] [senha local]')
    print('Para consultar tokens: [user] [senha local]')
    sys.exit()

print('Abrindo base...')
db = load_database('gerador_senhas.json')
print('Base aberta com sucesso.')

if len(args) == 3:
    username = args[0]
    if username not in db:
        print('Cadastrando novo usuario...')
        insert(db, args)
        print('Usuario cadastrado com sucesso.')
        print('Salvando base...')
        save_database('database.json', db)
        print('Base salva com sucesso.')
    else:
        print('Usuario ja cadastrado.')
    sys.exit()

if len(args) == 2:
    username = args[0]
    password = args[1]
    if username not in db:
        print('Usuario nao cadastrado.')
    else:
        print('Verificando senha...')
        if verify_password(password, (db[username])['senha_local'], (db[username])['salt']):
            print('Usuario autenticado com sucesso.')
        else:
            print('Falha na autenticacao.')
    sys.exit()

