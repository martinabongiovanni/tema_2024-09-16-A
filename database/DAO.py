from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_limit_range():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """
                        SELECT MIN(s.Lat) as lat_min, MAX(s.Lat) as lat_max, MIN(s.Lng) as lon_min, MAX(s.Lng) as lon_max
                        FROM state s"""
            cursor.execute(query)

            for row in cursor:
                result.append((row['lat_min'], row['lat_max'], row['lon_min'], row['lon_max']))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_shapes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """
                        SELECT DISTINCT s.shape
                        FROM sighting s 
                        WHERE s.shape IS NOT NULL AND s.shape != ""
                        ORDER BY s.shape DESC"""
            cursor.execute(query)

            for row in cursor:
                result.append((row['shape']))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_states_by_input(lat, lon, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """
                        SELECT DISTINCT st.id, st.Name, st.Capital, st.Lat, st.Lng, st.Area, st.Population, st.Neighbors 
                        FROM state st, sighting si
                        WHERE st.Lat > %s AND st.Lng > %s AND si.shape = %s
                        """
            cursor.execute(query, (lat, lon, shape))

            for row in cursor:
                result.append(State(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_total_duration(state_id, lat, lon, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """
                        SELECT SUM(si.duration) as duration
                        FROM sighting si, state st
                        WHERE UPPER(si.state) = %s AND st.Lat > %s AND st.Lng > %s AND si.shape = %s"""
            cursor.execute(query, (state_id, lat, lon, shape))

            for row in cursor:
                result.append((row['duration']))
            cursor.close()
            cnx.close()
        return result
