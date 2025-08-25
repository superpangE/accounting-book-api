from config.database import db
from models.accounting_book import AccountingBook
from datetime import date

class AccountingBookRepository:
    def create(self, user_id, data):
        new_entry = AccountingBook(
            user_id=user_id,
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

    def get_by_id(self, user_id, id):
        return AccountingBook.query.filter_by(user_id=user_id, id=id).first()

    def update(self, user_id, entry, data):
        # Ensure the entry belongs to the user before updating
        if entry.user_id != user_id:
            return None # Or raise an exception for unauthorized access
        if 'person' in data:
            entry.person = data['person']
        if 'category' in data:
            entry.category = data['category']
        if 'is_send' in data:
            entry.is_send = data['is_send']
        db.session.commit()
        return entry

    def delete(self, user_id, entry):
        # Ensure the entry belongs to the user before deleting
        if entry.user_id != user_id:
            return False # Or raise an exception for unauthorized access
        db.session.delete(entry)
        db.session.commit()

    def get_all(self, user_id, start_date=None, end_date=None):
        query = AccountingBook.query.filter_by(user_id=user_id)
        if start_date:
            query = query.filter(AccountingBook.date >= date.fromisoformat(start_date))
        if end_date:
            query = query.filter(AccountingBook.date <= date.fromisoformat(end_date))
        return query.all()
