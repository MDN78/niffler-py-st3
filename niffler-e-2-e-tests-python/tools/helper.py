from databases.spend_db import SpendDb


def check_category_in_db(spend_db: SpendDb, category_id: str, expected_name: str, expected_username: str,
                         expected_archived: bool):
    category = spend_db.get_user_category(category_id)

    assert category is not None
    assert category.name == expected_name
    assert category.username == expected_username
    assert category.archived == expected_archived
