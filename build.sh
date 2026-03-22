#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Instala as dependências
pip install -r requirements.txt

# 2. Coleta os arquivos estáticos (Resolve o visual quebrado)
python manage.py collectstatic --no-input

# 3. Aplica as migrações (Cria as tabelas no Postgres)
python manage.py migrate

# 4. CRIAÇÃO SEGURA DO SUPERUSUÁRIO (Ajustado para o seu modelo core.Usuario)
python manage.py shell <<EOF
from core.models import Usuario
import os

email_admin = os.getenv('ADMIN_EMAIL')
senha_admin = os.getenv('ADMIN_PASSWORD')

if email_admin and senha_admin:
    if not Usuario.objects.filter(email=email_admin).exists():
        # Removido o campo 'nome' que causou o erro anterior
        Usuario.objects.create_superuser(
            username=email_admin,
            email=email_admin, 
            password=senha_admin
        )
        print(f"SUCESSO: Superusuario {email_admin} criado.")
    else:
        print(f"AVISO: O usuario {email_admin} ja existe.")
else:
    print("ERRO: Variaveis ADMIN_EMAIL ou ADMIN_PASSWORD nao encontradas.")
EOF