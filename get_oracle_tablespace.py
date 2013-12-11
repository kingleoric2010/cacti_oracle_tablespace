#!/usr/bin/env python2
# -* encoding:utf-8 *-

import cx_Oracle
import sys

try:
    username = sys.argv[1]
    password = sys.argv[2]

    host = sys.argv[3]
    port = sys.argv[4]
    inst = sys.argv[5]

    tbn = "%s:%s/%s" % (host, port, inst)

    con = cx_Oracle.connect(username, password, tbn)
    cur = con.cursor()
    cur.execute("""
SELECT 
	"TABLESPACE_NAME", 
	"ALLOCATED", 
	"USED", 
	"FREE", 
	"DATAFILES" 
FROM(
	SELECT 
		a.tablespace_name,
		c.bytes allocated,
		round(c.bytes - nvl(b.bytes,0), 2) used,
		round(nvl(b.bytes,0), 2) free,
		c.datafiles
	FROM
		dba_tablespaces a,
		( 
			SELECT 
				tablespace_name, 
				SUM(bytes) bytes 
			FROM 
				dba_free_space 
			GROUP BY 
				tablespace_name 
		) b,
		( 
			select
				count(1) datafiles,
				SUM(bytes) bytes,
				tablespace_name
			from 
				dba_data_files 
			GROUP BY tablespace_name
		) c
	WHERE 
		b.tablespace_name (+) = a.tablespace_name
	AND 
		c.tablespace_name (+) = a.tablespace_name
)
WHERE
	"TABLESPACE_NAME" NOT LIKE 'TEMP%'
ORDER BY
	"TABLESPACE_NAME"
""")
    result = cur.fetchall()

    cur.close()
    con.close()
    i = 1
    for content in result:
        if sys.argv[6] == 'index':
            print i
        elif sys.argv[6] == 'query':
            if sys.argv[7] == 'index':
                cont = i
            elif sys.argv[7] == 'tabname':
                cont = content[0]
            elif sys.argv[7] == 'total':
                cont = content[1]
            elif sys.argv[7] == 'used':
                cont = content[2]
	    else:
		raise IndexError

            print "%s!%s" % (i, cont)
        elif sys.argv[6] == 'get':
            index = int(sys.argv[8]) - 1
            if sys.argv[7] == 'total':
                print result[index][1]
                break
            elif sys.argv[7] == 'used':
                print result[index][2]
                break
            elif sys.argv[7] == 'tabname':
                print result[index][0]
                break
            elif sys.argv[7] == 'index':
                print index + 1
                break
            else:
		raise IndexError
        i += 1

except IndexError:
    print "Usage: %s username password host port instance_name operation..." % sys.argv[0]
