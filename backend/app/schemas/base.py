"""Base Pydantic schemas for API response envelopes."""

from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class Meta(BaseModel):
    """Metadata for API responses."""

    request_id: str | None = Field(
        default=None,
        description="Unique request identifier for correlation",
    )
    total: int | None = Field(
        default=None,
        description="Total count of items (for paginated responses)",
    )
    limit: int | None = Field(
        default=None,
        description="Maximum items per page",
    )
    offset: int | None = Field(
        default=None,
        description="Number of items skipped",
    )


class SuccessResponse(BaseModel, Generic[T]):
    """Standard success response envelope.

    Usage:
        # Single resource
        SuccessResponse[UserSchema](data=user, meta=Meta(request_id="..."))

        # List of resources
        SuccessResponse[list[UserSchema]](
            data=users,
            meta=Meta(request_id="...", total=100, limit=20, offset=0)
        )
    """

    data: T = Field(..., description="Response payload")
    meta: Meta = Field(default_factory=Meta, description="Response metadata")


class ErrorDetail(BaseModel):
    """Details about a specific error."""

    field: str | None = Field(
        default=None,
        description="Field that caused the error (for validation errors)",
    )
    message: str = Field(..., description="Error message")
    code: str | None = Field(
        default=None,
        description="Error code for programmatic handling",
    )


class ErrorBody(BaseModel):
    """Error information container."""

    code: str = Field(..., description="Error code (e.g., VALIDATION_ERROR, NOT_FOUND)")
    message: str = Field(..., description="Human-readable error message")
    details: list[ErrorDetail] = Field(
        default_factory=list,
        description="Additional error details",
    )


class ErrorResponse(BaseModel):
    """Standard error response envelope.

    Usage:
        ErrorResponse(
            error=ErrorBody(
                code="NOT_FOUND",
                message="User not found",
                details=[]
            )
        )
    """

    error: ErrorBody = Field(..., description="Error information")


# Common response types for convenience
class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(default="ok", description="Service health status")


class PaginationParams(BaseModel):
    """Pagination query parameters."""

    limit: int = Field(default=20, ge=1, le=100, description="Items per page")
    offset: int = Field(default=0, ge=0, description="Items to skip")
