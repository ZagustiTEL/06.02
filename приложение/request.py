import sqlite3
from datetime import date

conn = sqlite3.connect('avtovokzal.db')
cursor = conn.cursor()

# 1. ВСЕ РЕЙСЫ ЗА СЕГОДНЯШНИЙ ДЕНЬ
print("\n1. РЕЙСЫ НА СЕГОДНЯ:")

today = date.today().strftime('%Y-%m-%d')
cursor.execute('''
    SELECT departure_time, route_number, departure_city, arrival_city
    FROM BusSchedule 
    JOIN Routes ON BusSchedule.route_id = Routes.route_id
    WHERE date(departure_time) = ?
''', (today,))

trips = cursor.fetchall()
if trips:
    for trip in trips:
        print(f"{trip[0]} | {trip[1]} | {trip[2]} -> {trip[3]}")
else:
    print("На сегодня рейсов нет")

# 2. САМЫЙ ПОПУЛЯРНЫЙ МАРШРУТ
print("\n2. САМЫЙ ПОПУЛЯРНЫЙ МАРШРУТ:")

cursor.execute('''
    SELECT route_number, departure_city, arrival_city, COUNT(*) as count
    FROM Routes
    JOIN BusSchedule ON Routes.route_id = BusSchedule.route_id
    GROUP BY Routes.route_id
    ORDER BY count DESC
    LIMIT 1
''')

popular = cursor.fetchone()
if popular:
    print(f"{popular[0]}: {popular[1]} -> {popular[2]} ")

# 3. ПАССАЖИР ПОТРАТИВШИЙ БОЛЬШУЮ СУММУ
print ("\n3. ПАССАЖИР ПОТРАТИВШИЙ БОЛЬШУЮ СУММУ")

cursor.execute('''
    SELECT 
        Passengers.last_name || ' ' || Passengers.first_name || ' ' || Passengers.middle_name AS full_name,
        Passengers.passport_number,
        SUM(Tickets.price) AS total_spent,
        COUNT(Tickets.ticket_id) AS tickets_count
    FROM Passengers
    JOIN Tickets ON Passengers.passenger_id = Tickets.passenger_id
    GROUP BY Passengers.passenger_id
    ORDER BY total_spent DESC
    LIMIT 1
''')

top_passenger = cursor.fetchone()
if top_passenger:
    print(f"Пассажир: {top_passenger[0]}")
    print(f"Всего потрачено: {top_passenger[2]}")
    print(f"Куплено билетов: {top_passenger[3]}")
else:
    print("Данные о покупках отсутствуют")


conn.close()

conn.close()