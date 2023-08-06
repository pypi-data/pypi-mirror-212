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

from dataclasses import dataclass
from typing import Optional

from . import value_objects as vo
from .exceptions import IncorrectValue


@dataclass
class Book:
    isbn: vo.Isbn
    title: vo.Title
    year: vo.Year
    authors: list[vo.Author]
    genres: list[vo.Genre]
    cover: Optional[vo.Cover] = None

    @classmethod
    def instanciate(
        cls,
        isbn: vo.Isbn,
        title: vo.Title,
        year: vo.Year,
        authors: list[vo.Author],
        genres: list[vo.Genre],
        cover: Optional[vo.Cover] = None,
    ) -> "Book":
        if not authors:
            raise IncorrectValue("authors", "A book must have at least one author!")
        return Book(isbn, title, year, authors, genres, cover)
