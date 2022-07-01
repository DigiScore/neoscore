# 0.1.2 (unreleased)
- Support disabling automatic viewport interaction with `neoscore.show(auto_viewport_interaction_enabled=False)`. This disables scroll-zooming, drag-moving, and the appearance of window scrollbars.
- Support setting the preview window size with `neoscore.show(window_size=(width, height))`

# 0.1.1 (2022-05-20)

- [Fixed PDF export on Windows](https://github.com/DigiScore/neoscore/issues/37)
- Updated `neoscore.render_image()` to block by default. Set the new kwarg `wait=False` to finalize export asynchronously.
- Fixed bug where image and PDF export exceptions could be ignored. Exceptions in image export threads now propagate on join via the new `PropagatingThread` class.

# 0.1.0 (2020-05-15)

Initial release! ❤️❤️❤️
