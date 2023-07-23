from datetime import datetime
from apps.database import db
from sqlalchemy.orm import relationship

class UserModel(db.Model):
    __tablename__ = 'user_info'

    id = db.Column(db.Integer, primary_key=True)
    third_uid = db.Column(db.String, nullable=False)
    third_party = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    created_at = db.Column(db.TIMESTAMP(True), nullable=False, default=db.text('CURRENT_TIMESTAMP'))

    # faqs = relationship('FaqModel', primaryjoin=id == FaqModel.faq_list_id)
    # bot = relationship(
    #     'BotModel',
    #     back_populates='faq_lists',
    #     foreign_keys=[bot_id])
    # start_faq = relationship('FaqModel',
    #                          primaryjoin=start_faq_id == FaqModel.id)
    # not_found_faq = relationship('FaqModel',
    #                              primaryjoin=not_found_faq_id == FaqModel.id)

    def __init__(self, third_uid: str, third_party: str, email: str):
        self.third_uid = third_uid
        self.third_party = third_party
        self.email = email
