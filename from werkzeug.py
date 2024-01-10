from werkzeug.security import check_password_hash, generate_password_hash

secret = '12345'

hash = generate_password_hash(secret)
print(check_password_hash(hash, secret))
print(len(hash))
