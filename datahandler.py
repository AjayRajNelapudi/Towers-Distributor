import json
import numpy as np

class Serializer:
    '''
    Serializes the tower distribution data structure to write to files
    '''
    def __init__(self, tower_distribution):
        self.tower_distribution = tower_distribution

    def serialize(self):
        self.stringified_structure = dict()
        for key, region in self.tower_distribution.items():
            self.stringified_structure[key] = {
                'base_station': str(region['base_station']),
                'users': "[" + ",".join([str(user) for user in region['users']]) + "]",
                # 'cell_sites': "[" + ",".join([str(cell_site) for cell_site in region['cell_sites']]) + "]",
            }
        return self.stringified_structure

    def save(self, filename):
        writeable_structure = json.dumps(self.stringified_structure)
        with open(filename, "w") as output_file:
            output_file.write(writeable_structure)

class Deserializer:
    '''
    Deserializes the tower distribution stringified data structure
    '''
    def __init__(self):
        pass

    def deserialize(self):
        self.tower_distribution = dict()
        for key, region in self.stringified_structure.items():
            base_station = np.fromstring(
                region['base_station'].replace("[", "").replace("]", ""),
                dtype=np.float,
                sep=" "
            )

            users = np.array(
                [
                    np.fromstring(
                        user.replace("[", "").replace("]", ""),
                        dtype=np.float,
                        sep=" "
                    )
                    for user in region['users'].split(",")
                ]
            )

            cell_sites = np.array(
                [
                    np.fromstring(
                        cell_site.replace("[", "").replace("]", ""),
                        dtype=np.float,
                        sep=" "
                    )
                    for cell_site in region['cell_sites'].split(",")
                ]
            )

            self.tower_distribution[key] = {
                'base_station': base_station,
                'users': users,
                'cell_sites': cell_sites
            }

        return self.tower_distribution

    def restore(self, filename):
        with open(filename) as output_file:
            self.stringified_structure = json.load(output_file)

if __name__ == "__main__":
    deserializer = Deserializer()
    deserializer.restore("tower-distribution.json")
    structure = deserializer.deserialize()

    print(structure)
