import mysql.connector
import config

class Database:
    def __init__(self):
        try:
            self.mydb = mysql.connector.connect(
                    host = config.db['host'],
                    user= config.db['user'],
                    passwd = config.db['passwd'],
                    database = config.db['database']
                )
        except mysql.connector.errors.ProgrammingError as e:
            print("error : "+str(e))
        
    def select_all(self, table):
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT * FROM "+table)
        columns = tuple( [d[0] for d in mycursor.description] )
        result = []
        myresult = mycursor.fetchall()
        for row in myresult:
            result.append(dict(zip(columns, row)))
        return result
    
    def select_where(self, table,*args):
        filtertable = ''
        for arg in args:
            filtertable = filtertable+arg+" "
        query = "SELECT * FROM "+table+" WHERE "+filtertable
        mycursor = self.mydb.cursor()
        mycursor.execute(query)
        columns = tuple( [d[0] for d in mycursor.description] )
        result = []
        myresult = mycursor.fetchall()
        for row in myresult:
            result.append(dict(zip(columns, row)))        
        return result

    def insert_into(self, table, column=('',''), values = [('','')]):
        try:
            if len(values[0]) != len(column):
                return 'Error'
            valuesescaped = []
            for i in range(len(column)):
                valuesescaped.append('%s')
            
            valuesescapedstring = ','.join(valuesescaped)
            valuesescapedstring = '('+valuesescapedstring+')'

            column_name = ','.join(column)
            column_name = '('+column_name+')'

            mycursor = self.mydb.cursor()
            sql = "INSERT INTO "+table+" "+column_name+" VALUES "+valuesescapedstring
            print("SQL EXECUTE: "+sql)
            mycursor.executemany(sql, values)
            self.mydb.commit()

            print(mycursor.rowcount, "Berhasil diinsert.")
        except Exception as err:
            print("NO INSERT : "+str(err))

    #check apakah udah ada di db belum, not tested
    def is_exists(self, table, col_name, value, col_name2=None, value2=None):
        try:
            val2 = str(value2)
            andwhere = "AND "+col_name2+" = '"+val2+"'"
            if val2 == 'None':
                andwhere = "AND "+col_name2+" is NULL"
            query = "SELECT "+col_name+" FROM "+table+" WHERE "+col_name+"='"+value+"'"+andwhere
            mycursor = self.mydb.cursor()
            print("SQL EXECUTE : "+str(query))
            mycursor.execute(query)
            row = mycursor.fetchone()  
            # check if it is empty and print error
            
            if not row:
                print("It does not exist")
                return False
            else:
                print("Row Exist")
                return True
        except Exception as err:
            print("Error is_exists: "+str(err))

    def update_where(self, table, col_name, value, condition_col, condition_val):
        try:
            query = "UPDATE "+table+" SET "+col_name+" = "+value+" WHERE "+ condition_col+" = "+condition_val
            mycursor = self.mydb.cursor()
            print("SQL EXECUTE : "+str(query))
            mycursor.execute(query)
            self.mydb.commit()
            print(mycursor.rowcount, "record(s) affected")
        except Exception as err:
            print("Error update_where: "+str(err))
