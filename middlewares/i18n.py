from pathlib import Path
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from config import *
from main import dp

BASE_DIR = Path(__file__).parent.parent
LOCALES_DIR = BASE_DIR / 'locales'

i18n = I18nMiddleware(domain=DATABASE_FSM_NAME,
                      path=LOCALES_DIR)

dp.middleware.setup(i18n)

_ = i18n.lazy_gettext

