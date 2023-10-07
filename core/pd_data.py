import pandas as pd
from django.core.management.base import BaseCommand
from .models import Item
from sqlalchemy import create_engine


class ItemCommand(BaseCommand):
    help = "Command to add data from Excel file to the Item table"

    def handle(self, *args, **options):
        excel_file = ''
        df = pd.read(excel_file)

        engine = create_engine('sqlite://db.sqlite3')

        df.to_sql(Item.meta.db_table, if_exists='replace', con=engine, index=True)
