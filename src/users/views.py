from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import CustomTokenObtainPairSerializer, UserRegistrationSerializer, OTPVerificationSerializer
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import get_user_model
import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

User = get_user_model()

logger = logging.getLogger(__name__)

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_active=False)
            user.otp = "1234" # TODO: Заглушка: всегда проверяем OTP "1234"
            user.save()
            logger.info(f"User registered with phone number: {user.phone_number}, OTP set to: {user.otp}")
            return Response({"message": "User registered successfully. Use OTP '1234' to verify."}, status=status.HTTP_201_CREATED)
        logger.error(f"Registration failed. Errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OTPVerificationView(APIView):
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            otp = serializer.validated_data['otp']
            try:
                user = User.objects.get(phone_number=phone_number)
                # TODO:Заглушка: всегда проверяем OTP "1234"
                if otp == "1234":
                    # Не меняем статус пользователя и не очищаем OTP
                    # user.is_active = True
                    # user.otp = None
                    # user.save()
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.user
        if not user.is_active:
            return Response({"detail": "User account is disabled."}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"detail": "Token is valid."})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "This is a protected resource."})
