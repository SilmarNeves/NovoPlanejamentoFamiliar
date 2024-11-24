from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.LoginUsuarioView.as_view(), name='login'),
    path('recuperar-senha/', views.RecuperarSenhaView.as_view(), name='recuperar_senha'),
    path('financeiro/transacoes/', views.TransacaoListView.as_view(), name='transacoes'),
    path('financeiro/transacao/nova/', views.TransacaoCreateView.as_view(), name='transacao_create'),
    path('financeiro/transacao/<int:pk>/editar/', views.TransacaoUpdateView.as_view(), name='transacao_update'),
    path('financeiro/transacao/<int:pk>/excluir/', views.TransacaoDeleteView.as_view(), name='transacao_delete'),
    path('categorias/', views.CategoriaListView.as_view(), name='categorias'),
    path('categoria/nova/', views.CategoriaCreateView.as_view(), name='categoria_create'),
    path('categoria/<int:pk>/editar/', views.CategoriaUpdateView.as_view(), name='categoria_update'),
    path('categoria/<int:pk>/excluir/', views.CategoriaDeleteView.as_view(), name='categoria_delete'),
    path('resumo/', views.ResumoView.as_view(), name='resumo'),
    path('logout/', LogoutView.as_view(next_page='login', template_name='login.html'), name='logout'),
    path('salvar-saldos-faturas/', views.salvar_saldos_faturas, name='salvar_saldos_faturas'),
]


