# If you use PyMySQL as a fallback, this makes it available as MySQLdb
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except Exception:
    # PyMySQL not installed; if you use mysqlclient this is fine
    pass
