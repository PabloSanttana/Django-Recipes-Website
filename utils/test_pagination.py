# usando unittest teste simples

from unittest import TestCase

from utils.pagination import make_pagination_range


class PaginationTest(TestCase):
    # testando o range da paginacao
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )

        self.assertEqual([1, 2, 3, 4], pagination["pagination"])

    def test_make_pagination_range_first_range_is_static_if_current_page_is_less_than_middle_page(self):  # noqa: E501
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )

        self.assertEqual([1, 2, 3, 4], pagination["pagination"])

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=2,
        )

        self.assertEqual([1, 2, 3, 4], pagination["pagination"])

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=3,
        )

        self.assertEqual([2, 3, 4, 5], pagination["pagination"])

    def test_make_pagination_range_sure_middle_ranges_are_correct(self):

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=10,
        )

        self.assertEqual([9, 10, 11, 12], pagination["pagination"])

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=16,
        )

        self.assertEqual([15, 16, 17, 18], pagination["pagination"])

    def test_make_pagination_range_static_paging_range_at_the_end(self):

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=18,
        )

        self.assertEqual([17, 18, 19, 20], pagination["pagination"])

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=19,
        )

        self.assertEqual([17, 18, 19, 20], pagination["pagination"])

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=20,
        )

        self.assertEqual([17, 18, 19, 20], pagination["pagination"])
