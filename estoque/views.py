from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Produto, MovimentacaoEstoque
from .forms import ProdutoForm, MovimentacaoEstoqueForm

@login_required
def listar_estoque(request):
    """
    Lista o estoque separado por categorias para facilitar a gestão da Ckaizen.
    """
    base_query = Produto.objects.filter(empresa=request.user.empresa).order_by('nome')
    
    context = {
        'materiais': base_query.filter(tipo='materia_prima'),
        'ativos': base_query.filter(tipo='ativo_imobilizado'),
        'consumo': base_query.filter(tipo='uso_consumo'),
    }
    
    return render(request, 'estoque/produto_list.html', context)

@login_required
def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            produto = form.save(commit=False)
            produto.empresa = request.user.empresa
            produto.save()
            return redirect('listar_estoque')
    else:
        form = ProdutoForm()
    return render(request, 'estoque/produto_form.html', {'form': form})

@login_required
def movimentar_estoque(request):
    if request.method == 'POST':
        form = MovimentacaoEstoqueForm(request.POST, empresa=request.user.empresa)
        if form.is_valid():
            movimentacao = form.save(commit=False)
            movimentacao.empresa = request.user.empresa
            movimentacao.save()
            return redirect('listar_estoque')
    else:
        form = MovimentacaoEstoqueForm(empresa=request.user.empresa)
    return render(request, 'estoque/movimentacao_form.html', {'form': form})