from sqlalchemy import create_engine, text
import pymysql

db_connection_string = "mysql+pymysql://n4ugv3ja4obdcl3qrlz0:pscale_pw_O35f0Iq23vdSnbNNEfVNsJoaWzra101puQ8Aql92JgN@aws.connect.psdb.cloud:3306/tiqkets?charset=utf8mb4"

engine = create_engine(db_connection_string,
                       connect_args={
                           "ssl": {
                               "ssl_ca": "/etc/ssl/cert.pem"
                           }
                       })
print ("connected again")

with engine.connect() as conn:
  result = conn.execute(text('SELECT * FROM user'))
  user = result.all()
  print (user)
 