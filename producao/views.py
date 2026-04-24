from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from core.permissoes import is_gerente
from .models import Comanda, ItemComanda
from .forms import ComandaForm, ItemComandaFormSet

@login_required
def nova_comanda(request):
    if request.method == 'POST':
        form = ComandaForm(request.POST, empresa=request.user.empresa)
        formset = ItemComandaFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            comanda = form.save(commit=False)
            comanda.empresa = request.user.empresa
            comanda.save()
            formset.instance = comanda
            formset.save()
            comanda.atualizar_total()
            messages.success(request, f"Comanda #{comanda.id} criada com sucesso.")
            return redirect('listar_comandas')
    else:
        form = ComandaForm(empresa=request.user.empresa)
        formset = ItemComandaFormSet()

    return render(request, 'producao/comanda_form.html', {
        'form': form,
        'formset': formset,
        'editando': False
    })

@login_required
@user_passes_test(is_gerente, login_url='listar_comandas')
def editar_comanda(request, comanda_id):
    comanda = get_object_or_404(Comanda, id=comanda_id, empresa=request.user.empresa)
    if request.method == 'POST':
        form = ComandaForm(request.POST, instance=comanda, empresa=request.user.empresa)
        formset = ItemComandaFormSet(request.POST, instance=comanda)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            comanda.atualizar_total()
            messages.success(request, f"Comanda #{comanda.id} atualizada com sucesso.")
            return redirect('listar_comandas')
    else:
        form = ComandaForm(instance=comanda, empresa=request.user.empresa)
        formset = ItemComandaFormSet(instance=comanda)

    return render(request, 'producao/comanda_form.html', {
        'form': form,
        'formset': formset,
        'editando': True
    })

@login_required
def listar_comandas(request):
    comandas = Comanda.objects.filter(
        empresa=request.user.empresa,
        ativo=True
    ).exclude(status='entregue').order_by('data_entrega_prevista')

    origem = request.GET.get('origem')
    tipo_servico = request.GET.get('tipo_servico')

    if origem:
        comandas = comandas.filter(origem=origem)
    if tipo_servico:
        comandas = comandas.filter(itens__tipo_servico=tipo_servico).distinct()

    return render(request, 'producao/comanda_list.html', {
        'comandas': comandas,
        'status_opcoes': Comanda.STATUS_CHOICES,
        'origem_opcoes': Comanda.ORIGEM_CHOICES,
        'tipo_servico_opcoes': ItemComanda.TIPO_SERVICO_CHOICES,
        'filtro_origem': origem or '',
        'filtro_tipo_servico': tipo_servico or '',
    })

@login_required
def atualizar_status(request, comanda_id):
    if request.method == 'POST':
        comanda = get_object_or_404(Comanda, id=comanda_id, empresa=request.user.empresa)
        novo_status = request.POST.get('status')

        if novo_status in ['pronto', 'entregue'] and comanda.saldo_devedor > 0:
            messages.error(request, f"Ação bloqueada: a comanda #{comanda.id} possui saldo devedor.")
            return redirect('listar_comandas')

        if novo_status:
            comanda.status = novo_status
            comanda.save(update_fields=['status'])
            messages.success(request, f"Status da comanda #{comanda.id} atualizado.")

    return redirect('listar_comandas')

@login_required
def imprimir_comanda(request, comanda_id):
    comanda = get_object_or_404(Comanda, id=comanda_id, empresa=request.user.empresa)
    return render(request, 'producao/imprimir_comanda.html', {'comanda': comanda})

@login_required
@user_passes_test(is_gerente, login_url='listar_comandas')
def remover_comanda(request, comanda_id):
    if request.method == 'POST':
        comanda = get_object_or_404(Comanda, id=comanda_id, empresa=request.user.empresa)
        comanda.ativo = False
        comanda.save(update_fields=['ativo'])
        messages.success(request, f"Comanda #{comanda.id} removida do sistema.")
    return redirect('listar_comandas')