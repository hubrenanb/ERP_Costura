from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ClienteForm
from .models import Cliente

@login_required
def cadastrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.empresa = request.user.empresa
            cliente.save()
            return redirect('nova_comanda')
    else:
        form = ClienteForm()
    return render(request, 'core/cadastrar_cliente.html', {'form': form})

@login_required
def listar_clientes(request):
    clientes = Cliente.objects.filter(empresa=request.user.empresa, ativo=True)
    return render(request, 'core/cliente_list.html', {'clientes': clientes})

@login_required
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id, empresa=request.user.empresa)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, f"Cliente {cliente.nome_completo} atualizado com sucesso.")
            return redirect('listar_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'core/editar_cliente.html', {'form': form, 'cliente': cliente})

@login_required
def inativar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id, empresa=request.user.empresa)
    if request.method == 'POST':
        cliente.ativo = False
        cliente.save()
        messages.success(request, f"Cliente {cliente.nome_completo} removido do sistema.")
    return redirect('listar_clientes')