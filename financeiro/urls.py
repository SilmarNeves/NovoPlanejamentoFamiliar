from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('financeiro/transacoes/', views.TransacaoListView.as_view(), name='transacoes'),
    path('financeiro/transacao/nova/', views.TransacaoCreateView.as_view(), name='transacao_create'),
    path('financeiro/transacao/<int:pk>/editar/', views.TransacaoUpdateView.as_view(), name='transacao_update'),
    path('financeiro/transacao/<int:pk>/excluir/', views.TransacaoDeleteView.as_view(), name='transacao_delete'),
    path('categorias/', views.CategoriaListView.as_view(), name='categorias'),
    path('categoria/nova/', views.CategoriaCreateView.as_view(), name='categoria_create'),
    path('categoria/<int:pk>/editar/', views.CategoriaUpdateView.as_view(), name='categoria_update'),
    path('categoria/<int:pk>/excluir/', views.CategoriaDeleteView.as_view(), name='categoria_delete'),
    path('resumo/', views.ResumoView.as_view(), name='resumo'),
    path('salvar-saldos-faturas/', views.salvar_saldos_faturas, name='salvar_saldos_faturas'),
    # outras urls...
]
