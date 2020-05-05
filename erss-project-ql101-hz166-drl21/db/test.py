import psycopg2
import code

if __name__ == "__main__":
    conn = psycopg2.connect(dbname="amazondb", user = "postgres", host="127.0.0.1", port= "5433",password="password")
    cur = conn.cursor()
    cur.execute("select * from products;")
    print(cur.fetchall())
    code.interact(local=locals())
    
