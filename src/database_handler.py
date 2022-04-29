import sqlite3
from datetime import date, datetime
import os
import pandas as pd

script_directory = os.path.dirname(os.path.realpath(__file__))
db_path = (
    os.path.dirname(os.path.normpath(script_directory)) + "/data/score_presentazioni.db"
)


def create_table(date_session):
    connection = sqlite3.connect(db_path, check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS ["
        + date_session
        + "] (presenter TEXT PRIMARY KEY, il_ridere INTEGER, il_sapere INTEGER, il_sacrificio INTEGER, combo INTEGER)"
    )
    connection.commit()
    cursor.close()
    connection.close()


def insert(date_session, presenter, category, final_score):
    connection = sqlite3.connect(db_path, check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(
        "INSERT or IGNORE INTO ["
        + date_session
        + "] (presenter,"
        + category
        + ") VALUES(?, ?)",
        (presenter, final_score),
    )
    cursor.execute(
        "UPDATE [" + date_session + "] SET " + category + "= (?) WHERE presenter=(?)",
        (final_score, presenter),
    )
    connection.commit()
    cursor.close()
    connection.close()


def get_combo_score(date_session):  ### risultato classifica generale
    connection = sqlite3.connect(db_path, check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("UPDATE [" + date_session + "] SET combo = il_ridere + il_sapere")
    connection.commit()
    cursor.close()
    connection.close()


def query_data(date_session):  ### TODO: fix spaghetti code
    get_combo_score(date_session)
    connection = sqlite3.connect(db_path, check_same_thread=False)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT presenter, il_ridere FROM ["
        + date_session
        + "] ORDER BY il_ridere DESC"
    )
    il_ridere_list = cursor.fetchall()
    il_ridere_classification = []
    for i in range(len(il_ridere_list)):
        name = il_ridere_list[i][0]
        score = il_ridere_list[i][1]
        il_ridere_classification.append(
            str(i + 1) + ". " + str(name) + " = " + str(score)
        )

    cursor.execute(
        "SELECT presenter, il_sapere FROM ["
        + date_session
        + "] ORDER BY il_sapere DESC"
    )
    il_sapere_list = cursor.fetchall()
    il_sapere_classification = []
    for i in range(len(il_sapere_list)):
        name = il_sapere_list[i][0]
        score = il_sapere_list[i][1]
        il_sapere_classification.append(
            str(i + 1) + ". " + str(name) + " = " + str(score)
        )

    cursor.execute(
        "SELECT presenter, il_sacrificio FROM ["
        + date_session
        + "] ORDER BY il_sacrificio DESC"
    )
    il_sacrificio_list = cursor.fetchall()
    il_sacrificio_classification = []
    for i in range(len(il_sacrificio_list)):
        name = il_sacrificio_list[i][0]
        score = il_sacrificio_list[i][1]
        il_sacrificio_classification.append(
            str(i + 1) + ". " + str(name) + " = " + str(score)
        )

    cursor.execute(
        "SELECT presenter, combo FROM [" + date_session + "] ORDER BY combo DESC"
    )
    combo_list = cursor.fetchall()
    combo_classification = []
    for i in range(len(combo_list)):
        name = combo_list[i][0]
        score = combo_list[i][1]
        combo_classification.append(str(i + 1) + ". " + str(name) + " = " + str(score))

    return (
        combo_classification,
        il_ridere_classification,
        il_sapere_classification,
        il_sacrificio_classification,
    )


def get_table_list():
    connection = sqlite3.connect(db_path, check_same_thread=False)
    cursor = connection.cursor()
    list = []
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for name in tables.fetchall():
        list.append(name[0])
    cursor.close()
    connection.close()
    return list
