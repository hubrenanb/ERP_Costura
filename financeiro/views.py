import csv
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Q
from django.db.models.functions import TruncDate
from core.permissoes import is_gerente
from producao.models import Comanda
from .models import Transacao
from .forms import PagamentoComandaForm, TransacaoForm # Certifique-se de criar o TransacaoForm

@login_required
def listar_transacoes(request):
    """
    Lista todas as movimentações financeiras e permite o lançamento 
    de despesas manuais (limpeza, compras de material, etc).
    """
    transacoes = Transacao.objects.filter(empresa=request.user.empresa).order_by('-data_transacao')
    
    # Resumo para os cards do topo
    receitas = transacoes.filter(tipo='receita').aggregate(total=Sum('valor'))['total'] or 0
    despesas = transacoes.filter(tipo='despesa').aggregate(total=Sum('valor'))['total'] or 0
    saldo = receitas - despesas

    if request.method == 'POST':
        form = TransacaoForm(request.POST)
        if form.is_valid():
            nova_transacao = form.save(commit=False)
            nova_transacao.empresa = request.user.empresa
            # Se for lançamento manual, garantimos que categorias de despesa sejam tratadas
            nova_transacao.save()
            return redirect('listar_transacoes')
    else:
        form = TransacaoForm()

    return render(request, 'financeiro/transacoes.html', {
        'transacoes': transacoes,
        'form': form,
        'receitas': receitas,
        'despesas': despesas,
        'saldo': saldo,
    })

@login_required
def registrar_pagamento(request, comanda_id):
    comanda = get_object_or_404(Comanda, id=comanda_id, empresa=request.user.empresa)
    
    if request.method == 'POST':
        form = PagamentoComandaForm(request.POST)
        if form.is_valid():
            transacao = form.save(commit=False)
            transacao.comanda = comanda
            transacao.empresa = request.user.empresa
            transacao.tipo = 'receita'
            transacao.categoria = 'venda' # Categoria automática para comandas
            transacao.save()
            return redirect('listar_comandas')
    else:
        form = PagamentoComandaForm(initial={
            'descricao': f'Pagamento Comanda #{comanda.id}',
            'valor': comanda.saldo_devedor
        })

    return render(request, 'financeiro/pagamento_form.html', {
        'form': form, 
        'comanda': comanda
    })

@login_required
@user_passes_test(is_gerente, login_url='listar_comandas')
def dashboard_financeiro(request):
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    base_query = Transacao.objects.filter(empresa=request.user.empresa)

    if data_inicio and data_fim:
        base_query = base_query.filter(data_transacao__date__gte=data_inicio, data_transacao__date__lte=data_fim)

    receitas = base_query.filter(tipo='receita').aggregate(total=Sum('valor'))['total'] or 0
    despesas = base_query.filter(tipo='despesa').aggregate(total=Sum('valor'))['total'] or 0
    saldo_caixa = float(receitas) - float(despesas)

    comandas_abertas = Comanda.objects.filter(empresa=request.user.empresa).exclude(status='entregue').count()

    # Dados por Categoria para gráfico de pizza
    por_categoria = base_query.values('categoria').annotate(total=Sum('valor'))

    # Dados para o Gráfico de Linha (Tempo)
    transacoes_por_dia = base_query.annotate(
        data=TruncDate('data_transacao')
    ).values('data').annotate(
        receita_diaria=Sum('valor', filter=Q(tipo='receita')),
        despesa_diaria=Sum('valor', filter=Q(tipo='despesa'))
    ).order_by('data')

    datas = [t['data'].strftime('%d/%m/%Y') for t in transacoes_por_dia if t['data']]
    receitas_chart = [float(t['receita_diaria'] or 0) for t in transacoes_por_dia]
    despesas_chart = [float(t['despesa_diaria'] or 0) for t in transacoes_por_dia]

    return render(request, 'financeiro/dashboard.html', {
        'receitas': receitas, 
        'despesas': despesas, 
        'saldo_caixa': saldo_caixa,
        'comandas_abertas': comandas_abertas, 
        'datas_json': json.dumps(datas),
        'receitas_json': json.dumps(receitas_chart), 
        'despesas_json': json.dumps(despesas_chart),
        'data_inicio': data_inicio or '', 
        'data_fim': data_fim or '',
    })

@login_required
@user_passes_test(is_gerente, login_url='listar_comandas')
def exportar_relatorio_comandas(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="relatorio_financeiro.csv"'

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID', 'Cliente', 'Entrada', 'Previsão', 'Total', 'Saldo', 'Status'])

    comandas = Comanda.objects.filter(empresa=request.user.empresa).select_related('cliente')
    
    for comanda in comandas:
        writer.writerow([
            comanda.id, 
            comanda.cliente.nome_completo,
            comanda.data_entrada.strftime('%d/%m/%Y') if comanda.data_entrada else '',
            comanda.data_entrega_prevista.strftime('%d/%m/%Y') if comanda.data_entrega_prevista else '',
            str(comanda.valor_total).replace('.', ','),
            str(comanda.saldo_devedor).replace('.', ','),
            comanda.get_status_display()
        ])
    return response