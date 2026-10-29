import bcrypt



def hash_pwd(password:str, rounds=12):
    pwd = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds))
    return pwd.decode()

def check_pwd(password:str,hashed_pwd:str) -> bool : 
    return bcrypt.checkpw(password.encode(), hashed_pwd.encode())