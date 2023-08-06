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


class Presenter(ABC):
    @abstractmethod
    def not_an_isbn(self, isbn: str) -> None:
        ...

    @abstractmethod
    def book_does_not_exist(self, isbn: vo.Isbn) -> None:
        ...

    @abstractmethod
    def see_other(self, isbn: vo.Isbn) -> None:
        ...

    @abstractmethod
    def book(self, book: e.Book) -> None:
        ...


@dataclass(frozen=True)
class Interactor:
    presenter: Presenter
    books: r.Books

    def execute(self, request: Request) -> None:
        try:
            isbn = vo.Isbn.instanciate(request.isbn)
        except ex.IncorrectValue:
            return self.presenter.not_an_isbn(request.isbn)

        if str(isbn) != request.isbn:
            return self.presenter.see_other(isbn)

        if book := self.books.by_isbn(isbn):
            return self.presenter.book(book)

        self.presenter.book_does_not_exist(isbn)
