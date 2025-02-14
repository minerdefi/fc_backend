from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    ProfileSerializer, 
    WithdrawalSerializer,
    EarningsHistorySerializer,
    RecentActivitySerializer,
    WalletAddressSerializer
)
import logging
from django.utils import timezone
from .models import (
    EmailVerification,
    Withdrawal,
    EarningsTransaction,
    TransactionHistory,
    WalletAddress,
    Deposit
)
from .utils import send_verification_email
from django.db.models import Q
from django.contrib.auth.models import User
from decimal import Decimal
from django.core.mail import send_mail
from django.conf import settings
import random
from django.contrib.auth.hashers import check_password
import jwt
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    try:
        serializer = UserRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create user
        user = serializer.save()
        
        # Create email verification token
        verification = EmailVerification.objects.create(user=user)
        
        # Send verification email
        send_verification_email(user, verification.token)

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'status': 'success',
            'message': 'Registration successful. Please check your email to verify your account.',
            'data': {
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                },
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        login = serializer.validated_data['login']
        password = serializer.validated_data['password']
        
        try:
            # First, find the user by either username or email
            user = User.objects.get(Q(username=login) | Q(email=login))
            # Then authenticate using the found username
            authenticated_user = authenticate(username=user.username, password=password)
            
            if authenticated_user:
                refresh = RefreshToken.for_user(authenticated_user)
                return Response({
                    'status': 'success',
                    'data': {
                        'user': {
                            'username': user.username,
                            'email': user.email,
                            'first_name': user.first_name,
                            'last_name': user.last_name
                        },
                        'tokens': {
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                        }
                    }
                })
            else:
                return Response({
                    'status': 'error',
                    'message': 'Invalid password'
                }, status=status.HTTP_401_UNAUTHORIZED)
                
        except User.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'No account found with this username or email'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
    return Response({
        'status': 'error',
        'message': 'Invalid credentials',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    try:
        print("Auth header:", request.headers.get('Authorization'))  # Debug log
        print("User:", request.user)  # Debug log
        
        profile = request.user.profile
        serializer = ProfileSerializer(profile)
        data = serializer.data
        print("Profile data:", data)  # Debug log
        
        return Response({
            'status': 'success',
            'data': data
        })
    except Exception as e:
        print("Profile error:", str(e))  # Debug log
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email(request):
    token = request.query_params.get('token')
    try:
        verification = EmailVerification.objects.get(token=token, is_verified=False)
        verification.is_verified = True
        verification.verified_at = timezone.now()
        verification.save()
        
        return Response({
            'status': 'success',
            'message': 'Email verified successfully'
        })
    except EmailVerification.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Invalid or expired verification token'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_withdrawal(request):
    try:
        # Check for PIN first
        if not request.user.profile.transaction_pin:
            return Response({
                'status': 'error',
                'message': 'Transaction PIN not set',
                'code': 'PIN_REQUIRED'
            }, status=400)

        # Validate transaction PIN
        transaction_pin = request.data.get('transaction_pin')
        if not transaction_pin:
            return Response({
                'status': 'error',
                'message': 'Transaction PIN is required'
            }, status=400)

        if transaction_pin != request.user.profile.transaction_pin:
            return Response({
                'status': 'error',
                'message': 'Invalid transaction PIN'
            }, status=400)

        # Continue with amount validation and withdrawal creation
        print("Creating withdrawal - Data:", request.data)  # Debug log
        try:
            # Convert amount to Decimal
            amount = Decimal(str(request.data.get('amount', '0')))
            
            # Basic validations...
            if amount < Decimal('100'):
                return Response({
                    'status': 'error',
                    'message': 'Minimum withdrawal amount is $100'
                }, status=400)

            if request.user.profile.avail_balance < amount:
                return Response({
                    'status': 'error',
                    'message': 'Insufficient available balance'
                }, status=400)

            # Create withdrawal request
            serializer = WithdrawalSerializer(
                data={
                    'amount': str(amount),
                    'payment_method': request.data.get('payment_method'),
                    'wallet_address': request.data.get('wallet_address'),
                },
                context={'request': request}
            )

            if not serializer.is_valid():
                return Response({
                    'status': 'error',
                    'message': 'Invalid data',
                    'errors': serializer.errors
                }, status=400)

            withdrawal = serializer.save(user=request.user)
            
            # Return success response with details
            return Response({
                'status': 'success',
                'message': 'Withdrawal request submitted successfully',
                'data': {
                    'withdrawal': {
                        'id': withdrawal.id,
                        'amount': str(withdrawal.amount),
                        'payment_method': withdrawal.payment_method,
                        'status': withdrawal.status,
                    },
                    'profile': {
                        'avail_balance': str(request.user.profile.avail_balance)
                    }
                }
            }, status=201)  # Using 201 Created for successful creation

        except Exception as e:
            print("Error in create_withdrawal:", str(e))  # Debug log
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=400)

    except Exception as e:
        print("Error in create_withdrawal:", str(e))  # Debug log
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_withdrawals(request):
    withdrawals = Withdrawal.objects.filter(user=request.user)
    serializer = WithdrawalSerializer(withdrawals, many=True)
    return Response({
        'status': 'success',
        'data': serializer.data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_earnings_history(request):
    try:
        earnings = EarningsTransaction.objects.filter(
            profile=request.user.profile,
            transaction_type='credit'
        ).order_by('created_at')
        
        serializer = EarningsHistorySerializer(earnings, many=True)
        
        return Response({
            'status': 'success',
            'data': serializer.data
        })
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recent_activity(request):
    try:
        activities = TransactionHistory.objects.filter(
            user=request.user
        ).order_by('-created_at')[:5]  # Get last 5 transactions
        
        serializer = RecentActivitySerializer(activities, many=True)
        
        return Response({
            'status': 'success',
            'data': serializer.data
        })
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_transactions(request):
    try:
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        
        transactions = TransactionHistory.objects.filter(
            user=request.user
        ).order_by('-created_at')
        
        # Calculate pagination
        start = (page - 1) * page_size
        end = start + page_size
        
        serializer = RecentActivitySerializer(transactions[start:end], many=True)
        total_count = transactions.count()
        
        return Response({
            'status': 'success',
            'data': {
                'transactions': serializer.data,
                'total': total_count,
                'page': page,
                'total_pages': (total_count + page_size - 1) // page_size
            }
        })
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_active_wallets(request):
    try:
        # Debug logs
        print("Request user:", request.user)
        print("Auth header:", request.headers.get('Authorization'))

        # Get active wallets and ensure they exist
        wallets = WalletAddress.objects.filter(status='active')
        if not wallets.exists():
            print("No active wallets found")
            return Response({
                'status': 'success',
                'data': []
            })

        # Serialize the wallets
        serializer = WalletAddressSerializer(wallets, many=True)
        print("Serialized wallets:", serializer.data)

        return Response({
            'status': 'success',
            'data': serializer.data
        })
    except WalletAddress.DoesNotExist:
        print("WalletAddress model does not exist")
        return Response({
            'status': 'error',
            'message': 'Wallet system not configured'
        }, status=500)
    except Exception as e:
        print("Error in get_active_wallets:", str(e))
        return Response({
            'status': 'error',
            'message': 'Internal server error'
        }, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_deposit(request):
    try:
        amount = request.data.get('amount')
        payment_type = request.data.get('payment_type')
        proof_file = request.FILES.get('proof_of_payment')

        if not amount or not payment_type:
            return Response({
                'status': 'error',
                'message': 'Amount and payment type are required'
            }, status=400)

        # Validate amount
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be greater than 0")
        except ValueError as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=400)

        # Create deposit record
        deposit = Deposit.objects.create(
            user=request.user,
            amount=amount,
            payment_type=payment_type,
            status='pending',
            proof_of_payment=proof_file
        )

        return Response({
            'status': 'success',
            'message': 'Deposit request submitted successfully',
            'data': {
                'id': deposit.id,
                'amount': str(deposit.amount),
                'status': deposit.status
            }
        })
    except Exception as e:
        print(f"Error creating deposit: {str(e)}")
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_pin_otp(request):
    try:
        # Generate OTP
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        user = request.user

        # Store OTP in user's profile (you might want to add an OTP field to Profile model)
        user.profile.pin_otp = otp
        user.profile.pin_otp_created = timezone.now()
        user.profile.save()

        # Send OTP via email
        send_mail(
            'Transaction PIN Setup - OTP Verification',
            f'Your OTP for setting up transaction PIN is: {otp}\nThis code will expire in 10 minutes.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return Response({
            'status': 'success',
            'message': 'OTP has been sent to your email'
        })
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_transaction_pin(request):
    try:
        otp = request.data.get('otp')
        pin = request.data.get('pin')
        confirm_pin = request.data.get('confirm_pin')

        if not otp or not pin or not confirm_pin:
            return Response({
                'status': 'error',
                'message': 'OTP and PIN are required'
            }, status=400)

        if pin != confirm_pin:
            return Response({
                'status': 'error',
                'message': 'PINs do not match'
            }, status=400)

        if len(pin) != 6:
            return Response({
                'status': 'error',
                'message': 'PIN must be 6 digits'
            }, status=400)

        user = request.user
        # Verify OTP
        if not user.profile.pin_otp or user.profile.pin_otp != otp:
            return Response({
                'status': 'error',
                'message': 'Invalid OTP'
            }, status=400)

        # Check OTP expiry (10 minutes)
        otp_age = timezone.now() - user.profile.pin_otp_created
        if otp_age.total_seconds() > 600:
            return Response({
                'status': 'error',
                'message': 'OTP has expired'
            }, status=400)

        # Set the PIN
        user.profile.transaction_pin = pin
        user.profile.pin_otp = None  # Clear OTP
        user.profile.pin_otp_created = None
        user.profile.save()

        return Response({
            'status': 'success',
            'message': 'Transaction PIN set successfully'
        })
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    try:
        user = request.user
        profile = user.profile

        # Update user fields
        if 'first_name' in request.data:
            user.first_name = request.data['first_name']
        if 'last_name' in request.data:
            user.last_name = request.data['last_name']
        
        # Update profile fields
        if 'phone_number' in request.data:
            profile.phone_number = request.data['phone_number']

        user.save()
        profile.save()

        # Return updated profile data
        serializer = ProfileSerializer(profile)
        return Response({
            'status': 'success',
            'message': 'Profile updated successfully',
            'data': serializer.data
        })

    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    try:
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        if not current_password or not new_password:
            return Response({
                'status': 'error',
                'message': 'Both current and new password are required'
            }, status=400)

        # Verify current password
        if not user.check_password(current_password):  # Changed to use check_password method
            return Response({
                'status': 'error',
                'message': 'Current password is incorrect'
            }, status=400)

        # Validate new password
        if len(new_password) < 8:
            return Response({
                'status': 'error',
                'message': 'Password must be at least 8 characters long'
            }, status=400)

        # Update password
        user.set_password(new_password)
        user.save()

        # Generate new tokens since password changed
        refresh = RefreshToken.for_user(user)

        return Response({
            'status': 'success',
            'message': 'Password changed successfully. Please login with your new password.',
            'data': {
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }
        })

    except Exception as e:
        print("Password change error:", str(e))  # Add logging
        return Response({
            'status': 'error',
            'message': 'Failed to change password. Please try again.'
        }, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    try:
        email = request.data.get('email')
        
        if not email:
            return Response({
                'status': 'error',
                'message': 'Email is required'
            }, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Don't reveal if email exists
            return Response({
                'status': 'success',
                'message': 'If an account exists with this email, you will receive reset instructions.'
            })

        # Generate reset token
        reset_token = jwt.encode({
            'user_id': user.id,
            'exp': int((timezone.now() + timedelta(hours=1)).timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')

        # Create reset URL
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"

        # Send simple email
        send_mail(
            'Reset Your Password - Forbes Capital',
            f'Click here to reset your password: {reset_url}\n\nThis link will expire in 1 hour.',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return Response({
            'status': 'success',
            'message': 'Password reset instructions have been sent to your email.'
        })

    except Exception as e:
        print(f"Password reset error: {str(e)}")
        return Response({
            'status': 'error',
            'message': 'Failed to send reset instructions.'
        }, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    try:
        token = request.data.get('token')
        new_password = request.data.get('password')

        if not token or not new_password:
            return Response({
                'status': 'error',
                'message': 'Token and new password are required'
            }, status=400)

        try:
            # Verify and decode token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            
            # Get user
            user = User.objects.get(id=user_id)

            # Update password without checking profile token
            user.set_password(new_password)
            user.save()

            # Generate new login tokens
            refresh = RefreshToken.for_user(user)

            return Response({
                'status': 'success',
                'message': 'Password has been reset successfully',
                'data': {
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }
            })

        except jwt.ExpiredSignatureError:
            return Response({
                'status': 'error',
                'message': 'Reset link has expired. Please request a new one.'
            }, status=400)
        except jwt.InvalidTokenError:
            return Response({
                'status': 'error',
                'message': 'Invalid reset link. Please request a new one.'
            }, status=400)
        except User.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'User not found'
            }, status=400)

    except Exception as e:
        print(f"Password reset error: {str(e)}")  # Debug log
        return Response({
            'status': 'error',
            'message': 'Failed to reset password. Please try again.'
        }, status=400)
