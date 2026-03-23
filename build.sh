#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Instala as dependências
pip install -r requirements.txt

# 2. Coleta os arquivos estáticos
python manage.py collectstatic --no-input

# 3. LIMPEZA PRÉ-MIGRAÇÃO (Resolve o erro IntegrityError de duplicados)
# Aqui removemos os usuários que estão impedindo o banco de criar a regra de e-mail único
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
# Remove TODOS os usuários para resetar o ambiente de acesso e permitir a migração única
User.objects.all().delete()
print("Banco limpo para migração.")
EOF

# 4. Aplica as migrações (Agora vai funcionar pois não há duplicados)
python manage.py migrate

# 5. RECRIAÇÃO DOS ACESSOS OFICIAIS
python manage.py shell <<EOF
from core.models import Usuario, Empresa
import os

empresa, _ = Empresa.objects.get_or_create(nome_fantasia='Ckaizen Ateliê')

admin_email = os.getenv('ADMIN_EMAIL')
admin_pass = os.getenv('ADMIN_PASSWORD')

# Recria seu Admin
if admin_email and admin_pass:
    u_admin = Usuario.objects.create_superuser(
        username=admin_email.split('@'),
        email=admin_email,
        password=admin_pass,
        empresa=empresa
    )
    print(f"Admin {admin_email} recriado.")

# Recria o Gerente de Teste
gerente_email = 'gerente@ckaizen.com.br'
u_test = Usuario.objects.create(
    username='gerente_ckaizen',
    email=gerente_email,
    is_staff=True,
    is_active=True,
    tipo='gerente',
    empresa=empresa
)
u_test.set_password('senha_gerente_123')
u_test.save()
print(f"Gerente {gerente_email} recriado.")
EOF