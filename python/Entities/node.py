class Node:

    def __init__(self, id, point):
        self.id = id
        self.point = point
    
    
    def __repr__(self):
        return f"ID: {self.id}, point: {self.point}"