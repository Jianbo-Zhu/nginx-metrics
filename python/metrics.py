# coding: utf-8
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Metrics(Base):
    __tablename__ = 'metrics'
    id = Column(Integer, primary_key=True)
    collect_tms = Column(String(50))
    cache_item_count = Column(String(20))
    cache_item_size = Column(String(20))
    items_bytype = Column(String(500))
    hit_bytes = Column(String(20))
    hit_requests = Column(String(20))
    miss_bytes = Column(String(20))
    miss_requests = Column(String(20))
    total_bytes = Column(String(20))
    total_requests = Column(String(20))
