# JWT-Fox

Ferramenta focada em testes de segurança, auditoria e análise de JSON Web Tokens (JWT). O JWT-Fox permite a inspeção rápida de payloads, verificação de resistência de chaves secretas via brute force multithreaded e simulação de cenários de teste de manipulação de claims e algoritmos.

## Funcionalidades

- **Análise de Token:** Decodifica o header e o payload para visualização imediata das estruturas de dados.
- **Brute Force Otimizado:** Testa a resistência de chaves secretas (HS256) utilizando multithreading para alta performance.
- **Verificação de Algoritmo None:** Testa se a aplicação aceita a ausência de assinatura (alg: none).
- **Key Confusion Test:** Avalia a vulnerabilidade de troca de contexto entre RS256 e HS256 utilizando chaves públicas.
- **Manipulação de Claims:** Permite testar a integridade alterando claims específicas e reassinando o token com uma chave conhecida.

## Requisitos

- Python 3.8+
- PyJWT

```bash
pip install PyJWT
```

## Como Usar

### 1. Analisar um Token

Exibe os dados decodificados do header e payload:

```bash
python jwt_fox.py -t <token> -s
```

### 2. Testar Resistência da Chave (Brute Force)

Verifica se a chave secreta consta em uma lista de dicionário:

```bash
python jwt_fox.py -t <token> -w wordlist.txt
```

### 3. Teste de Algoritmo none

Valida se o token é aceito sem assinatura:

```bash
python jwt_fox.py -t <token> --none
```

### 4. Teste de Edição de Claims

Modifica propriedades do payload para validar a checagem de integridade:

```bash
python jwt_fox.py -t <token> -k <chave_secreta> -m admin=true
```

### 5. Teste de Confusão de Chaves (Key Confusion)

Simula o cenário de substituição de chave assimétrica por simétrica:

```bash
python jwt_fox.py -t <token> --conf public_key.pem
```

## Uso Responsável

Esta ferramenta foi desenvolvida exclusivamente para fins educacionais, auditorias autorizadas e testes de segurança em ambientes controlados.
