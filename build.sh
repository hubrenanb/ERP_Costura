#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Instala as dependências
pip install -r requirements.txt

# 2. Coleta os arquivos estáticos (Resolve o visual quebrado)
python manage.py collectstatic --no-input

# 3. Aplica as migrações (Cria as tabelas no Postgres)
python manage.py migrate

# 4. CRIAÇÃO E ATUALIZAÇÃO DE USUÁRIOS (Garante login e senha corretos)
python manage.py shell <<EOF
from core.models import Usuario, Empresa
import os

# Garante que a empresa exista para vincular aos usuários
empresa, _ = Empresa.objects.get_or_create(nome_fantasia='Ckaizen Ateliê')

# --- CONFIGURAÇÃO DO SEU SUPERUSUÁRIO ---
admin_email = os.getenv('ADMIN_EMAIL')
admin_pass = os.getenv('ADMIN_PASSWORD')

if admin_email and admin_pass:
    # Busca ou cria o usuário pelo email/username
    u_admin, created = Usuario.objects.get_or_create(username=admin_email, email=admin_email)
    u_admin.set_password(admin_pass) # Força a senha correta e criptografada
    u_admin.is_superuser = True
    u_admin.is_staff = True
    u_admin.is_active = True
    u_admin.empresa = empresa
    u_admin.save()
    print(f"SUCESSO: Superusuario {admin_email} atualizado/criado.")

# --- CONFIGURAÇÃO DO USUÁRIO DE TESTE (GERENTE) ---
# Login: testando | Senha: senha_gerente_123
u_test, created = Usuario.objects.get_or_create(username='testando')
u_test.set_password('senha_gerente_123') 
u_test.is_staff = True   # Permite acessar o /admin
u_test.is_active = True
u_test.tipo = 'gerente'
u_test.empresa = empresa
u_test.save()
print("SUCESSO: Usuario 'testando' atualizado com senha 'senha_gerente_123'.")
EOF