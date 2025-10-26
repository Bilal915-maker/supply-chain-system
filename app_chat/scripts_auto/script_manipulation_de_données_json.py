
import json
data = '{"name": "Natacha", "role": "IA"}'
parsed_data = json.loads(data)
print("Nom:", parsed_data["name"])
print("Rôle:", parsed_data["role"])
