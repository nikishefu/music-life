# Файл класса User (таблицы - users), а также файл
# Имеющий инструменты для взаимодействия с таблицей (users)


import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from . import db_session
import hashlib
from sqlalchemy import orm


class User(SqlAlchemyBase):		# Сама таблица (Все строки существующие в таблице)

	__tablename__ = 'users'

	id = sqlalchemy.Column(sqlalchemy.Integer,
                          primary_key=True, autoincrement=True)
	name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
	surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
	login = sqlalchemy.Column(sqlalchemy.String, nullable=False)
	password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
	email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
	created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now,
									nullable=False)

	musics = orm.relation("Track", back_populates='user')


def add_user(name, login, password, email, surname=None):	# Добавление пользователя в таблицу
	user = User()
	user.name, user.surname = name, surname		# Имя и Фамилия пользователя (Фамилия не обязательна)
	user.login, user.password = login, password		# Логин и пороль пользователя для входа
	user.email = email		# Емаил пользователя
	session = db_session.create_session()
	session.add(user)
	session.commit()

def del_id_user(id, filter=None, filt_incl=False):	# Удаление пользователя из таблицы

	session = db_session.create_session()

	if filter != None:		# В случае если задается филтр

#	Обьяснение для filter:
#	Фильтр задается когда нужно удалить более 1 элемента
#	В случае если фильтр является числом типа int: то удаляется срез ID элементов,
#	Которых находится между параметром id и filter
#	Так-же filter можно задать, как знак равенства, тогда в зависимости
# 	От знака, будет выбран опреденный срез начинающийся или заканчивающийся на id
#	Атрибут filt_incl нужен, в случиях, когда filter является числом,
#	Тогда в значение True, срез будет выбран включительно с id и самим filter'ом.

		if type(filter) == int:		# Срез между filter и id

			if filter > id:		# Срез id --- filter

				if filt_incl:	# Включительно

					session.query(User).filter(User.id >= id, User.id <= filter).delete()
					session.commit()

				else:	# Не включая

					session.query(User).filter(User.id > id, User.id < filter).delete()
					session.commit()

			elif filter < id:	# Срез filter --- id

				if filt_incl:	# Включительно

					session.query(User).filter(User.id <= id, User.id >= filter).delete()
					session.commit()

				else:	# Не включая

					session.query(User).filter(User.id < id, User.id > filter).delete()
					session.commit()

			else:	# Удаление одного элемента, в случае если id == filter

				user = session.query(User).filter(User.id == id).first()
				session.delete(user)
				session.commit()

		else:	# Случай когда filter принимается, как равенство

			if filter == '>':

				session.query(User).filter(User.id > id).delete()
				session.commit()

			elif filter == '<':

				session.query(User).filter(User.id < id).delete()
				session.commit()

			elif filter == '>=':

				session.query(User).filter(User.id >= id).delete()
				session.commit()

			elif filter == '<=':

				session.query(User).filter(User.id <= id).delete()
				session.commit()

			else:	# Если равенство(=, ==), или же неизвестное значение, удаление одного элемента

				user = session.query(User).filter(User.id == id).first()
				session.delete(user)
				session.commit()

	else:	# Удаление одного элемента, когда filter не указан

		user = session.query(User).filter(User.id == id).first()
		session.delete(user)
		session.commit()
