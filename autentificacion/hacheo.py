import bcrypt

# ============================
# FUNCIONES DE HASHEO
# ============================

def generar_hash(password: str) -> bytes:
    """
    Genera un hash seguro usando bcrypt
    """
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt(rounds=12)
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password


def verificar_password(password_plano: str, password_hash: bytes) -> bool:
    """
    Verifica una contraseña contra su hash
    """
    return bcrypt.checkpw(
        password_plano.encode("utf-8"),
        password_hash
    )


# ============================
# DEMO (SE MANTIENE TU EJEMPLO)
# ============================

if __name__ == "__main__":
    incoming_password = input("Ingresa tu contraseña: ")
    hashed = generar_hash(incoming_password)
    print("Contraseña hasheada:", hashed)

    confirm_password = input("Ingresa nuevamente la contraseña: ")

    if verificar_password(confirm_password, hashed):
        print("Contraseña correcta")
    else:
        print("Contraseña incorrecta")
