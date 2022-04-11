class arquive():
    def __init__(self, data, parent=None, isDir=True) -> None:
        self.data = data
        self.parent = parent
        self.children = []
        self.isDir = isDir

    def __str__(self) -> str:
        return str(self.data)

    def show(self, level=0) -> None:
        print(f'{"---" * level}{self.data}')
        for child in sorted(self.children, key=lambda x:x.data):
            child.show(level + 1)

    def cd(self, dir) -> object:
        if dir == '' or dir == '.':
            return self
        arq_aux = self
        for child in sorted(arq_aux.children, key=lambda x:x.data):
            if child.data == dir:
                if child.isDir:
                    arq_aux = child
                else:
                    raise Exception("COMANDO INVÁLIDO")
        if arq_aux == self:
            raise Exception("CAMINHO INVÁLIDO")
        return arq_aux

    def pwd(self) -> str:
        parent = self.parent
        if parent:
            return parent.pwd() + '/' + self.data
        return ''

    def mkdir(self, dir) -> object:
        for child in self.children:
            if dir == child.data: 
                return child
        self.children.append(arquive(dir, self))
        return self.children[-1]

    def dirRepetido(self, dir) -> bool:
        for child in self.children:
            if dir == child.data: # retirar '  and child.isDir ' caso arq e dir devem ser !=
                return True
        self.children.append(arquive(dir, self))
        return False

    def rm(self, arquiv) -> object:
        for child in self.children:
            if arquiv == child.data:
                self.children.remove(child)
                return child
        return None

    def touch(self, arq) -> None:
        for child in self.children:
            if arq == child.data:
                if child.isDir:
                    return print("CAMINHO INVÁLIDO")
                else:
                    return print("ARQUIVO JÁ EXISTE")
        self.children.append(arquive(arq, self, False))
        return None

    def find(self, target) -> None:
        if self.data == target:
            return self
        for child in sorted(self.children, key=lambda x:x.data):
            response = child.find(target)
            if response:
                print(response.pwd())
        return None

def followPath(path:list[str]) -> arquive:
    if path[0] == '.' or path[0] == '..':
        global arq
        arq_aux = arq
    else:
        arq_aux = root
    for dir in path:
        if dir == '..':
            arq_aux = arq_aux.parent
            if arq_aux is None:
                raise Exception("CAMINHO INVÁLIDO")
        else:
            try: 
                arq_aux = arq_aux.cd(dir)
            except Exception as e:
                raise Exception(e)
    return arq_aux


arq = arquive('/')
root = arq 
while True:
    cmd = input().split(' ', 1)
    if cmd[0] == 'show':
        root.show() 
    elif cmd[0] == 'cd':
        try:
            arq = followPath(cmd[1].split('/'))
        except Exception as e:
            print(e)
    elif cmd[0] == 'pwd':
        if arq.data == '/':
            print('/')
        else:
            print(arq.pwd())
    elif cmd[0] == 'mkdir':
        arq_aux = root
        if cmd[1] == '/':
            print("DIRETÓRIO JÁ EXISTE")
        else:
            path = cmd[1].split('/')[1:]
            lastDir = path.pop()
            for dir in path:
                arq_aux = arq_aux.mkdir(dir)
            if arq_aux.dirRepetido(lastDir):
                print("DIRETÓRIO JÁ EXISTE")
    elif cmd[0] == 'mv': 
        originPath, destinyPath = cmd[1].split() 
        if originPath[-1] == '.':
            originPath += '/'
        destinyPath, originPath = destinyPath.split('/'), originPath.split('/')
        arqToMove = originPath.pop()
        try:
            originResponse, destinyResponse = followPath(originPath), followPath(destinyPath) 
            if originResponse.data == '/' and arqToMove == '': pass
            else:
                if arqToMove == '':
                    arqToMove = originResponse.data
                    originResponse = originResponse.parent
                arqToMove = originResponse.rm(arqToMove)
                if arqToMove:
                    destinyResponse.rm(arqToMove.data) # deletar se tiver dado antigo para sobreescrever
                    arqToMove.parent = destinyResponse
                    destinyResponse.children.append(arqToMove)
                else:
                    print("ARQUIVO ou DIRETÓRIO não existe")   
        except Exception as e:
            print(e)
    elif cmd[0] == 'touch':
        arq_aux = root
        path = cmd[1].split('/')
        lastArq = path.pop()
        if len(path) > 0:
            try:
                arq_aux = followPath(path)
                arq_aux.touch(lastArq)
            except Exception as e:
                print("CAMINHO INVÁLIDO")
    elif cmd[0] == 'rm':
        if cmd[1][-1] == '.':
            cmd[1] += '/'
        path = cmd[1].split('/') 
        arqToRemove = path.pop()
        try:
            response = followPath(path)
            if response.data == '/' and arqToRemove == '': pass 
            else:
                if arqToRemove == '':
                    arqToRemove = response.data
                    response = response.parent
                arqToRemove = response.rm(arqToRemove)
                if arqToRemove:
                    if arqToRemove.data in arq.pwd().split('/'): 
                        arq = root
                else:
                    print("ARQUIVO ou DIRETÓRIO não existe")
        except Exception as e:
            print(e)
    elif cmd[0] == 'find':
        root.find(cmd[1])
    elif cmd[0] == 'end':
        break