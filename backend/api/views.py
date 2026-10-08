from typing import Any, cast
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import RouteRequestSerializer, RouteResponseSerializer
from .services.route import build_route  # pyright: ignore[reportAttributeAccessIssue]


# @api_view(["GET"])
# def hello(request):
#     return Response({"message": "Hello there o from Django"})

@api_view (["POST"])
def create_route(request):
    serializer = RouteRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = cast(dict[str, Any], serializer.validated_data)
    route = build_route(data["locations"], data["start"])
    response_serializer = RouteResponseSerializer(data=route)
    response_serializer.is_valid(raise_exception=True)
    return Response(response_serializer.data)