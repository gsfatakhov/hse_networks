## Лабораторная работа 2

### Описание работы со скриптом 

#### Запуск скрипта:

```shell
docker build -t mtu-finder . # Собираем контейнер

docker run --rm mtu-finder 77.88.55.242 # Запускаем его
```

#### Полученный вывод:
```
Target IP: 77.88.55.242
Target availability: reachable
ICMP: not blocked
Result MTU: 1500 bytes (MSS 1472 + 28 bytes in headers)
```

#### Проверка вывода:

Отправляем MSS:
```shell
ping -D -s 1472 77.88.55.242
   
PING 77.88.55.242 (77.88.55.242): 1472 data bytes
1480 bytes from 77.88.55.242: icmp_seq=0 ttl=244 time=13.886 ms
1480 bytes from 77.88.55.242: icmp_seq=1 ttl=244 time=13.433 ms
1480 bytes from 77.88.55.242: icmp_seq=2 ttl=244 time=13.742 ms
1480 bytes from 77.88.55.242: icmp_seq=3 ttl=244 time=13.657 ms


ping -D -s 1473 77.88.55.242

PING 77.88.55.242 (77.88.55.242): 1473 data bytes
ping: sendto: Message too long
ping: sendto: Message too long
Request timeout for icmp_seq 0
ping: sendto: Message too long
Request timeout for icmp_seq 1
```


#### Описание и ответ:

Получили размер тела запроса (MSS) 1472 байт, 20 байт `IP header`, 8 байт `ICMP request header`.

Итого размер сообщения состовляет: `1472 + 20 + 8 = 1500` байт.


**Ответ: 1500**


### Описание скрипта

Скрипт выполняет необходимые проверки и валидацию введенных данных, проверяет достижимость и ICMP запросы к введенному хост. Далее бинарным поиском находит максимальное MTU при котором запрос без фрагментации будет доходить успешно.
