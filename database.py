from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://l8mrfcq1wcbdgytn465l:pscale_pw_MD0rI4kaxu35VDQzMLmgLyjtNr4Jee78z7Kvwc4Rwe4@aws.connect.psdb.cloud/tiqkets?charset=utf8mb4")
print ("connected")

with engine.connect() as conn:
  