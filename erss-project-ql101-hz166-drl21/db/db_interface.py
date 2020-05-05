import psycopg2
import code


def get_connection(host="127.0.0.1"):
    return psycopg2.connect(dbname="amazondb", user="postgres", host=host, port="5433", password="password")


conn = get_connection()


def adjust_inventory(whid, prodid, n):
    cur = conn.cursor()
    cur.execute("select * from wh_contents where whid = %s and productid = %s;", (whid, prodid))
    ret = cur.fetchone()
    if not ret:
        cur.execute("INSERT INTO wh_contents VALUES (%s,%s,0);", (whid, prodid))
        cnt =0
    else:
        cnt= ret[2]

    ncnt = cnt + n
    if ncnt == 0:
        cur.execute("DELETE FROM wh_contents where whid = %s and productid = %s;", (whid, prodid))
    elif ncnt > 0:
        cur.execute("UPDATE wh_contents set count = %s where whid=%s and productid = %s", (ncnt, whid, prodid))
    else:
        raise AssertionError(f"Invalid value for new count: {ncnt}")


    conn.commit()

if __name__ == "__main__":
    adjust_inventory(1, 2, -5)
