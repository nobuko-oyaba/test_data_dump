import pyodbc
from tabulate import tabulate
import textwrap
import numpy as np

# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port

def dump_query_data_tenchi(f,cur, t_name, query):
	cur.execute(query) 
	header = ['column_name','column_value']
	columns = [column[0] for column in cur.description]
	rows = [(column, textwrap.shorten(str(row), width=600, placeholder="...")) for column, row in zip(columns, cur.fetchone())]
	title = '■'+t_name
	print(title)
	print(title, file=f)
	result=tabulate(rows, header, tablefmt="simple", colalign=('right', 'left'))
	print(result)
	print(result, file=f)
	print(' \n')


def dump_query_data(f,cur, t_name, query):
	cur.execute(query) 
	columns = [column[0] for column in cur.description]
	rows = cur.fetchall()
	title = '■'+t_name
	print(title)
	print(title, file=f)
	result=tabulate(rows, columns, tablefmt="grid")
	print(result)
	print(result, file=f)
	print(' \n')

def dump_query_data_danwake(f,cur, t_name, query,wakerukazu=8):
	cur.execute(query) 
	columns_all = [column[0] for column in cur.description]
	rows_all = cur.fetchall()
	
	num_ally = np.array(rows_all)
	
	page_all = int(len(columns_all)/wakerukazu)
	page_all = page_all if len(columns_all)%wakerukazu==0 else (page_all+1)
	page = 1
	for m in range(0,len(columns_all),wakerukazu):
		end = m+wakerukazu if m+wakerukazu<len(columns_all) else len(columns_all)-1
		title = '■'+t_name+' ページ('+str(page)+' / '+str(page_all)+') 表示列('+str(m+1)+'～'+str(end)+'列目)'
		print(title)
		print(title, file=f)
		columns = columns_all[m:end]
		rows = num_ally[:, range(m,end)]
		result=tabulate(rows, columns, tablefmt="grid")
		print(result)
		print(result, file=f)
		print(' \n')
		page+=1
	print(' \n')

#code sample
def contract_renew_kaito(f, cur):
	dump_query_data(f, cur,"test title_name", "select * from test_table where id in (1101,1102,1103,1104,1105)");
	dump_query_data_danwake(f, cur,"test title_name", "select * from test_table where id in (1101,1102,1103,1104,1105)", 10);


server = '***.***.***.***' 
database = '*****' 
username = '***' 
password = '*****' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
with open("file.txt", "w", encoding='UTF-8') as f:
	contract_renew_kaito(f, cursor)
cnxn.close()
