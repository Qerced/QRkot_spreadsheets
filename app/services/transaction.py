from datetime import datetime

from app.models.base import DonationCharityBase


def investment(
    target: DonationCharityBase,
    sources: list[DonationCharityBase]
) -> list[DonationCharityBase]:
    changed: list = []
    for source in sources:
        invested = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        for object in (target, source):
            object.invested_amount += invested
            if object.full_amount == object.invested_amount:
                object.close_date = datetime.now()
                object.fully_invested = True
        changed.append(source)
        if target.full_amount == target.invested_amount:
            break
    return changed
