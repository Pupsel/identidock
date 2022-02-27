# Небольшая веб-страницей, содержащей форму для ввода имени пользователя

from flask import Flask, Response, request 							# Импорт из пакета Flask модулю Respone, используемого для передачи изображения
import requests										# Импорт библиотеки requests (http://docs.python-requests.org/en/latest/), используемой для организации диалога с сервисом dnmonster.
import hashlib		 								# Импорт библиотеки, которая будет использоваться для хэширования данных, вводимых пользователем.
import redis										# Импорт модуля Redis
import html
app = Flask(__name__)
cache = redis.StrictRedis( host='redis', port=6379, db=0 )				# Настройка кэша Redis. Мы будем использовать соединения Docker, чтобы обеспечить доступность имени хоста redis.
salt = "UNIQUE_SALT"									# Определение значения переменной salt, используемой в хэш-функции. При изменении этого значения разные сайты могут генерировать различные идентификационные пиктограммы для одних и тех же входных данных.
default_name = 'Joe Bloggs'
@app.route('/', methods=['GET', 'POST'])						# По умолчанию Flask определяет пути только для ответов на GET. Форма в исходном коде отправляет POST, поэтому необходимо добавить аргумент methods к списку путей и определить, что будут обрабатываться оба запроса POST и GET.
def mainpage():
	name = default_name
	if request.method == 'POST': 							# Если значение request.method равно значению "POST", то запрос является результатом подтверждения данных (submith). В этом случае необходимо обновить переменную name, присвоив ей текстовое значение, введенное пользователем.
		name = html.escape( request.form['name'], quote=True )			# Метод html.escape() используется для преобразования введенных пользователем данных в требуемую форму							
	salted_name = salt + name
	name_hash = hashlib.sha256( salted_name.encode() ).hexdigest()			# Выполнение операции хэширования введенных данных с использованием алгоритма SHA256
	header = '<html><head><title>Identidock</title></head><body>'
	body = '''<form method="POST">
		Hello <input type="text" name="name" value="{}">
 		<input type="submit" value="submit">
 		</form>
 		<p>You look like a:
 		<img src="/monster/{}"/>
 		'''.format(name, name_hash)						# Изменение URL изображения с учетом полученного выше хэшированного значения. При попытке загрузки файла изображения браузер будет вызывать функцию get_identicon, учитывая заданный путь и это хэшированное значение
	footer = '</body></html>'
	return header + body + footer
@app.route('/monster/<name>')
def get_identicon( name ):
	name = html.escape( name, quote=True )						# Метод html.escape() используется для преобразования введенных пользователем данных в требуемую форму
	image = cache.get( name )							# Проверка наличия текущего значения переменной name в кэше
	if image is None: 								# При промахе кэша (то есть при отсутствии текущего значения в кэше) Redis возвращает значение None. В этом случае изображение генерируется как обычно
		print( "Cache miss (промах кэша)", flush=True )				# Выводится некоторая отладочная информация об отсутствии кэшированного изображения
		r = requests.get('http://dnmonster:8080/monster/' + name + '?size=80')		# Создание HTTP-запроса GET, отправляемого сервису dnmonster. Запрашивается имя идентификационного изображения как значение переменной name, при этом размер изображения должен быть равен 80 пикселам.
		image = r.content
		cache.set( name, image )						#  Сгенерированный образ добавляется в кэш и связывается с заданным именем
	return Response( image, mimetype='image/png' ) 					# Оператор return немного усложняется из-за использования функции Response, сообщающей серверу Flask о том, что возвращается изображение в формате PNG, а не HTML-код и не текст.
if __name__ == '__main__':
	app.run( debug=True, host='0.0.0.0' )
