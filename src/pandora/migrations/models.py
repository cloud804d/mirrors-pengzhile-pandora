# -*- coding: utf-8 -*-

from datetime import datetime as dt

from sqlalchemy import func, Column, Text, Integer
from sqlalchemy.orm import DeclarativeBase

from ..migrations.database import session


class Base(DeclarativeBase):
    pass


class ConversationOfficial(Base):
    __tablename__ = 'conversation_official'

    conversation_id = Column(Text, primary_key=True, autoincrement=False)
    title = Column(Text, nullable=False)
    create_time = Column(Integer, nullable=False)

    @staticmethod
    def get_list(offset, limit):
        total = session.query(func.count(ConversationOfficial.conversation_id)).scalar()
        return total, session.query(ConversationOfficial).order_by(ConversationOfficial.create_time.desc()).limit(
            limit).offset(offset).all()

    @staticmethod
    def get(conversation_id):
        return session.query(ConversationOfficial).get(conversation_id)

    def save(self):
        session.commit()
        return self

    def new(self):
        session.add(self)
        session.commit()

        return self

    @staticmethod
    def delete(conversation_id):
        session.query(ConversationOfficial).filter(ConversationOfficial.conversation_id == conversation_id).delete()
        session.commit()

    @staticmethod
    def clear():
        session.query(ConversationOfficial).delete()
        session.commit()

    @staticmethod
    def new_conversation(conversation_id, title=None):
        conv = ConversationOfficial.get(conversation_id)

        if not conv:
            conv = ConversationOfficial()
            conv.conversation_id = conversation_id
            conv.title = title or 'New chat'
            conv.create_time = dt.now().timestamp()
            conv.new()
        else:
            conv.title = title or 'New chat'
            conv.save()

    @staticmethod
    def wrap_conversation_list(offset, limit):
        total, items = ConversationOfficial.get_list(offset, limit)

        stripped = []
        for item in items:
            stripped.append({
                'id': item.conversation_id,
                'title': item.title,
                'create_time': dt.utcfromtimestamp(item.create_time).isoformat(),
            })

        return {'items': stripped, 'total': total, 'limit': limit, 'offset': offset}


class ConversationInfo(Base):
    __tablename__ = 'conversation_info'

    conversation_id = Column(Text, primary_key=True, autoincrement=False)
    title = Column(Text, nullable=False)
    create_time = Column(Integer, nullable=False)
    current_node = Column(Text, nullable=True)

    @staticmethod
    def get_list(offset, limit):
        total = session.query(func.count(ConversationInfo.conversation_id)).scalar()
        return total, session.query(ConversationInfo).order_by(ConversationInfo.create_time.desc()).limit(
            limit).offset(offset).all()

    @staticmethod
    def get(conversation_id):
        return session.query(ConversationInfo).get(conversation_id)

    def new(self):
        session.add(self)
        session.commit()

        return self

    @staticmethod
    def delete(conversation_id):
        session.query(ConversationInfo).filter(ConversationInfo.conversation_id == conversation_id).delete()
        session.commit()

    @staticmethod
    def clear():
        session.query(ConversationInfo).delete()
        session.commit()


class PromptInfo(Base):
    __tablename__ = 'prompt_info'

    prompt_id = Column(Text, primary_key=True, autoincrement=False)
    conversation_id = Column(Text, primary_key=True, autoincrement=False)
    model = Column(Text, nullable=True)
    parent_id = Column(Text, nullable=True)
    role = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    create_time = Column(Integer, nullable=False)

    @staticmethod
    def list_by_conversation_id(conversation_id):
        return session.query(PromptInfo).filter(PromptInfo.conversation_id == conversation_id).all()

    def new(self):
        session.add(self)
        session.commit()

        return self

    @staticmethod
    def clear():
        session.query(PromptInfo).delete()
        session.commit()
