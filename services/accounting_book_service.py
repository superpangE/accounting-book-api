from repositories.accounting_book_repository import AccountingBookRepository

class AccountingBookService:
    def __init__(self):
        self.repository = AccountingBookRepository()

    def create_entry(self, user_id, data):
        return self.repository.create(user_id, data)

    def get_entry(self, user_id, id):
        return self.repository.get_by_id(user_id, id)

    def update_entry(self, user_id, id, data):
        entry = self.repository.get_by_id(user_id, id)
        if not entry:
            return None
        return self.repository.update(user_id, entry, data)

    def delete_entry(self, user_id, id):
        entry = self.repository.get_by_id(user_id, id)
        if not entry:
            return False
        self.repository.delete(user_id, entry)
        return True

    def list_entries(self, user_id, start_date=None, end_date=None):
        return self.repository.get_all(user_id, start_date, end_date)
