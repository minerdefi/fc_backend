from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', views.get_user_profile, name='profile'),
    path('verify-email/', views.verify_email, name='verify-email'),
    path('withdrawals/', views.get_withdrawals, name='withdrawals'),
    path('withdrawals/create/', views.create_withdrawal, name='create-withdrawal'),
    path('earnings-history/', views.get_earnings_history, name='earnings-history'),
    path('recent-activity/', views.get_recent_activity, name='recent-activity'),
    path('transactions/', views.get_all_transactions, name='all-transactions'),
    path('wallets/', views.get_active_wallets, name='active-wallets'),
    path('deposits/create/', views.create_deposit, name='create-deposit'),
    path('transaction-pin/request-otp/', views.request_pin_otp, name='request-pin-otp'),
    path('transaction-pin/set/', views.set_transaction_pin, name='set-transaction-pin'),
    path('profile/update/', views.update_profile, name='update-profile'),
    path('change-password/', views.change_password, name='change-password'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('reset-password/', views.reset_password, name='reset-password'),
]
