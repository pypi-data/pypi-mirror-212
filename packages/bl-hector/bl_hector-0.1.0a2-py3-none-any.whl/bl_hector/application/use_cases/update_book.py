# Hector --- A collection manager.
# Copyright © 2023 Bioneland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from abc import ABC, abstractmethod
from dataclasses import dataclass

from bl_hector.domain.collection_management import entities as e
from bl_hector.domain.collection_management import exceptions as ex
from bl_hector.domain.collection_management import repositories as r
from bl_hector.domain.collection_management import value_objects as vo


@dataclass
class Request:
    isbn: str
    title: str
    year: int
    authors: list[str]
    genres: list[str]
    cover: str = ""


class Presenter(ABC):
    @abstractmethod
    def bad_request(self) -> None:
        ...

    @abstractmethod
    def book_does_not_exist(self, isbn: vo.Isbn) -> None:
        ...

    @abstractmethod
    def book_updated(self, book: e.Book) -> None:
        ...


@dataclass(frozen=True)
class Interactor:
    presenter: Presenter
    books: r.Books

    def execute(self, request: Request) -> None:
        try:
            # There's no business logic to apply when updating a book.
            book = e.Book.instanciate(
                vo.Isbn.instanciate(request.isbn),
                vo.Title.instanciate(request.title),
                vo.Year.instanciate(request.year),
                [vo.Author.instanciate(a) for a in request.authors if a],
                [vo.Genre.instanciate(g) for g in request.genres if g],
                vo.Cover.instanciate(request.cover) if request.cover else None,
            )
        except ex.IncorrectValue:
            return self.presenter.bad_request()

        if not self.books.search(isbn=book.isbn):
            return self.presenter.book_does_not_exist(book.isbn)

        self.books.update(book)
        self.presenter.book_updated(book)
