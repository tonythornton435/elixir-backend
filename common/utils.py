"""This module houses common miscellaneous utils."""

import json
from math import sqrt

from django.contrib.postgres.search import SearchVector

from common.payload import create_error_payload, create_success_payload, ErrorCode


def validate_post_data(request, required_fields):
    """Validate POST fields against a list of required fields."""
    try:
        request_data = json.loads(request.body)
        if "user_id" in required_fields:
            request_data["user_id"] = request.token["sub"]
    except json.JSONDecodeError:
        return False, {}, {"data": {}, "message": "Please provide valid JSON."}

    missing_fields = {}
    for field in required_fields:
        if field not in request_data:
            missing_fields[field] = ErrorCode.FIELD_REQUIRED

    return (
        len(missing_fields) == 0,
        request_data,
        {"data": missing_fields, "message": ""},
    )


def create(model, request):
    """Validate POST data and save it to the table."""
    is_valid, request_data, debug_data = validate_post_data(
        request, model.POST_REQUIRED_FIELDS
    )
    if not is_valid:
        return create_error_payload(debug_data["data"], message=debug_data["message"])

    success, result = model.create(request_data)
    if success:
        return create_success_payload(
            result.serialize(), message="Created successfully."
        )
    else:
        return create_error_payload(message=result)


def search_table(model, search_fields, request):
    """Validate POST query and search the *search_fields columns."""
    is_valid, request_data, debug_data = validate_post_data(request, ["query"])
    if not is_valid:
        return create_error_payload(debug_data["data"], message=debug_data["message"])

    results = model.objects.annotate(search=SearchVector(*search_fields)).filter(
        search=request_data["query"]
    )
    return create_success_payload([result.serialize() for result in results])


def error404(request, exception):
    """Return an error 404 HTTP payload."""
    return create_error_payload({}, ErrorCode.DOES_NOT_EXIST, status=404)


def parameterized(dec):
    """
    Create parameterized decorators.

    https://stackoverflow.com/a/26151604/12938797
    """

    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)

        return repl

    return layer


def ci_lower_bound(n_positive, n):
    """
    Find the Wilson Score Interval for n_positive/n ratings.

    https://www.evanmiller.org/how-not-to-sort-by-average-rating.html
    https://stackoverflow.com/a/10029645
    """
    if n == 0:
        return 0
    z = 1.96  # 95% confidence level
    phat = 1.0 * n_positive / n
    return (
        phat + z * z / (2 * n) - z * sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)
    ) / (1 + z * z / n)
