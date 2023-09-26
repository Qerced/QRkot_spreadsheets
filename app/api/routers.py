from fastapi import APIRouter

from app.api.endpoints import (
    charity_router, donation_router, google_router, user_router
)

PREFIX_CHARITY_PROJECT = '/charity_project'
TAGS_CHARITY_PROJECT = 'Charity project'
PREFIX_DONATION = '/donation'
TAGS_DONATION = 'Donation'
PREFIX_GOOGLE_API = '/google'
TAGS_GOOGLE_API = 'Google'

main_router = APIRouter()
main_router.include_router(
    charity_router, prefix=PREFIX_CHARITY_PROJECT, tags=[TAGS_CHARITY_PROJECT]
)
main_router.include_router(
    donation_router, prefix=PREFIX_DONATION, tags=[TAGS_DONATION]
)
main_router.include_router(
    google_router, prefix=PREFIX_GOOGLE_API, tags=[TAGS_GOOGLE_API]
)
main_router.include_router(user_router)
