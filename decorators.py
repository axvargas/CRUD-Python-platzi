'''
Created Date: Monday September 13th 2021 8:24:24 pm
Author: Andrés X. Vargas
-----
Last Modified: Monday September 13th 2021 9:21:47 pm
Modified By: the developer known as Andrés X. Vargas at <axvargas@fiec.espol.edu.ec>
-----
Copyright (c) 2021 MattuApps
'''
PASSWPORD = "12345"


def password_required(func):
    def wrapper():
        password = input("Cual es tu contraseña: ")
        if password == PASSWPORD:
            return func()
        else:
            print("La contraseña es incorrecta")
    return wrapper


@password_required
def needs_password():
    print("Tu contraseña es correcta")


def upper(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper

@upper
def say_my_name(name):
    return (f"My name is {name}")

if __name__ == "__main__":
    needs_password()
    print(say_my_name("Andrés"))
