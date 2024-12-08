import psycopg2

from config import db_user, db_host, db_password, db_port, db_name


def create_db():
	conn = psycopg2.connect(
		database="postgres",
		user=db_user,
		password=db_password,
		host=db_host,
		port=db_port
	)
	conn.autocommit = True
	cursor = conn.cursor()
	sql = f''' CREATE database {db_name} '''
	cursor.execute(sql)
	conn.close()
	print('DB was created successfully!')


if __name__=='__main__':
	create_db()
