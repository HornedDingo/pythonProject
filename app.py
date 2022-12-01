async def on_startup(dpp):

    import filters
    filters.setup(dpp)

    from utils.notify_admins import on_startup_notifying
    await on_startup_notifying(dpp)

    from utils.set_bot_commands import set_default_commands
    await set_default_commands(dpp)

    print('Бот запущен')

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
