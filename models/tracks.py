import datetime
import sqlalchemy
from . import db_session
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Track(SqlAlchemyBase):
    __tablename__ = 'tracks'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    path = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now,
                                     nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("users.id"))

    user = orm.relation('User')


def add_track(title, path, user_id):	# Добавление музыки в таблицу
    track = Track()
    track.title = title
    track.path = path
    track.user_id = user_id
    session = db_session.create_session()
    session.add(track)
    session.commit()

def count_tracks():
    session = db_session.create_session()
    return session.query(Track).count()

def get_track(id):
    session = db_session.create_session()
    return session.query(Track).get(id)

def del_id_track(id, filter=None, filt_incl=False):	# Удаление музыки из таблицы
    session = db_session.create_session()

    if filter != None:		# В случае если задается филтр

    # Обьяснение для filter:
    # Фильтр задается когда нужно удалить более 1 элемента
    # В случае если фильтр является числом типа int: то удаляется срез ID элементов,
    # Которых находится между параметром id и filter
    # Так-же filter можно задать, как знак равенства, тогда в зависимости
    # От знака, будет выбран опреденный срез начинающийся или заканчивающийся на id
    # Атрибут filt_incl нужен, в случиях, когда filter является числом,
    # Тогда в значение True, срез будет выбран включительно с id и самим filter'ом.

        if type(filter) == int:		# Срез между filter и id
            if filter > id:		# Срез id --- filter
                if filt_incl:	# Включительно
                    session.query(Track).filter(Track.id >= id, Track.id <= filter).delete()
                    session.commit()

                else:	# Не включая
                    session.query(Track).filter(Track.id > id, Track.id < filter).delete()
                    session.commit()

            elif filter < id:	# Срез filter --- id
                if filt_incl:	# Включительно
                    session.query(Track).filter(Track.id <= id, Track.id >= filter).delete()
                    session.commit()

                else:	# Не включая
                    session.query(Track).filter(Track.id < id, Track.id > filter).delete()
                    session.commit()

            else:	# Удаление одного элемента, в случае если id == filter
                track = session.query(Track).filter(Track.id == id).first()
                session.delete(track)
                session.commit()

        else:	# Случай когда filter принимается, как равенство
            if filter == '>':
                session.query(Track).filter(Track.id > id).delete()
                session.commit()

            elif filter == '<':
                session.query(Track).filter(Track.id < id).delete()
                session.commit()

            elif filter == '>=':
                session.query(Track).filter(Track.id >= id).delete()
                session.commit()

            elif filter == '<=':
                session.query(Track).filter(Track.id <= id).delete()
                session.commit()

            else:	# Если равенство(=, ==), или же неизвестное значение, удаление одного элемента
                track = session.query(Track).filter(Track.id == id).first()
                session.delete(track)
                session.commit()

    else:	# Удаление одного элемента, когда filter не указан
        track = session.query(Track).filter(Track.id == id).first()
        session.delete(track)
        session.commit()

def del_rt_track(real_title):		# Удаление музыки из базы данных по имени файла
    session = db_session.create_session()
    track = session.query(Track).filter(Track.real_title == real_title).first()
    session.delete(track)
    session.commit()