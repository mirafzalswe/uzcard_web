def connect_bs():
    import psycopg2

    db_params = {
        'dbname': 'mirafzal',
        'user': 'mirafzal',
        'password': 'mirafzal',
        'host': 'localhost',
        'port': '5432'
    }

    try:
        conn = psycopg2.connect(**db_params)
        print("Успешное подключение к базе данных")
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        exit()

    cur = conn.cursor()

    card_num = '1234567890123456'
    query = """
    SELECT * FROM transactions
    WHERE card_num = %s
    """
    cur.execute(query, (card_num,))

    # Получение и вывод всех строк результата
    rows = cur.fetchall()
    for row in rows:
        print(row)

    # Закрытие курсора и соединения
    cur.close()
    conn.close()
