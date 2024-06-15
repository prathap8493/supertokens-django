
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('userinfo',views.getUserDetailsAPI.as_view(),name='user-details'),
    path('saveText',views.SaveUserTextAPI.as_view(),name='save'),
    path('PostText',views.TextModifier.as_view(),name='laksjd'),
    path('rephrase',views.RephraseTextView.as_view(),name=';alskdl'),
    path('grammerCheck',views.GrammarCheckView.as_view(),name='grammer-checker'),
    path('validate',views.ValidateTextView.as_view(),name="validate")
]