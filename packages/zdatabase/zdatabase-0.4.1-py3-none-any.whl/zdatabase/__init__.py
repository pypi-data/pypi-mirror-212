from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class Database:
    def make_url(self, config, db_type):
        if db_type == 'postgre':
            url = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(**config)
        else:
            url = 'mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8mb4'.format(**config)
        return url

    def init(self, url):
        engine = create_engine(url)
        metadata = MetaData(bind=engine)
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.session = Session()
        return engine, metadata
 
 
Model = declarative_base()
db = Database()
