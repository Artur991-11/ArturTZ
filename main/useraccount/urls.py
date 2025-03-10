from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
app_name = 'useraccount'

urlpatterns = [
    path('edit_profile/', views.EditMyProfileView.as_view(), name='edit_profile'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('notification/', views.NotificationView.as_view(), name='notification'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('tickets/', views.TicketsView.as_view(), name='tickets'),
    path('tickets/<slug:pk>/delete/', views.TicketDeleteView.as_view(), name='ticket_delete'),
    path('tickets/<uuid:ticket_id>/add_comment/', views.TicketCommentCreateView.as_view(), name='add_comment'),
    path('tickets/<slug:pk>/', views.TicketMessageView.as_view(), name='ticket_message'),
    # Чат
    path('chats/', views.ChatsListView.as_view(), name='chats_list'),
    path('chats/<uuid:pk>/', views.ChatsDetailView.as_view(), name='chats'),
    path('chats/<uuid:chat_id>/add_mesage/', views.ChatsMessageCreateView.as_view(), name='add_mesage'),
    path('chats/<uuid:pk>/delete/', views.ChatDeleteView.as_view(), name='chat_delete'),
    path('chats/create/', views.ChatGroupCreateView.as_view(), name='chat_create'),
    path('chats/<uuid:pk>/update/', views.ChatUpdateView.as_view(), name='chat_edit'),
    path('create-chat/<uuid:user_id>/', views.CreateChatView.as_view(), name='create_chat'),

]