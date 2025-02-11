import time
from contextlib import contextmanager

from django.db.backends.postgresql.base import DatabaseWrapper
from django.db.backends.utils import CursorWrapper
from django.utils.encoding import force_str
import logging

from core.middleware import thread_locals 

logger = logging.getLogger(__name__)


@contextmanager
def calc_sql_time(sql): # сам запрос в аргументе sql
    timestamp = time.monotonic() # измерение времени запроса в БД

    yield # чтобы следующий код выполнился только после заврешения блока with
    
    if hasattr(thread_locals, 'sql_count'):
        thread_locals.sql_count += 1
        thread_locals.sql_total += time.monotonic() - timestamp

    logger.info(
        f'Продолжительность SQL-запроса {sql} - '
        f'{time.monotonic() - timestamp:.3f} сек.'
    )


def make_safe(s):
   return s.replace('*', '').replace('\\', '').replace('%', '')


class CursorWrapper(CursorWrapper): # переопределяем метод execute
   def execute(self, sql, params=None):
       path = getattr(thread_locals, 'path', '')
       if path:
           path = make_safe(path)
           sql = f'/* {path} */\n{force_str(sql)}\n/* {path} */'

       with calc_sql_time(sql): # измерение времени запроса
           return super().execute(sql, params)


class DatabaseWrapper(DatabaseWrapper):
   def create_cursor(self, name=None):
       cursor = super().create_cursor(name)
       return CursorWrapper(cursor, self)