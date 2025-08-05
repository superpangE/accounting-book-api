from repositories.accounting_book_repository import AccountingBookRepository

class AccountingBookService:
    def __init__(self):
        self.repository = AccountingBookRepository()

    def create_entry(self, data):
        return self.repository.create(data)

    def get_entry(self, id):
        return self.repository.get_by_id(id)

    def update_entry(self, id, data):
        entry = self.repository.get_by_id(id)
        if not entry:
            return None
        return self.repository.update(entry, data)

    def delete_entry(self, id):
        entry = self.repository.get_by_id(id)
        if not entry:
            return False
        self.repository.delete(entry)
        return True

    def list_entries(self, start_date=None, end_date=None):
        return self.repository.get_all(start_date, end_date)
