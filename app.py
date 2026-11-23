import sys, time, jwt
from flask import Flask, request, jsonify

KEY = "lab7-secret-key-0123456789abcdef"
PORT = int(sys.argv[2])
app = Flask(__name__)


@app.post("/login")
def login():
    now = int(time.time())
    claims = {"sub": "user1", "role": "user", "iss": "lab7", "aud": "students",
              "iat": now, "exp": now + 3600}
    return jsonify(token=jwt.encode(claims, KEY, algorithm="HS256"))


@app.get("/api")
def api():
    tok = request.headers.get("Authorization", "").removeprefix("Bearer ")
    try:
        claims = jwt.decode(tok, KEY, algorithms=["HS256"],
                            issuer="lab7", audience="students")
    except jwt.InvalidTokenError as e:
        return jsonify(error=type(e).__name__, detail=str(e)), 401
    return jsonify(server=sys.argv[1], sub=claims.get("sub"), role=claims.get("role"))


app.run(port=PORT)
