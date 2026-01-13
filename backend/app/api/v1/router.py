"""API v1 router aggregating all endpoint modules."""

from fastapi import APIRouter

router = APIRouter()

# Endpoint modules will be included here as they are implemented
# Example:
# from app.api.v1.endpoints import auth, assessments, suppliers
# router.include_router(auth.router, prefix="/auth", tags=["auth"])
# router.include_router(assessments.router, prefix="/assessments", tags=["assessments"])
# router.include_router(suppliers.router, prefix="/suppliers", tags=["suppliers"])
