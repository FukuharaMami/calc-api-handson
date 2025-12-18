import azure.functions as func

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


def _error(reason: str) -> func.HttpResponse:
    return func.HttpResponse(
        body=f"ERROR: {reason}",
        status_code=200,
        mimetype="text/plain",
        charset="utf-8",
    )


def _get_required_int_query(req: func.HttpRequest, name: str):
    value = req.params.get(name)
    if value is None:
        return None, _error(f"Missing query parameter {name}")

    try:
        return int(value), None
    except (TypeError, ValueError):
        return None, _error(f"Query parameter {name} must be an integer")


def _trunc_div(a: int, b: int) -> int:
    # truncation toward zero
    sign = -1 if (a < 0) ^ (b < 0) else 1
    return sign * (abs(a) // abs(b))


@app.route(route="multiply", methods=["GET"])
def multiply(req: func.HttpRequest) -> func.HttpResponse:
    a, err = _get_required_int_query(req, "A")
    if err is not None:
        return err

    b, err = _get_required_int_query(req, "B")
    if err is not None:
        return err

    return func.HttpResponse(
        body=str(a * b),
        status_code=200,
        mimetype="text/plain",
        charset="utf-8",
    )


@app.route(route="divide", methods=["GET"])
def divide(req: func.HttpRequest) -> func.HttpResponse:
    a, err = _get_required_int_query(req, "A")
    if err is not None:
        return err

    b, err = _get_required_int_query(req, "B")
    if err is not None:
        return err

    if b == 0:
        return _error("Division by zero")

    return func.HttpResponse(
        body=str(_trunc_div(a, b)),
        status_code=200,
        mimetype="text/plain",
        charset="utf-8",
    )
