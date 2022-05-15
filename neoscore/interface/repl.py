def running_in_ipython_gui_repl() -> bool:
    """Check if we are running inside an IPython REPL with the config gui=qt5.

    That config can be set either with ``ipython --gui=qt5 [-i script.py]``
    or by running the IPython magic command ``%gui qt5``.
    """
    try:
        import IPython  # type: ignore

        # None if not running within ipython
        ipython = IPython.get_ipython()
        if ipython:
            if ipython.config["TerminalIPythonApp"]["gui"] == "qt5":
                return True
    except:  # noqa
        pass
    return False
