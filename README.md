Данный бот создан для пробразования резервных копий для Z-Way между разными архетектурами.

файлы:
bot.py - основной скрипт запуска бота

zabToJSON.py - скрипт котороый берет файл из параметра запуска, и преобразует его в .json файл с заменой оригинала

jsonToZAB.py - скрипт выполняет обратное действие, принимает файл .json и запоковывает его в .zab с заменой оригинала

update_config.py - скрипт который берет файл из параметра запуска, и 2 параметра запуска --config --port

далее он в этом файле идет к соответствующим ключам и меняет их содержимое на то которое было в параметрах запуска
config.json/instances/0/params/config
config.json/instances/0/params/port


Данный боту умеет следующее:
	Принимать файл в telegram, пропуская только файл резервной копии с расширением .zab
	Преобразовывать данный .zab файл в .json объект
	Выводит кнопки после получения и преобразования файла:
		Преобразовать резервную копию для Z-Wave.Me HUB
    		Преобразовать резервную копию для Raspberry pi или linux систем с платой Razberry
    		Преобразовать резервную копию для Raspberry pi с UZB стиком
    		Преобразовать резервную копию для Home Assistant Z-Way Addon с платой Razberry
    		Преобразовать резервную копию для Home Assistant Z-Way Addon с UZB стиком
    - в json файле меняются ключи port и config, после этого файл отправляется обратно отправителю

