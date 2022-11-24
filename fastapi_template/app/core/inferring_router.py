from typing import TYPE_CHECKING, Any, Callable, get_type_hints

from fastapi import APIRouter
from pydantic import BaseModel


class InferringRouter(APIRouter):
    """
    Overrides the route decorator logic to use the annotated return type as the `response_model` if unspecified.
    """

    if not TYPE_CHECKING:  # pragma: no branch

        def add_api_route(self, path: str, endpoint: Callable[..., Any], **kwargs: Any) -> None:
            if not (kwargs.get("response_model") or kwargs.get("response_class")):
                return_cls = get_type_hints(endpoint).get("return")
                if isinstance(return_cls, BaseModel):
                    kwargs["response_model"] = return_cls
                else:
                    kwargs["response_class"] = return_cls
            return super().add_api_route(path, endpoint, **kwargs)
