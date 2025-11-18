from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ikon_auth import IKonJWTVerifier

verifier = IKonJWTVerifier()


@api_view(["GET"])
def public_view(request):
    return Response({"message": "Django DRF public OK"})


@api_view(["GET"])
def secure_view(request):
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return Response(
            {"error": "Missing or invalid Authorization header"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token = auth_header.split(" ", 1)[1]

    try:
        claims = verifier.verify(token)
        return Response(
            {"message": "Django DRF secure OK", "claims": claims},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
