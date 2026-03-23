#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Instala as dependências
pip install -r requirements.txt

# 2. Coleta os arquivos estáticos
python manage.py collectstatic --no-input

# 3. Aplica as migrações (Crucial para o novo modelo de e-mail)
python manage.py migrate

# 4. CONFIGURAÇÃO DE ACESSOS VIA E-MAIL (Limpeza e Criação)
python manage.py shell <<EOF
from core.models import Usuario, Empresa
import os

# Garante a empresa base para evitar Erro 500 ao salvar registros
empresa, _ = Empresa.objects.get_or_create(nome_fantasia='Ckaizen Ateliê')

# --- LIMPEZA DE SEGURANÇA ---
# Remove usuários que não seguem a nova regra de e-mail único ou nomes antigos
Usuario.objects.filter(email='').delete()
Usuario.objects.filter(username='testando').delete()

# --- SEU SUPERUSUÁRIO ---
admin_email = os.getenv('ADMIN_EMAIL')
admin_pass = os.getenv('ADMIN_PASSWORD')

if admin_email and admin_pass:
    # Busca ou cria pelo email (novo padrão)
    u_admin, created = Usuario.objects.get_or_create(
        email=admin_email, 
        defaults={'username': admin_email.split('@')}
    )
    # Forçamos as permissões e a senha correta (hasheada)
    u_admin.set_password(admin_pass)
    u_admin.is_superuser = True
    u_admin.is_staff = True
    u_admin.is_active = True
    u_admin.empresa = empresa
    u_admin.save()
    print(f"SUCESSO: Superusuario {admin_email} pronto e atualizado.")

# --- USUÁRIO GERENTE (TESTE) ---
# Login: gerente@ckaizen.com.br | Senha: senha_gerente_123
gerente_email = 'gerente@ckaizen.com.br'
u_test, created = Usuario.objects.get_or_create(
    email=gerente_email,
    defaults={'username': 'gerente_ckaizen'}
)

u_test.set_password('senha_gerente_123')
u_test.is_staff = True
u_test.is_active = True
u_test.tipo = 'gerente'
u_test.empresa = empresa
u_test.save()
print(f"SUCESSO: Gerente {gerente_email} pronto para login.")

EOF