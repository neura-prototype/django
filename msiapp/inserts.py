import mysql.connector

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password",
    database = "NeuraData",
)

cur = conn.cursor()

sql = """CREATE VIEW vsumperiodvaluesday_django AS
    SELECT 
        SUM(`periodvalues`.`cFixed`) AS `FixedCost`,
        SUM(`periodvalues`.`cMaximum`) AS `MaximumDemandCost`,
        SUM(`periodvalues`.`cAcc`) AS `EnergyCost`,
        SUM(`periodvalues`.`uMaximum`) AS `MaximumDemand`,
        SUM(`periodvalues`.`uAcc`) AS `Energy`,
        DATE_FORMAT(`periodvalues`.`DateReceived`,
                '%Y/%m/%d') AS `DateOnly`,
        `periodvalues`.`Node` AS `Node`
    FROM
        `periodvalues`
    GROUP BY `periodvalues`.`Node` , DATE_FORMAT(`periodvalues`.`DateReceived`,
            '%Y/%m/%d')"""

try:
    cur.execute(sql)
    conn.commit()
except:
    conn.rollback()
cur.execute("SELECT * FROM vsumperiodvaluesday_django")

for x in cur:
    print(x)

cur.close()
conn.close()

