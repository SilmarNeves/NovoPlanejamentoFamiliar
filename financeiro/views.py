from django.shortcuts import render
from django.contrib.auth.views import LoginView, PasswordResetView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Sum
import json
from calendar import month_name
from datetime import datetime
from .models import Categoria, Transacao, SaldosFaturas
from django.urls import reverse_lazy, reverse


def index(request):
    return render(request, 'base.html')

class LoginUsuarioView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('transacoes')

class RecuperarSenhaView(PasswordResetView):
    template_name = 'recuperar_senha.html'
    email_template_name = 'email/recuperar_senha_email.html'
    success_url = reverse_lazy('password_reset_done')

class ResumoView(LoginRequiredMixin, TemplateView):
    template_name = 'resumo/resumo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['saldos_faturas'] = SaldosFaturas.objects.last()
        
        mes_selecionado = int(self.request.GET.get('mes', datetime.now().month))
        ano_selecionado = int(self.request.GET.get('ano', datetime.now().year))

        context['meses'] = [(i, month_name[i]) for i in range(1, 13)]
        
        ano_atual = datetime.now().year
        context['anos'] = range(ano_atual - 4, ano_atual + 1)
        
        context['mes_selecionado'] = mes_selecionado
        context['ano_selecionado'] = ano_selecionado

        transacoes = Transacao.objects.filter(
            data__month=mes_selecionado,
            data__year=ano_selecionado
        )

        context['total_receitas'] = transacoes.filter(tipo='R').aggregate(
            total=Sum('valor'))['total'] or 0
        context['total_despesas'] = transacoes.filter(tipo='D').aggregate(
            total=Sum('valor'))['total'] or 0
        context['saldo'] = context['total_receitas'] - context['total_despesas']

        return context

class CategoriaListView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'categorias/lista.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        columns = ['Nome', 'Ações']
        
        table_data = [
            [
                categoria.nome,
                f'''
                <a href="{reverse('categoria_update', args=[categoria.id])}" class="br-button secondary circle small">
                    <i class="fas fa-edit" aria-hidden="true"></i>
                </a>
                <a href="{reverse('categoria_delete', args=[categoria.id])}" class="br-button danger circle small">
                    <i class="fas fa-trash-alt" aria-hidden="true"></i>
                </a>
                '''
            ] for categoria in self.get_queryset()
        ]

        grid_context = {
            'title': 'Lista de Categorias',
            'columns': columns,
            'table_data': table_data
        }

        context['grid_content'] = render_to_string('components/ggrid.html', grid_context)
        return context


class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    fields = ['nome']
    template_name = 'categorias/form.html'
    success_url = reverse_lazy('categorias')

class CategoriaUpdateView(LoginRequiredMixin, UpdateView):
    model = Categoria
    fields = ['nome']
    template_name = 'categorias/form.html'
    success_url = reverse_lazy('categorias')

class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'categorias/delete.html'
    success_url = reverse_lazy('categorias')



class TransacaoListView(LoginRequiredMixin, ListView):
    model = Transacao
    template_name = 'transacoes/lista.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        columns = ['Data', 'Tipo', 'Descrição', 'Categoria', 'Valor', 'Ações']
        
        table_data = [
            [
                transacao.data.strftime('%d/%m/%Y'),
                transacao.get_tipo_display(),
                transacao.descricao,
                transacao.categoria.nome,
                f'R$ {transacao.valor:,.2f}',
                f'''
                <a href="{reverse('transacao_update', args=[transacao.id])}" class="br-button secondary circle small">
                    <i class="fas fa-edit" aria-hidden="true"></i>
                </a>
                <a href="{reverse('transacao_delete', args=[transacao.id])}" class="br-button danger circle small">
                    <i class="fas fa-trash-alt" aria-hidden="true"></i>
                </a>
                '''
            ] for transacao in self.get_queryset()
        ]

        grid_context = {
            'title': 'Lista de Transações',
            'columns': columns,
            'table_data': table_data
        }

        context['grid_content'] = render_to_string('components/ggrid.html', grid_context)
        return context

from django.utils import timezone

class TransacaoCreateView(LoginRequiredMixin, CreateView):
    model = Transacao
    fields = ['data', 'tipo', 'descricao', 'categoria', 'valor']
    template_name = 'transacoes/form.html'
    success_url = reverse_lazy('transacoes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['today'] = timezone.now().strftime('%Y-%m-%d')
        return context

class TransacaoUpdateView(LoginRequiredMixin, UpdateView):
    model = Transacao
    fields = ['data', 'tipo', 'descricao', 'categoria', 'valor']
    template_name = 'transacoes/form.html'
    success_url = reverse_lazy('transacoes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context

class TransacaoDeleteView(LoginRequiredMixin, DeleteView):
    model = Transacao
    template_name = 'transacoes/delete.html'
    success_url = reverse_lazy('transacoes')

@require_POST
def salvar_saldos_faturas(request):
    try:
        data = json.loads(request.body)
        saldos_faturas, created = SaldosFaturas.objects.update_or_create(
            defaults={
                'saldo_bradesco': data['saldo_bradesco'],
                'saldo_itau': data['saldo_itau'],
                'saldo_inter': data['saldo_inter'],
                'fatura_bradesco': data['fatura_bradesco'],
                'fatura_itau': data['fatura_itau'],
                'fatura_inter': data['fatura_inter']
            }
        )
        return JsonResponse({
            'status': 'success',
            'message': 'Dados salvos com sucesso!'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })
