from brown.utils.paper_templates import paper_templates


def test_paper_template_names_unique():
    upcase_keys = [k.upper() for k in paper_templates.keys()]
    assert len(upcase_keys) == len(set(upcase_keys))
