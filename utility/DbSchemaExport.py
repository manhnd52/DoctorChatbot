from neo4j import GraphDatabase

# Cấu hình kết nối
uri = "neo4j://localhost:7687"
user = "neo4j"
password = "12345678"

class Neo4jInspector:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        print("Connected to Neo4j database.")

    def close(self):
        self.driver.close()

    def query(self, cypher_query):
        with self.driver.session(database="doctor") as session:
            result = session.execute_read(lambda tx: list(tx.run(cypher_query)))
            return result

    def get_labels(self):
        return self.query("CALL db.labels()")

    def get_relationship_types(self):
        return self.query("CALL db.relationshipTypes()")

    def get_property_keys(self):
        return self.query("CALL db.propertyKeys()")

    def get_node_properties(self):
        return self.query("CALL db.schema.nodeTypeProperties()")

    def get_relationship_properties(self):
        return self.query("CALL db.schema.relTypeProperties()")

    def get_node_relationships(self):
        return self.query("MATCH (a)-[b]-(c) RETURN DISTINCT labels(a)[0], type(b), labels(c)[0] ")

# --- Sử dụng ---
inspector = Neo4jInspector(uri, user, password)

with open("database-schema.txt", "w", encoding="utf-8") as f:
    # f.write("# Labels:\n")
    # for label in inspector.get_labels():
    #     f.write(f"- {label["label"]}\n")

    # f.write("\n# Relationship Types:\n")
    # for record in inspector.get_relationship_types():
    #     f.write(f"- {record["relationshipType"]}\n")

    # f.write("\n# Property Keys:\n")
    # for record in inspector.get_property_keys():
    #     f.write(f"- {record}\n")

    f.write("\n# Node Properties:\n")
    node_properties = {
    }
    for record in inspector.get_node_properties():
        labels = record["nodeLabels"]
        for label in labels:
            if label not in node_properties:
                node_properties[label] = []
            node_properties[label].append(record["propertyName"])

    for label, properties in node_properties.items():
        f.write(f"## {label}:\n")
        for prop in properties:
            f.write(f"- {prop}\n")

    f.write("\n# Relationship Properties:\n")
    relationship_properties = {
    }
    for record in inspector.get_relationship_properties():
        if record["propertyName"] is not None:
            rel_type = record["relType"]
            if rel_type not in relationship_properties:
                relationship_properties[rel_type] = []
            relationship_properties[rel_type].append(record["propertyName"])
    for rel_type, properties in relationship_properties.items():
        f.write(f"## {rel_type}:\n")
        for prop in properties:
            f.write(f"- {prop}\n")
    
    print("Database schema exported to database-schema.txt")

    f.write("\n# Relationships Between Nodes:\n")
    node_relationships = {
    }
    for record in inspector.get_node_relationships():
        start_label = record["labels(a)[0]"]
        rel_type = record["type(b)"]
        end_label = record["labels(c)[0]"]
        f.write(f"- {start_label} -[{rel_type}]- {end_label}\n")

inspector.close()
