#!/bin/bash
cd "$(dirname "$0")"
# ключ береться зі змінної середовища, у коді його немає
export JWT_KEY="${JWT_KEY:-$(python3 -c 'import secrets;print(secrets.token_hex(32))')}"
python3 app.py strict 5002
