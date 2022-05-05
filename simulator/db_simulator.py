import sqlite3
import time


class QValueDB:
    def __init__(self):
        self.connection = self.create_connecction()
        self.create_table()

    def create_connecction(self):
        try:
            self.connection = sqlite3.connect("q_value_table.db")
            return self.connection
        except sqlite3.Error as e:
            print(e)
        return None

    def create_table(self):
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS q_values(
        slo NOT NULL,
        range_id NOT NULL,
        q_value NOT NULL);
        '''
        try:
            c = self.connection.cursor()
            c.execute(create_table_sql)
            self.connection.commit()
        except sqlite3.Error as e:
            print(e)

    def get_q_value(self, slo, range_id):
        query = '''SELECT * FROM q_values WHERE slo=? AND range_id=?'''
        c = self.connection.cursor()
        c.execute(query, (slo, range_id))
        rows = c.fetchall()
        return rows

    def save_q_value(self, slo, range_id, q_value):
        insert_sql = '''INSERT INTO q_values(slo, range_id, q_value) VALUES (?,?,?)'''
        if self.connection:
            c = self.connection.cursor()
            c.execute(insert_sql, (slo, range_id, q_value))
            self.connection.commit()
        else:
            print("Connection Error")

    def close_connection(self):
        self.connection.close()


class HistoryDB:
    def __init__(self):
        self.db_file = "experiment_history.db"
        self.connection = self.create_connection()
        self.create_table()

    def create_connection(self):
        try:
            self.connection = sqlite3.connect(self.db_file)
            return self.connection
        except sqlite3.Error as e:
            print(e)
        return None

    def create_table(self):
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY,
        experiment_id INTEGER,
        experiment_time TEXT NOT NULL,
        range_id INTEGER NOT NULL ,
        rps_range TEXT NOT NULL ,
        rps REAL NOT NULL ,
        slo REAL NOT NULL ,
        response REAL NOT NULL ,
        cost REAL NOT NULL ,
        delta_si REAL,
        delta_response REAL,
        n_s INT,
        configs TEXT NOT NULL ,
        utils TEXT NOT NULL ,
        throttles TEXT NOT NULL,
        current_configs TEXT NOT NULL, 
        threshold REAL,
        poisson TEXT,
        container_stats TEXT);
        '''
        try:
            c = self.connection.cursor()
            c.execute(create_table_sql)
            self.connection.commit()
        except sqlite3.Error as e:
            print(e)

    def close_connection(self):
        self.connection.close()

    def insert_into_table(self, data):
        insert_value_sql = '''INSERT INTO history(experiment_id, experiment_time, range_id, rps_range, rps, slo, response, cost, delta_si, delta_response, n_s, configs, utils, throttles,current_configs, threshold,poisson,container_stats) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
        if self.connection:
            try:
                c = self.connection.cursor()
                c.execute(insert_value_sql, (
                    data["experiment_id"], data["time"], data["range_id"], str(data["rps_range"]), data["rps"], data["slo"],
                    data["response"], data["cost"], data["delta_si"], data["delta_response"],
                    data["n_s"], str(data["configs"]), str(data["utils"]), str(data["throttles"]),
                    str(data["current_configs"]), data["threshold"],data["poisson"],str(data["container_stats"])))
                self.connection.commit()
            except sqlite3.Error as e:
                print(e)
        else:
            print("Connection Error")
        # write to response table data["rps"], data["range_id"], data["slo"], data["response"]
        # write to config table data["rps"], data["range_id"], data["slo"], data["configs"]
        # write to settings table data["rps"], data["range_id"], data["slo"], data["delta_r"], data["delta_si"], data["n_s"]

    def get_data(self, query=None):
        get_data_sql = '''SELECT * FROM history;'''
        c = self.connection.cursor()
        c.execute(get_data_sql)
        rows = c.fetchall()
        for row in rows:
            print(row)

    def select_response_regression(self, slo, range_id):
        query = '''SELECT * FROM history WHERE slo=? AND range_id=?'''
        c = self.connection.cursor()
        c.execute(query, (slo, range_id))
        rows = c.fetchall()
        return rows

    def get_previous_history(self, slo, range_id, cost):
        query = '''SELECT * FROM history WHERE delta_response>0 AND cost>? AND slo=? AND range_id=? ORDER BY id DESC LIMIT 1'''
        c = self.connection.cursor()
        c.execute(query, (cost, slo, range_id))
        rows = c.fetchall()
        return rows

    def get_last_configuration(self, slo, range_id):
        query = '''SELECT * FROM history WHERE slo=? AND range_id=? ORDER BY id DESC LIMIT 1'''
        c = self.connection.cursor()
        c.execute(query, (slo, range_id))
        rows = c.fetchall()
        return rows
