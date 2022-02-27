#!/bin/bash

#Если значение переменной ENV равно DEV, то запускается веб-сервер для отладки, в противном случае будет использоваться «настоящий» сервер для эксплуатации. Команда exec нужна для того, чтобы не создавать нового процесса и обеспечить получение и обработку любых сигналов (таких как SIGTERM) единственным процессом uwsgi, а не избыточным родительским процессом.

set -e

if [ "$ENV" = 'DEV' ]; then
	echo "Running Development Server"						# Запуск сервера для разработки
	exec python "identidock.py"
elif [ "$ENV" = 'UNIT' ]; then									
	echo "Running Unit Tests"							# Заупск тестирования при ENV=UNIT
	exec python "tests.py"
else
	echo "Running Production Server" 						# Запуск сервера для эксплуатации
	exec uwsgi --http 0.0.0.0:9090 --wsgi-file /app/identidock.py \
 		--callable app --stats 0.0.0.0:9191
fi
