from lxml import etree

def parse_invoice(xml_string):
    # FIXED: Disable entity resolution to prevent XXE
    parser = etree.XMLParser(resolve_entities=False)
    root = etree.fromstring(xml_string, parser=parser)
    
    return root.find("total").text

def xml_to_json(xml_str):
    root = etree.fromstring(xml_str)
    return etree_to_dict(root)

def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = {}
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                if k in dd:
                    if not isinstance(dd[k], list):
                        dd[k] = [dd[k]]
                    dd[k].append(v)
                else:
                    dd[k] = v
        d = {t.tag: dd}
    if t.attrib:
        d[t.tag].update(('@' + k, v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d