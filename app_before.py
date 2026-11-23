import os, sys, time, jwt
from flask import Flask, request, jsonify

KEY = os.environ["JWT_KEY"]
MODE = sys.argv[1]            # naive | strict
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
        if MODE == "naive":
            # наївно: підпис і claims не перевіряються
            claims = jwt.decode(tok, options={"verify_signature": False})
        else:
            claims = jwt.decode(tok, KEY, algorithms=["HS256"],
                                issuer="lab7", audience="students")
    except jwt.InvalidTokenError as e:
        return jsonify(error=type(e).__name__, detail=str(e)), 401
    return jsonify(server=MODE, sub=claims.get("sub"), role=claims.get("role"))


app.run(port=PORT)
