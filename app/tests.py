import unittest
import identidock
class TestCase( unittest.TestCase ):
	def setUp( self ):								# Инициализация тестовой версии веб-приложения с использованием сервера Flask
		identidock.app.config["TESTING"] = True
		self.app = identidock.app.test_client()
	def test_get_mainpage( self ):							# Тестирование метода, вызывающего URL / с передачей в поле name значения "Moby Dick". Затем тест проверяет код возврата этого метода на равенство значению 200, при этом данные должны содержать строки 'Hello' и 'Moby Dick'
		page = self.app.post( "/", data=dict(name="Moby Dick") )
		assert page.status_code == 200
		assert 'Hello' in str( page.data )
		assert 'Moby Dick' in str( page.data )
	def test_html_escaping( self ):							# Проверка правильности экранирования HTML-элементов в потоке ввода
		page = self.app.post( "/", data=dict(name='"><b>TEST</b><!--') )
		assert '<b>' not in str( page.data )
if __name__ == '__main__':
	unittest.main()
