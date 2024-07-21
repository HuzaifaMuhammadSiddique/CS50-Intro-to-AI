import csv  
import sys  

from util import Node, StackFrontier, QueueFrontier  # check util file for this

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}

def load_data(directory):
    
    # Load people and names
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)  
        for row in reader:  # this translated to: for every dictionary in the file
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()  # the movies (for now at least) is an empty set.
            }         
            # Gets the name of the person (in question) and converts it into lowercase
            current_name = row["name"].lower()  # e.g. "kevin bacon"

            if current_name not in names:
                names[current_name] = {row["id"]}
            else:
                names[current_name].add(row["id"])


    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)       
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set() # the stars (for now at least) is an empty set.
            }

    # Load movies and stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])       
                movies[row["movie_id"]]["stars"].add(row["person_id"])
                
            # In what case can this occur (?)    
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "small"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")
    
    # print(names)
    
    # print("\n")
    
    # print(people)
    
    # print("\n")
    
    # print(movies)
    
    # print("\n")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)
    # path = None
    
    
    # testing
    # a = neighbors_for_person(source)
    # print(a)
    # for t in a:
    #     print(type(t[0]))
    #     print(type(t[1]))

    # print(people[source])

    # print(source)
    # print(target)
    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    num_explored = 0
    
    initial_node = Node(state=source, parent=None, action=neighbors_for_person(source))
    
    frontier = QueueFrontier()
    frontier.add(initial_node)

    explored = set()
    
    # Keep looping until solution found
    while True:

        # If nothing left in frontier, then no path
        if frontier.empty():
            raise Exception("no solution")

        # Choose a node from the frontier
        node = frontier.remove()
        num_explored += 1
        
        if node.state == target:
            actions = []
            
            
            while (node.parent is not None) and (node is not None):
                                              
                for item in node.action:
                    if item[1] == node.state:
                        actions.append(item)
                        break
                    
                node = node.parent
                        
            actions.reverse()
            return actions
        
        
        # Mark node as explored
        explored.add(node.state)

    
        for t in node.action:  # checks every element of the set
            current_id = t[1]
            if not frontier.contains_state(current_id) and current_id not in explored:
                new_child = Node(state=current_id, parent=node, action=neighbors_for_person(current_id))
                frontier.add(new_child)

    
    
    
    
    


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0] # returns an ID for the name


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    
    
    
    
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
