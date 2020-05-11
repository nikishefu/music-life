# Вспомогающий - связующий файл, для работы базы данных
# С помощью него просиходит работа с таблицами в БД


import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()		# Абстрактная декларированная база

__factory = None	# Для получения сессий и подключения к таблицам

def global_init(db_file):	# Инициализация базы данных
	# Обьяснение для global_init:
	# Функция принимает на вход адрес базы данных,
	# Затем проверяет, не создано ли уже фабрика подключений
	# В случае, если уже создано, то происходит завершение работы,
	# Так как начальную инициализацию надо проводить только единожды.

	global __factory

	if __factory:
		return

	if not db_file or not db_file.strip():
		raise Exception("Необходимо указать файл базы данных.")

	conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
	print(f"Подключение к базе данных по адресу {conn_str}")

	engine = sa.create_engine(conn_str, echo=False)
	__factory = orm.sessionmaker(bind=engine)

	from . import __all_models

	SqlAlchemyBase.metadata.create_all(engine)

def create_session() -> Session:
	# Функция create_session нужна для получения сессии подключения к нашей базе данных.

	global __factory
	return __factory()
