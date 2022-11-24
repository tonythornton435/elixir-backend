import os
from datetime import timedelta

import jwt
from django.utils import timezone
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET

from .models import User
from registry.models import HealthWorker
from common.views import create
from common.payload import (
    ErrorCode,
    create_success_payload,
    create_error_payload,
)
from common.validation import validate_post_data


@csrf_exempt
@require_POST
def register_user(request):
    return create(request, User)


@csrf_exempt
@require_POST
def login(request):
    is_valid, request_data, debug_data = validate_post_data(
        request.body, ["email", "password"]
    )
    if not is_valid:
        return create_error_payload(
            debug_data["data"], message=debug_data["message"]
        )  # pragma: no cover

    user = authenticate(email=request_data["email"], password=request_data["password"])
    if user is not None:
        now = timezone.now()
        roles = ["PATIENT"]
        # check if user is a healthworker
        if HealthWorker.objects.filter(user=user).exists():
            roles.append("HEALTH_WORKER")

        claims = {
            "sub": str(user.uuid),
            "iat": now.timestamp(),
            "exp": (
                now + timedelta(seconds=31556926)  # one solar year lol
            ).timestamp(),
            "roles": " ".join(roles),
        }
        token = jwt.encode(claims, os.environ["JWT_PRIVATE_KEY"], algorithm="RS384")
        return create_success_payload(
            {
                "token": token,
                "algorithm": "RS384",
                "public_key": os.environ["JWT_PUBLIC_KEY"],
            },
            message="Login successful.",
        )
    else:
        return create_error_payload({"message": ErrorCode.LOGIN_FAILED})


@require_GET
def public_key(request):
    return create_success_payload(
        {"algorithm": "RS384", "public_key": os.environ["JWT_PUBLIC_KEY"]}
    )


# @csrf_exempt
# @require_POST
# def reset_password(request):
#     pass


# @csrf_exempt
# @require_POST
# def change_password(request):
#     pass
