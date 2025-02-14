from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Withdrawal, Deposit, EarningsTransaction, TransactionHistory, WalletAddress
from django.db.models import Sum

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords don't match"})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    login = serializers.CharField(label='Username or Email')  # Changed from username to login
    password = serializers.CharField(write_only=True)

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    total_withdrawals = serializers.SerializerMethodField()
    total_deposits = serializers.SerializerMethodField()

    def get_total_withdrawals(self, obj):
        try:
            total = obj.user.withdrawal_set.filter(status='completed').aggregate(total=Sum('amount'))['total']
            return f"{float(total or 0):.2f}"
        except Exception as e:
            print(f"Error calculating withdrawals: {e}")
            return "0.00"

    def get_total_deposits(self, obj):
        try:
            total = obj.user.deposit_set.filter(status='completed').aggregate(total=Sum('amount'))['total']
            return f"{float(total or 0):.2f}"
        except Exception as e:
            print(f"Error calculating deposits: {e}")
            return "0.00"

    def format_amount(self, amount):
        try:
            return f"{float(amount):.2f}" if amount is not None else "0.00"
        except (TypeError, ValueError):
            return "0.00"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Format all decimal fields consistently
        decimal_fields = ['balance', 'earnings', 'ADA', 'avail_balance', 'Tax_balance']
        for field in decimal_fields:
            data[field] = self.format_amount(data[field])
        return data

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        
        # Update user fields
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()
        
        # Update profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance

    class Meta:
        model = Profile
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 
                 'balance', 'earnings', 'ADA', 'avail_balance', 'Tax_balance', 
                 'deposit', 'total_deposits', 'total_withdrawals', 'created_at',
                 'transaction_pin']  # Add this field
        read_only_fields = ['balance', 'earnings', 'ADA', 'avail_balance', 
                           'Tax_balance', 'deposit', 'total_deposits', 'total_withdrawals', 'created_at']

class WithdrawalSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Withdrawal
        fields = ['id', 'username', 'amount', 'payment_method', 
                 'wallet_address', 'status', 'created_at', 'transaction_id']
        read_only_fields = ['id', 'status', 'transaction_id', 'created_at']

    def validate(self, data):
        # Get user from context if available, otherwise skip balance check
        if 'request' in self.context:
            user = self.context['request'].user
            amount = data['amount']

            if amount <= 0:
                raise serializers.ValidationError("Amount must be greater than 0")

            # Check minimum withdrawal amount
            if amount < 100:
                raise serializers.ValidationError("Minimum withdrawal amount is $100")

            # Check available balance
            if user.profile.avail_balance < amount:
                raise serializers.ValidationError("Insufficient available balance")

        return data

class EarningsHistorySerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(source='created_at', format="%d %b")
    value = serializers.DecimalField(source='amount', max_digits=15, decimal_places=2)

    class Meta:
        model = EarningsTransaction
        fields = ['date', 'value']

class RecentActivitySerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(source='created_at', format="%d %b, %H:%M")
    amount = serializers.SerializerMethodField()

    def get_amount(self, obj):
        try:
            return f"${float(obj.amount):.2f}"
        except:
            return "$0.00"

    class Meta:
        model = TransactionHistory
        fields = ['transaction_type', 'amount', 'description', 'status', 'time']

class WalletAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletAddress
        fields = [
            'cryptocurrency',
            'network',
            'address',
            'qr_code',
            'status',
            'memo',
            'description'
        ]
