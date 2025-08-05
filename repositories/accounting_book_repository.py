from config.database import db
from models.accounting_book import AccountingBook
from datetime import date

class AccountingBookRepository:
    def create(self, data):
        new_entry = AccountingBook(
            card=data['card'],
            date=date.fromisoformat(data['date']),
            amount=data['amount'],
            detail=data['description'],
            category=data['category'],
            person=data['person'],
            is_send=data.get('is_send', False)
        )
        db.session.add(new_entry)
        db.session.commit()
        return new_entry

    def get_by_id(self, id):
        return AccountingBook.query.get(id)

    def update(self, entry, data):
        entry.is_send = data.get('is_send', entry.is_send)
        db.session.commit()
        return entry

    def delete(self, entry):
        db.session.delete(entry)
        db.session.commit()

    def get_all(self, start_date=None, end_date=None):
        query = AccountingBook.query
        if start_date:
            query = query.filter(AccountingBook.date >= date.fromisoformat(start_date))
        if end_date:
            query = query.filter(AccountingBook.date <= date.fromisoformat(end_date))
        return query.all()
