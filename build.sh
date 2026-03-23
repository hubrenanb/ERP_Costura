#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

python manage.py shell <<EOF
from core.models import Usuario, Empresa
import os

# 1. Garante a empresa base
empresa, _ = Empresa.objects.get_or_create(nome_fantasia='Ckaizen Ateliê')

# 2. RESGATE DO SUPERUSUÁRIO
# Puxa os dados direto das variáveis de ambiente do Render
admin_email = os.getenv('ADMIN_EMAIL')
admin_pass = os.getenv('ADMIN_PASSWORD')

if admin_email and admin_pass:
    u_admin, created = Usuario.objects.get_or_create(
        email=admin_email, 
        defaults={'username': admin_email.split('@')}
    )
    # Sobrescreve a senha a cada deploy para garantir o resgate
    u_admin.set_password(admin_pass)
    u_admin.is_superuser = True
    u_admin.is_staff = True
    u_admin.is_active = True
    u_admin.empresa = empresa
    u_admin.save()
    print(f"SUCESSO: Superusuario {admin_email} resgatado e senha sincronizada.")
else:
    print("ERRO: Variaveis ADMIN_EMAIL ou ADMIN_PASSWORD ausentes no Render.")

# 3. CRIAÇÃO DAS GERENTES (Nathalya e Luciana)
gerentes = [
    {'email': 'nathalya@ckaizen.com', 'username': 'nathalya_gerente'},
    {'email': 'luciana@ckaizen.com', 'username': 'luciana_gerente'}
]

for g in gerentes:
    u_gerente, created = Usuario.objects.get_or_create(
        email=g['email'],
        defaults={'username': g['username']}
    )
    
    # Define a senha apenas na criação para não apagar se elas alterarem depois
    if created:
        u_gerente.set_password('Mudar@123')
        u_gerente.is_staff = True
        u_gerente.is_active = True
        u_gerente.tipo = 'gerente'
        u_gerente.empresa = empresa
        u_gerente.save()
        print(f"SUCESSO: Gerente {g['email']} criada com senha padrao.")
    else:
        print(f"AVISO: Gerente {g['email']} ja existe. Senha mantida intacta.")
EOF