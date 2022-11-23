from aiogram import dispatcher
from .private_chat import IsPrivate

def setup(dp: dispatcher):
    dp.filters_factory.bind(IsPrivate)