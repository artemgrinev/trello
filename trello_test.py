import requests
import json
import sys


auth_params = {    
    'key': "bcda680e815b1edb071efbc7520a264c",    
    'token': "bdf01b18ec51d8b66d3c7d42e6dc6f6f88d5d4e73cb732a13a4c15e74f8f5a78", 
    }  
  
base_url = "https://api.trello.com/1/{}" 
board_id = "Eayrfcke"

def read():      
    # Получим данные всех колонок на доске:      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
      
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:      
    for column in column_data:      
        print(column['name'])    
        # Получим данные всех задач в колонке и перечислим все названия      
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()      
        if not task_data:      
            print('\t' + 'Нет задач!')      
            continue      
        for task in task_data:      
            print('\t' + task['name'])


def create(name, column_name):
	column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
	for column in column_data:
		if column['name'] == column_name:
			requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
		break


def move(name, column_name):
    # Получим данные всех колонок на доске    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
        
    # Среди всех колонок нужно найти задачу по имени и получить её id    
    task_id = None
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                task_id = task['id']
                break
        if task_id:
            break
       
    # Теперь, когда у нас есть id задачи, которую мы хотим переместить    
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу    
    for column in column_data:
        if column['name'] == column_name:
            # И выполним запрос к API для перемещения задачи в нужную колонку    
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})
            break
if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])