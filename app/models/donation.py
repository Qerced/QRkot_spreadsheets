from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import DonationCharityBase


class Donation(DonationCharityBase):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
