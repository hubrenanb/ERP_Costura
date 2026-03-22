from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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
    # NOME CORRIGIDO PARA BATER COM O ARQUIVO
    return render(request, 'core/cadastrar_cliente.html', {'form': form})

@login_required
def listar_clientes(request):
    clientes = Cliente.objects.filter(empresa=request.user.empresa, ativo=True)
    return render(request, 'core/cliente_list.html', {'clientes': clientes})