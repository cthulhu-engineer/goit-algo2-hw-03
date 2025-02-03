from BTrees.OOBTree import OOBTree
import csv
import timeit

tree = OOBTree()
correct_tree = OOBTree()
item_dict = {}

def add_item_to_tree(tree):
    with open('generated_items_data.csv', mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        next(csv_reader, None)  # Пропускаємо заголовки
        for row in csv_reader:
            item_id, name, category, price = row[0], row[1], row[2], float(row[3])
            tree[item_id] = {'Name': name, 'Category': category, 'Price': price}

# Додавання об'єктів у дерево з ключами, що відповідають ціні
def add_item_to_correct_tree(tree):
    with open('generated_items_data.csv', mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        next(csv_reader, None)
        for row in csv_reader:
            price, name, category, item_id = float(row[3]), row[1], row[2], row[0]
            tree.setdefault(price, []).append({'Name': name, 'Category': category, 'ID': item_id})

def add_item_to_dict(item_dict):
    with open('generated_items_data.csv', mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        next(csv_reader, None)
        for row in csv_reader:
            item_id, name, category, price = row[0], row[1], row[2], float(row[3])
            item_dict[item_id] = {'Name': name, 'Category': category, 'Price': price}

add_item_to_tree(tree)
add_item_to_correct_tree(correct_tree)
add_item_to_dict(item_dict)

def range_query_tree(tree, min_price, max_price):
    return [(key, value) for key, value in tree.items() if min_price <= value['Price'] <= max_price]

def range_query_correct_tree(tree, min_price, max_price):
    return [(key, value) for key, value in tree.items(min_price, max_price)]

def range_query_dict(item_dict, min_price, max_price):
    return [(key, value) for key, value in item_dict.items() if min_price <= value['Price'] <= max_price]

def compare_time(min_price, max_price):
    tree_time = timeit.timeit(lambda: range_query_tree(tree, min_price, max_price), number=100)
    correct_tree_time = timeit.timeit(lambda: range_query_correct_tree(correct_tree, min_price, max_price), number=100)
    dict_time = timeit.timeit(lambda: range_query_dict(item_dict, min_price, max_price), number=100)

    print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds")
    print(f"Total range_query time for Optimized OOBTree: {correct_tree_time:.6f} seconds")
    print(f"Total range_query time for Dict: {dict_time:.6f} seconds")

min_price = 100
max_price = 500

compare_time(min_price, max_price)
