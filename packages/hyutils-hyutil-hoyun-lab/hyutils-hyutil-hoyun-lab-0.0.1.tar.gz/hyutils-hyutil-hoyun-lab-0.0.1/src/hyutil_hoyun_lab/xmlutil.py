def indent(elem, level=0):  # 자료 출처 https://goo.gl/J8VoDK
    i = "\n" + level * " " * 4
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + " " * 4
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i