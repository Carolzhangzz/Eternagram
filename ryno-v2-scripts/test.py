from werkzeug.security import generate_password_hash, check_password_hash

# A password is chosen
password = '60'

hashed_password1 = generate_password_hash(password)

test1 = 'pbkdf2:sha256:260000$nWrLtZclvzugg8xM$9158c0b6d157269346c9f5d71214d3e6062f21f2637f125266b27fc6872dad5b'

print(check_password_hash(test1, password))