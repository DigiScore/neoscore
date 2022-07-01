# 0.1.2 (unreleased)
- Support disabling automatic viewport interaction with `neoscore.show(auto_viewport_interaction_enabled=False)`. This disables scroll-zooming, drag-moving, and the appearance of window scrollbars.
- Support setting the preview window size with new `neoscore.show()` options `min_window_size` and `max_window_size`.
- Support launching the preview window in fullscreen mode with `neoscore.show(fullscreen=True)`.

# 0.1.1 (2022-05-20)

- [Fixed PDF export on Windows](https://github.com/DigiScore/neoscore/issues/37)
- Updated `neoscore.render_image()` to block by default. Set the new kwarg `wait=False` to finalize export asynchronously.
- Fixed bug where image and PDF export exceptions could be ignored. Exceptions in image export threads now propagate on join via the new `PropagatingThread` class.

# 0.1.0 (2020-05-15)

Initial release! ❤️❤️❤️
