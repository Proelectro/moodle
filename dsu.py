class DSU:
    def __init__(self, size) -> None:
        self.parent = [i for i in range(size)]
        self.rank = [1 for _ in range(size)]
    
    def find(self, x):
        if self.parent[x] == x:
            return x
        self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)
        if x == y:
            return
        if self.rank[x] < self.rank[y]:
            x, y = y, x
        self.parent[y] = x
        self.rank[x] += self.rank[y]
        
    def get_rank(self, x):
        return self.rank[self.find(x)]