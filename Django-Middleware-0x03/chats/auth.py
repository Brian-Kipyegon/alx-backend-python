from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication class if needed for future extensions.
    Currently inherits all behavior from JWTAuthentication.
    """

    pass
