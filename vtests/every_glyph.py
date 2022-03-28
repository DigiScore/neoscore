#
# def test_glyph_info(self, full_test=True):
#     font = MusicFont("Bravura", Unit)
#     if full_test:
#         glyphCount = 0
#
#         # test each glyph in the glyphnamelist json
#         for testGlyph in smufl.glyph_names:
#
#             # test for every alt option between 1 - 3
#             for alt in range(4):
#                 if alt == 0:
#                     alt = None
#                 elif alt == 3:
#                     testGlyph = 'garbage'
#                 print(f'\n\t\t\t\t{testGlyph}, {alt}, {glyphCount}')
#                 test_info_dict = font._glyph_info(testGlyph, alt)
#                 print(test_info_dict)
#
#                 # if returns filled dict AND not an alterante glyph add to count
#                 if len(test_info_dict) > 0 and alt == None:
#                     glyphCount += 1
#
#         # tally up - should be the same value
#         print(f'total glyph count === {glyphCount}')
#         print(f'total glyph list name count === {len(smufl.glyph_names)}')
#
#     else:
#         # oneTestGlyph = "accidentalDoubleFlatParens" # ligature
#         # oneTestGlyph = '4stringTabClef' # normal glyph
#         # oneTestGlyph = '4stringTabClefSerif' # optional glyph
#         oneTestGlyph = 'gClef4Above'  # ligature
#         r = font._glyph_info(oneTestGlyph)
#         print(f'\nreturn dict == === == {r}')