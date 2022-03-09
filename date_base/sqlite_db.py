import sqlite3 as sq


def sql_start():
    try:
        global base, cur
        base = sq.connect('count_date.db')
        cur = base.cursor()
        if base:
            print('Date base connected OK!')
            base.execute('CREATE TABLE IF NOT EXISTS user_data(user_name TEXT, date_1 TEXT, date_2 TEXT, result_1 TEXT, count_people TEXT, result_2 TEXT)')
            base.commit()

    except sq.Error as error:
        print("Ошибка при работе с SQLite", error)

    # finally:
    #     if base:
    #         base.close()
    #         print("Соединение с SQLite закрыто")

async def sql_add_command(state):
    #try:
    async with state.proxy() as data:
        result = cur.execute('SELECT * FROM user_data').fetchall()
        for x in result:
            user_name = x[0]
            if data['user_name'] == user_name:
                cur.execute(f'UPDATE user_data SET user_name=?, date_1=?, date_2=?, result_1=?, count_people=?, result_2=? WHERE user_name= {user_name}',
                            tuple(data.values()))
                base.commit()
                return
        cur.execute('INSERT INTO user_data VALUES (?, ?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()



    #except sq.Error as error:
        # print("Ошибка при работе с SQLite", error)

    # finally:
    #     if base:
    #         base.close()
    #         print("Соединение с SQLite закрыто")
