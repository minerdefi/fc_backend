from django.contrib import admin
from .models import Profile, ADATransaction, TaxTransaction, EarningsTransaction, Deposit, Withdrawal, TransactionHistory, WalletAddress

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone_number')
    list_filter = ('created_at',)

@admin.register(ADATransaction)
class ADATransactionAdmin(admin.ModelAdmin):
    list_display = ('profile', 'amount', 'transaction_type', 'description', 'created_at')
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('profile__user__username', 'description')

@admin.register(TaxTransaction)
class TaxTransactionAdmin(admin.ModelAdmin):
    list_display = ('profile', 'amount', 'transaction_type', 'description', 'created_at')
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('profile__user__username', 'description')

@admin.register(EarningsTransaction)
class EarningsTransactionAdmin(admin.ModelAdmin):
    list_display = ('profile', 'amount', 'transaction_type', 'source', 'description', 'created_at')
    list_filter = ('transaction_type', 'source', 'created_at')
    search_fields = ('profile__user__username', 'description')

@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'payment_type', 'deposit_type', 'status', 'created_at')
    list_filter = ('payment_type', 'deposit_type', 'status', 'created_at')
    search_fields = ('user__username', 'user__email', 'transaction_id')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('user__username', 'user__email', 'wallet_address', 'transaction_id')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['mark_as_completed', 'mark_as_rejected']

    def mark_as_completed(self, request, queryset):
        for withdrawal in queryset:
            withdrawal.status = 'completed'
            withdrawal.save()  # This will trigger the save method that updates transaction history
    mark_as_completed.short_description = "Mark selected withdrawals as completed"

    def mark_as_rejected(self, request, queryset):
        queryset.update(status='rejected')
    mark_as_rejected.short_description = "Mark selected withdrawals as rejected"

@admin.register(TransactionHistory)
class TransactionHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_type', 'amount', 'status', 'created_at')
    list_filter = ('transaction_type', 'status', 'created_at')
    search_fields = ('user__username', 'user__email', 'description', 'reference_id')
    readonly_fields = ('created_at', 'updated_at', 'previous_balance', 'new_balance')
    ordering = ('-created_at',)

@admin.register(WalletAddress)
class WalletAddressAdmin(admin.ModelAdmin):
    list_display = ('cryptocurrency', 'network', 'address', 'status', 'is_default')
    list_filter = ('cryptocurrency', 'network', 'status', 'is_default')
    search_fields = ('address', 'description')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['mark_as_active', 'mark_as_inactive', 'mark_as_maintenance']

    def mark_as_active(self, request, queryset):
        queryset.update(status='active')
    mark_as_active.short_description = "Mark selected addresses as active"

    def mark_as_inactive(self, request, queryset):
        queryset.update(status='inactive')
    mark_as_inactive.short_description = "Mark selected addresses as inactive"

    def mark_as_maintenance(self, request, queryset):
        queryset.update(status='maintenance')
    mark_as_maintenance.short_description = "Mark selected addresses as under maintenance"
