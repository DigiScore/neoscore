# 0.1.4 (2022-07-17)
- Fix bug where chordrest flags were not properly reset when rebuilding chords after mutations
- Added built-in support for mouse event handlers with `neoscore.set_mouse_event_handler`.
- Added built-in support for keyboard event handlers with `neoscore.set_key_event_handler`.

# 0.1.3 (2022-07-07)
- Reduce minimum Python version to 3.7
- Fix bug where arrowkeys still scrolled the viewport with `neoscore.show(auto_viewport_interaction_enabled=False)`


# 0.1.2 (2022-07-02)
- Support disabling automatic viewport interaction with `neoscore.show(auto_viewport_interaction_enabled=False)`. This disables scroll-zooming, drag-moving, and the appearance of window scrollbars.
- Support setting the preview window size with new `neoscore.show()` options `min_window_size` and `max_window_size`.
- Support launching the preview window in fullscreen mode with `neoscore.show(fullscreen=True)`.
- Support programmatically controlling the viewport's center position, scale (zoom), and rotation with `neoscore.set_viewport_center_pos()`, `neoscore.set_viewport_scale()`, and `neoscore.set_viewport_rotation()`. Corresponding getters are also provided.

# 0.1.1 (2022-05-20)

- [Fixed PDF export on Windows](https://github.com/DigiScore/neoscore/issues/37)
- Updated `neoscore.render_image()` to block by default. Set the new kwarg `wait=False` to finalize export asynchronously.
- Fixed bug where image and PDF export exceptions could be ignored. Exceptions in image export threads now propagate on join via the new `PropagatingThread` class.

# 0.1.0 (2020-05-15)

Initial release! ❤️❤️❤️
