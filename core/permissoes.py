def is_gerente(user):
    # Verifica o campo 'tipo' que definimos no Model Usuario
    return user.is_authenticated and (user.tipo == 'gerente' or user.is_superuser)

def is_funcionario(user):
    return user.is_authenticated and (user.tipo == 'funcionario' or user.tipo == 'gerente')