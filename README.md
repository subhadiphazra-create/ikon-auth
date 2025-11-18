# ikon-auth

**ikon-auth** is a reusable authentication and authorization library designed for FastAPI microservices.  
It provides an OAuth2 client credentials token generator and JWT verification using JWKS public keys, enabling secure inter-service communication without duplicating authentication logic.

---

## 🚀 Features

- OAuth2 Client Credentials token generation
- JWT validation using JWKS public keys
- FastAPI-ready `verify_token` dependency
- Thread-safe token caching & auto refresh
- Seamless environment configuration using `pydantic-settings`
- Plug-and-play security for microservices architectures

---

## 📦 Installation

```bash
pip install ikon-auth
````

---

## ⚙️ Environment Configuration

Create a `.env` file in the root of your FastAPI application (not inside the package):

```env
BASE_ISSUER_URL=https://example.com/issuer
OAUTH_CLIENT_ID=my-client-id
OAUTH_CLIENT_SECRET=my-client-secret
```

These environment values are automatically loaded when you import components from `ikon-auth`.

---

## 🛠 Usage with FastAPI

### JWT Verification Dependency

```python
from fastapi import FastAPI, Depends
from ikon_auth import verify_token

app = FastAPI()

@app.get("/secure", dependencies=[Depends(verify_token)])
def secure_route(claims=Depends(verify_token)):
    return {"status": "access granted", "claims": claims}
```

### Example Router Usage

```python
from fastapi import APIRouter, Depends
from ikon_auth import verify_token

router = APIRouter(prefix="/items", tags=["Items"])

@router.get("/", dependencies=[Depends(verify_token)])
def list_items():
    return {"items": []}
```



## 🔐 Generating Access Tokens Programmatically

```python
from ikon_auth import OAuthProvider

provider = OAuthProvider()
token = provider.get_token()
print(token)  # Bearer <access_token>
```
### ‼️FOR ALL TYPE OF FRAMEWORK USAGE PLEASE CHECK THE EXAMPLE ‼️

---

## 📡 How Verification Works

1. Loads JWKS configuration from:

   ```
   <BASE_ISSUER_URL>/platform/.well-known/openid-configuration
   ```
2. Downloads signing public keys (JWKS)
3. Validates signature, issuer, and token expiration
4. Makes verified claims available to your route

---

## 🧪 Example Project Structure

```
my-fastapi-service/
│
├── app/main.py
├── app/routers/
├── .env   ← contains environment variables
└── requirements.txt
```

---

## 🎯 Ideal Use Cases

* Internal microservice authentication
* Internal gateway or API management
* Centralized authentication logic for multiple Python services
* Reusable token verification and security layer

---

## 🧱 Requirements

| Dependency        | Version |
| ----------------- | ------- |
| Python            | 3.10+   |
| FastAPI           | 0.110+  |
| pydantic-settings | 2.0+    |
| python-jose       | 3.3+    |
| cryptography      | latest  |

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 🧠 Contributing

Contributions and improvements are always welcome.
Please open an issue or submit a pull request on GitHub.

---

## 🌍 Links

| Resource          | Link                                                                                         |
| ----------------- | -------------------------------------------------------------------------------------------- |
| PyPI Package      | [https://pypi.org/project/ikon-auth](https://pypi.org/project/ikon-auth/)                     |
| Issues            | [https://github.com/subhadiphazra-create/ikon-auth/issues](https://github.com/subhadiphazra-create/ikon-auth/issues) |
| GitHub Repository | [https://github.com/subhadiphazra-create/ikon-auth](https://github.com/subhadiphazra-create/ikon-auth)               |


---



