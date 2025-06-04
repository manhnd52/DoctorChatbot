from neo4j import GraphDatabase

# Thông tin kết nối database
URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "12345678"

def run_query(query):
    driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
    with driver.session(database="doctor") as session:
        try:
            result = session.run(query)
        except Exception as e:
            print(f"QUERY ERROR: {e}")
            return None
        return result.data()
    driver.close()

