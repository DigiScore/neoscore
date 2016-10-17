import unittest

from brown.document import Document
from brown.flowable import Flowable
from brown.point_unit import PointUnit
from brown.page import Page
from brown.paper import Paper
from PySide.QtGui import QGraphicsScene, QApplication
import sys


class FlowableTest(unittest.TestCase):

    def setUp(self):
        try:
            self.app = QApplication(sys.argv)
        except:
            pass
        self.scene = QGraphicsScene()
        self.document = Document(Paper(612, 792, 72, 72, 72, 72), self.scene)
        self.document.append_new_page_from_last()

    # def tearDown(self):
    #     self.app.quit()

    def test_single_page_wrapping_starting_from_page_corner(self):
        first_page = self.document.page_list[0]
        flowable = Flowable(self.document, first_page.left_margin_pos, first_page.top_margin_pos, 1600, 72)
        flowable.auto_build_sections()
        self.assertEqual(len(flowable.section_list), 4)

    def test_single_page_wrapping_starting_from_page_middle(self):
        # Start the flowable near the end of the line
        first_page = self.document.page_list[0]
        flowable = Flowable(self.document, first_page.right_margin_pos - PointUnit(68),
                            first_page.top_margin_pos, 1900, 72)
        flowable.auto_build_sections()
        self.assertEqual(len(flowable.section_list), 5)
    #
    def test_page_auto_adding_starting_from_page_corner(self):
        first_page = self.document.page_list[0]
        flowable = Flowable(self.document, first_page.left_margin_pos, first_page.top_margin_pos, 4136, 72)
        flowable.auto_build_sections()
        self.assertEqual(len(flowable.section_list), 9)
    #
    def test_multi_page_line_break_count_starting_from_page_corner(self):
        first_page = self.document.page_list[0]
        flowable = Flowable(self.document, first_page.left_margin_pos, first_page.top_margin_pos, 4136, 72)
        flowable.auto_build_sections()
        self.assertEqual(len(flowable.section_list), 9)

    def test_page_auto_adding_several_pages_starting_from_page_corner(self):
        first_page = self.document.page_list[0]
        flowable = Flowable(self.document, first_page.left_margin_pos, first_page.top_margin_pos, 41360, 72)
        flowable.auto_build_sections()
        self.assertEqual(len(flowable.section_list), 89)
    #
    def test_line_start_pos_y_values_repeat_across_pages(self):
        first_page = self.document.page_list[0]
        flowable = Flowable(self.document, first_page.left_margin_pos, first_page.top_margin_pos, 8400, 72)
        flowable.auto_build_sections()
        line_start_pos_y_list = [section.y_scene_space_pos.value for section in flowable.section_list]
        self.assertEqual(line_start_pos_y_list, [72, 180, 288, 396, 504, 612] * 3)

    def test_scene_space_coord_of_flowable_space_coord(self):
        pass

    # TODO: Test varying page types
    # def test_multi_page_wrapping_across_different_paper_types(self):
    #     pass


if __name__ == '__main__':
    unittest.main()
