from rest_framework.response import Response


def error(message, status_code):
    # common shape for hand-written errors: {"error": "..."}
    return Response({"error": message}, status=status_code)
