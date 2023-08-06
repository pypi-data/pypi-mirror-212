from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
import datetime, decimal

class xlh(object):
    def to_dict(self):
        # return {c.name: getattr(self, c.name) for c in self.__table__.columns}
        d = dict()
        for c in self.__table__.columns:
            v = getattr(self, c.name)
            new_v = (isinstance(v, (datetime.datetime, decimal.Decimal)) and str(v)) or v
            d.update({c.name: new_v})
        return d

class PytestOrm(xlh):
    def __init__(self, engine):
        if engine:
            engine = create_engine(engine)
            self.session = sessionmaker(bind=engine)()
            self.__base = automap_base()
            self.__base.prepare(autoload_with=engine)

    def model(self, table_name):
        try:
            self.__base
        except Exception as e:
            raise ValueError('ORM Connection timed out: Connect failed')
        Model = getattr(self.__base.classes, table_name)
        Model.to_dict = xlh.to_dict
        return Model

    def query(self, *args):
        return self.session.query(*args)