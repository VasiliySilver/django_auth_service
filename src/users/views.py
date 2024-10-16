from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserRegistrationSerializer,
    OTPVerificationSerializer,
)
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
            user.otp = "1234"  # TODO: Remove this after testing
            user.save()
            logger.info(
                f"User registered with phone number: {user.phone_number}, OTP set to: {user.otp}"
            )
            return Response(
                {"message": "User registered successfully. Use OTP '1234' to verify."},
                status=status.HTTP_201_CREATED,
            )
        logger.error(f"Registration failed. Errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OTPVerificationView(APIView):
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data["phone_number"]
            _otp = serializer.validated_data["otp"]
            try:
                user = User.objects.get(phone_number=phone_number)
                # TODO: Temporarily accept any OTP
                # Uncomment the following lines to enable OTP verification
                # if user.otp != _otp:
                #     return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
                user.is_active = True
                user.save()
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                    status=status.HTTP_200_OK,
                )
            except User.DoesNotExist:
                return Response(
                    {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )
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
            token = request.data.get("token")
            if not token:
                return Response(
                    {"detail": "No token provided"}, status=status.HTTP_400_BAD_REQUEST
                )

            access_token = AccessToken(token)
            user_id = access_token.payload.get("user_id")
            print(
                f"Token payload: {access_token.payload}"
            )  # Add this line for debugging
            if not user_id:
                return Response(
                    {"detail": "Invalid token payload"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = User.objects.get(id=user_id)
            print(f"User active status: {user.is_active}")
            if not user.is_active:
                return Response(
                    {"detail": "User account is disabled."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            return Response({"detail": "Token is valid."})
        except Exception as e:
            print(f"Error in token verification: {str(e)}")
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "This is a protected resource."})
