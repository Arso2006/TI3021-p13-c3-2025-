import bcrypt 

# paso 1. obtener contraseña en plano
incoming_password = input("ingresa tu contraseña: ")
# paso 2. crear un pedazo de sal
salt = bcrypt.gensalt(rounds=12)
# paso 3. hashear la contraseña en plano y dar una sal al hasheo
hashed_password = bcrypt.hashpw(password=incoming_password, salt=salt)
print("contraseña hasheada", hashed_password)
#paso 4. ingresar de nuevo la contraseña
confirm_password = input("ingresa nuevamente la contraseña : ").encode("utf-8")
#paso 5. comparar contraseñas 
if bcrypt.checkpw(confirm_password, hashed_password):
    print ("contraseña correcta ")
else:
    print("contraseña incorrecta ")