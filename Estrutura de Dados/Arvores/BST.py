class BST():
    '''
    Binary Search Tree

    '''
    def __init__(self, data=None, upper=None, left=None, right=None) -> None:
        self.data = data
        self.left = left
        self.right = right
        self.upper = upper

    def __str__(self) -> str:
        return str(self.data)

    def height(self) -> int:
        '''
        Returns the height of the  Binary Search Tree
        
        '''
        if self is None:
            return -1
        elif self.right is None or self.left is None:
            return 0
        else:
            return 1 + max( self.left.height(), self.right.height() )

    def insert(self, value) -> None:
        '''
        Place a new value in the Binary Search Tree
        
        '''
        upper = None
        x = self
        if x is None or x.data is None:
            return BST(value)
        else:
            while x:
                upper = x
                if value < x.data:
                    x = x.left
                else:
                    x = x.right
            if value < upper.data:
                upper.left = BST(value, upper)
                return self
            else:
                upper.right = BST(value, upper)
                return self

    def inOrder(self) -> None:
        '''
        Show the Binary Search Tree in in-order
        
        '''
        if self:
            if self.left:
                self.left.inOrder()
            print(self, end=" ")
            if self.right:
                self.right.inOrder()

    def preOrder(self) -> None:
        '''
        Show the Binary Search Tree in pre-order
        
        '''
        if self:
            print(self, end=" ")
            if self.left:
                self.left.preOrder()
            if self.right:
                self.right.preOrder()

    def postOrder(self) -> None:
        '''
        Show the Binary Search Tree in post-order
        
        '''
        if self:
            if self.left:
                self.left.postOrder()
            if self.right:
                self.right.postOrder()
            print(self, end=" ")

    def show(self, pref="  ", n=0) -> None:
        '''
        Show the Binary Search Tree with the prefix beginning from level n
        
        '''
        if self:
            print(f"{n*pref}{self.data}")
            if self.left:
                self.left.show(pref, n+1)
            if self.right:
                self.right.show( pref, n+1)

def rightRotation(tree) -> BST:
    '''
    Create a new Tree rotated to the right from any Binary Search Tree
    
    '''
    if tree is None or tree.left is None:
        return tree
    return BST(tree.left.data, None, tree.left.left, BST(tree.data, tree.left.data, tree.left.right, tree.right))

def leftRotation(tree) -> BST:
    '''
    Create a new Tree rotated to the left from any Binary Search Tree
    
    '''
    if tree is None or tree.right is None:
        return tree
    return BST(tree.right.data, None, BST(tree.data, tree.right.data, tree.left, tree.right.left), tree.right.right)

def arrayToTree(array: list[int]) -> BST:
    '''
    Create a Binary Search Tree from a list

    !!!!!!!!!need to balance this!!!!!!!!!!!!

    '''
    tree = BST(array.pop())
    while len(array) > 0:
        value = array.pop()
        upper = None
        x = tree
        while x:
            upper = x
            if value < x.data:
                x = x.left
            else:
                x = x.right
        if value < upper.data:
            upper.left = BST(value, upper)
        else:
            upper.right = BST(value, upper)
    return tree

def show_aux(tree: BST) -> str:
    '''
    Show a part of a Binary Search Tree with parentheses
    
    '''
    if tree:
        return f"{tree.data} ({show_aux(tree.left)}) ({show_aux(tree.right)})"
    return ""

def show(tree: BST) -> None:
    '''
    Show the entire Binary Search Tree with parentheses
    
    '''
    print(f"({show_aux(tree)})")

def showLevel(tree:BST, n:int) -> None:
    '''
    Show all n-level subtrees of a Binary Search Tree
    
    '''

    if tree is None:
        return None
    elif n == 0:
        return show(tree) # showAligned(tree)
    showLevel(tree.left, n-1)
    showLevel(tree.right, n-1)

def showAligned(tree:BST, pref="  ", n=0) -> None:
    '''
    Show the Binary Search Tree with the prefix beginning from level n
    
    '''
    if tree:
        print(f"{n*pref}{tree.data}")
        showAligned(tree.left, pref, n+1)
        showAligned(tree.right, pref, n+1)
    
def elemtsLevel(tree, n:int, array=[]) -> list:
    '''
    Create a list with all n-level elements of a Binary Search Tree

    '''
    if tree is None:
        return None
    elif n == 0:
        array.append(tree.data)
    elemtsLevel(tree.left, n-1, array)
    elemtsLevel(tree.right, n-1, array)
    return array

def LevelOfElemt(tree, n:int) -> int:
    '''
    Returns the level of a specific element n of a Binary Search Tree

    '''
    if tree:
        for h in range(tree.height() + 1):
            array = []
            if n in elemtsLevel(tree, h, array):
                return h
        return -1

def LevelOfElemt_2(tree, n:int, h=0) -> int:
    '''
    Returns the level of a specific element n of a Binary Search Tree

    '''
    if tree:
        if tree.data == n:
            return h
        return max ( LevelOfElemt_2(tree.left, n, h+1), LevelOfElemt_2(tree.right, n, h+1))
    return -1

def pathToElemt(tree, n:int, h=0, hsh={}) -> dict:
    '''
    Returns a dict of the path for a specific element n of a Binary Search Tree

    '''
    if tree:
        if tree.data == n:
            hsh[h] = tree.data
            return hsh
        else:
            pathToElemt(tree.right, n, h+1, hsh)
            pathToElemt(tree.left, n, h+1, hsh)
        if hsh != {} and min(hsh.keys()) == h+1:
            hsh[h] = tree.data
            return hsh # sorted(hsh.values(), key=lambda x:hsh.keys())
    return hsh 

def isBST(tree) -> bool:
    '''
    Checks if a Tree is a Binary Search Tree
    
    '''
    if tree:
        if tree.left:
            if tree.left.data < tree.data:
                if not isBST(tree.left):
                    return False
            else:
                return False
        if tree.right:
            if tree.right.data > tree.data:
                if not isBST(tree.right):
                    return False
            else:
                return False
    return True

l = [2,4,8,10,1,6]
tree = arrayToTree(l)
tree.left.right = rightRotation(tree.left.right)
tree.left = leftRotation(tree.left)

show(tree)
showAligned(tree)
print(elemtsLevel(tree, 2))
showLevel(tree, 1)
print(LevelOfElemt(tree, 10))
print(LevelOfElemt_2(tree, 10))
print(pathToElemt(tree, 10))
tree.show()







