import csv

def update_tables(file_tables_csv, numbered_tables, areas):
    with open(file_tables_csv, 'r') as file:
        for line in csv.reader(file):
            numbered_tables[int(line[0])] = [item.strip() for item in line[1:]]  # {number: area, status}
            areas.add(line[1].strip())
    return numbered_tables, areas

def update_menu(file_menu_csv, menu):
    with open(file_menu_csv, 'r') as file:
        for line in csv.reader(file):
            menu[line[0]] = [item.strip() for item in line[1:]] # {food: [ingredients]}
    return menu

def update_storage(file_storage_csv, storage):
    with open(file_storage_csv, 'r') as file:
        for line in csv.reader(file):
            if line[0] not in storage:
                storage[line[0]] = int(line[1].strip())
            else:
                storage[line[0]] += int(line[1].strip())
    return storage

def tables_report(numbered_tables, areas):
    if numbered_tables == {}:
        return print("- restaurante sem mesas")
    for area in sorted(areas):
        print(f"area: {area}")
        if area not in [value[0] for value in list(numbered_tables.values())]:
            print(f"- area sem mesas")
        else:
            for number in sorted(numbered_tables):
                if numbered_tables[number][0] == area:
                    print(f"- mesa: {number}, status: {numbered_tables[number][1]}")

def menu_report(menu):
    if menu == {}:
        return print("- cardapio vazio")
    for item in sorted(menu):
        print(f"item: {item}")
        for ingredient in sorted(set(menu[item])):
            print(f"- {ingredient}: {menu[item].count(ingredient)}")

def storage_report(storage):
    if storage == {}:
        return print("- estoque vazio")
    for ingredient in sorted(storage):
        print(f"{ingredient}: {storage[ingredient]}")

def make_request(numbered_tables, menu, storage, each_table_requests, chronological_requests):
    table_number, item_requested = input().split(", ")
    table_number = int(table_number)
    if table_number not in numbered_tables:
        print(f"erro >> mesa {table_number} inexistente")
    elif numbered_tables[table_number][1] == "livre":
        print(f"erro >> mesa {table_number} desocupada")
    elif item_requested not in menu:
        print(f"erro >> item {item_requested} nao existe no cardapio")
    else:
        for ingredient in menu[item_requested]:
            try:
                if storage[ingredient] >= menu[item_requested].count(ingredient): 
                    enough_ingredients = True
            except:
                enough_ingredients = False
                break
        if not enough_ingredients:
            print(f"erro >> ingredientes insuficientes para produzir o item {item_requested}")
        else:
            print(f"sucesso >> pedido realizado: item {item_requested} para mesa {table_number}")
            for ingredient in menu[item_requested]:
                if storage[ingredient] == menu[item_requested].count(ingredient): 
                    del storage[ingredient]
                else:
                    storage[ingredient] -= menu[item_requested].count(ingredient)
            if table_number not in each_table_requests:
                each_table_requests[table_number] = [item_requested]
            else:
                each_table_requests[table_number].append(item_requested)
            chronological_requests.append([table_number,item_requested])
    return storage, each_table_requests, chronological_requests
        
def requests_report(each_table_requests):
    if each_table_requests == {}:
        return print("- nenhum pedido foi realizado")
    for number in sorted(each_table_requests):
        print(f"mesa: {number}")
        for request in sorted(each_table_requests[number]):
            print(f"- {request}")

def close_restaurant(chronological_requests):
    if chronological_requests == []:
        print("- historico vazio")
    else:
        count = 1
        for request in chronological_requests:
            print(f"{count}. mesa {request[0]} pediu {request[1]}")
            count += 1
    return print("=> restaurante fechado")
    

numbered_tables, areas, menu, storage, each_table_requests, chronological_requests = dict() , set(), dict(), dict(), dict(), list()
print("=> restaurante aberto")
instruction = "=> restaurante aberto"
while instruction != "+ fechar restaurante":
    instruction = input()
    if instruction == "+ atualizar mesas":
        numbered_tables, areas = update_tables(input(), numbered_tables, areas)
    elif instruction == "+ atualizar cardapio":
        menu = update_menu(input(), menu)
    elif instruction == "+ atualizar estoque":
        storage = update_storage(input(), storage)
    elif instruction == "+ relatorio mesas":
        tables_report(numbered_tables, areas)
    elif instruction == "+ relatorio cardapio":
        menu_report(menu)
    elif instruction == "+ relatorio estoque":
        storage_report(storage)
    elif instruction == "+ fazer pedido":
        storage, each_table_requests, chronological_requests = make_request(numbered_tables, menu, storage, each_table_requests, chronological_requests)
    elif instruction == "+ relatorio pedidos":
        requests_report(each_table_requests)
    elif instruction == "+ fechar restaurante":
        close_restaurant(chronological_requests)
    else:
        print("erro >> comando inexistente")




