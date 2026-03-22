#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Instala as dependências
pip install -r requirements.txt

# 2. Coleta os arquivos estáticos
python manage.py collectstatic --no-input

# 3. Aplica as migrações no banco de dados
python manage.py migrate

# 4. CRIAÇÃO SEGURA DO SUPERUSUÁRIO (Lendo do Environment)
python manage.py shell <<EOF
from core.models import Usuario
import os

# Puxa os dados que você acabou de salvar no Render
email_admin = os.getenv('ADMIN_EMAIL')
senha_admin = os.getenv('ADMIN_PASSWORD')

if email_admin and senha_admin:
    if not Usuario.objects.filter(email=email_admin).exists():
        Usuario.objects.create_superuser(
            email=email_admin, 
            password=senha_admin, 
            nome='Admin Ckaizen'
        )
        print(f"SUCESSO: Superusuario {email_admin} criado via Environment.")
    else:
        print(f"AVISO: O usuario {email_admin} ja existe.")
else:
    print("ERRO: Variaveis ADMIN_EMAIL ou ADMIN_PASSWORD nao encontradas.")
EOF