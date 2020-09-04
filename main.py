import requests
import pandas as pd
from bs4 import BeautifulSoup

class HTMLTableParser:
    
    def parse_url(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        return [(table,self.parse_html_table(table))\
                for table in soup.find_all('table')]  

    def parse_html_table(self, table):
        n_columns = 0
        n_rows=0
        column_names = []

        # Find number of rows and columns
        # we also find the column titles if we can
        for row in table.find_all('tr'):
            
            # Determine the number of rows in the table
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows+=1
                if n_columns == 0:
                    # Set the number of columns for our table
                    n_columns = len(td_tags)
                    
            # Handle column names if we find them
            th_tags = row.find_all('th') 
            if len(th_tags) > 0 and len(column_names) == 0:
                for th in th_tags:
                    column_names.append(th.get_text())

        # Safeguard on Column Titles
        if len(column_names) > 0 and len(column_names) != n_columns:
            raise Exception("Column titles do not match the number of columns")

        columns = column_names if len(column_names) > 0 else range(0,n_columns)
        df = pd.DataFrame(columns = columns,
                          index= range(0,n_rows))
        row_marker = 0
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            for column in columns:
                df.iat[row_marker,column_marker] = column.get_text()
                column_marker += 1
            if len(columns) > 0:
                row_marker += 1
                
        # Convert to float if possible
        for col in df:
            try:
                df[col] = df[col].astype(float)
            except ValueError:
                pass
        """
        """
        return df

url = 'https://banco.santanderrio.com.ar/exec/cotizacion/index.jsp'
#url = 'https://www.cbc.uba.ar/materias_segun_carrera.html'
hp = HTMLTableParser()
table = hp.parse_url(url)[0][1] # Grabbing the table from the tuple
#table.head()
#print(type(table))


#print(table.to_json(orient="index", force_ascii=False, indent=4))

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"200": "Welcome To Heroku"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.get("/dolar")
def dolar():
    data = table.to_json(orient="index", indent=4)
    response = data
    return response



@app.get("/fizz_buzz/{num}")
def read_item2(num: int):
    # https: // ja.wikipedia.org / wiki / Fizz_Buzz
    if not num % 15:
        return {num: "Fizz Buzz"}
    elif not num % 5 or not num % 3:
        return {num: 'Fizz' if not num % 3 else 'Buzz'}
    else:
        return {num: 'Stay Silent'}
#C:/Users/Luca/AppData/Local/Microsoft/WindowsApps/python.exe -m pip install fastapi