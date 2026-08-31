# 🦊 JWT-Fox

Ferramenta focada em testes de segurança, auditoria e análise de JSON Web Tokens (JWT). O JWT-Fox permite a inspeção rápida de payloads, verificação de resistência de chaves secretas via brute force multithreaded e simulação de cenários de teste de manipulação de claims e algoritmos.

---

## Funcionalidades

* **Análise de Token:** Decodifica o header e o payload para visualização imediata das estruturas de dados.
* **Brute Force Otimizado:** Testa a resistência de chaves secretas (HS256) utilizando multithreading para alta performance.
* **Verificação de Algoritmo None:** Testa se a aplicação aceita a ausência de assinatura (`alg: none`).
* **Key Confusion Test:** Avalia a vulnerabilidade de troca de contexto entre RS256 e HS256 utilizando chaves públicas.
* **Manipulação de Claims:** Permite testar a integridade alterando claims específicas e reassinando o token com uma chave conhecida.

---

## Requisitos

* Python 3.8+
* PyJWT

```bash
pip install PyJWT
