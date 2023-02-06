# So that we can do from models import ... instead of from schemas.book import ...
from schemas.book import PlainBookSchema, QueryBookSchema, BookSchema, UpdateBookSchema
from schemas.author import PlainAuthorSchema, AuthorSchema, UpdateAuthorSchema
from schemas.work import PlainWorkSchema, WorkSchema, UpdateWorkSchema
from schemas.book_author import BookAndAuthorSchema
from schemas.book_work import BookAndWorkSchema
from schemas.user import UserSchema