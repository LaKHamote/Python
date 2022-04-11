def crypto(s):
    base = [str(i+1) for i in range(len(s) + 1)]
    key = ''
    count = 0
    aux = 0
    if s[0] == '+':
        aux = 1
        key += base.pop(0)
    for i in s[aux:]:
        if i == '-':
            count += 1
        else:
            for i in range(count + 1)[::-1]:
                key += base.pop(i)
            count = 0
    for i in range(count + 1)[::-1]:
        key += base.pop(i)
    print(key)


def deYodafy(w):
    punctuation = ''
    if w != '' and w[-1] in '!"#$%&()*+,-./:;<=>?@[\]^_`{|}~':
        punctuation = w[-1]
        w = w[:-1]
    print(' '.join(w.split()[::-1]) + punctuation)


def merge(i):
    gaps = sorted([eval(gap) for gap in i.replace(', ',',').split()])
    newGaps = []
    newStart, newEnd = gaps[0][0], gaps[0][1]
    for gap in gaps[1:]:
        currentStart, currentEnd = gap[0], gap[1]
        if currentStart <= newEnd:
            if currentEnd > newEnd:
                newEnd = currentEnd
        else:
            newGaps.append([newStart, newEnd])
            newStart, newEnd = currentStart, currentEnd
    newGaps.append([newStart, newEnd])
    print(*newGaps)


def halt(commands):
    print(f'{len(commands)} processo(s) e {sum([len(cmd) for cmd in commands])} comando(s) órfão(s).')


def process(commands):
    func, argument = commands[0].pop(0)
    eval(func)(argument)
    leftOvers = commands.pop(0)
    if leftOvers != []:
        commands.append(leftOvers)
    return commands


currentCommand = 'Start'
commands = []
while currentCommand != 'halt':
    currentCommand = input()
    if len(currentCommand.split()) > 1:
        currentCommand, repetition = currentCommand.split()   
    if currentCommand == 'process' and commands != []:
        commands = process(commands)
    elif currentCommand == 'add':
        subcommands = []
        for _ in range(int(repetition)):
            subcommands.append(input().split(' ', 1))
        commands.append(subcommands)
    elif currentCommand == 'halt':
        halt(commands)









