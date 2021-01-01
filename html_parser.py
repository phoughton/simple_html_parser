import re

VOID_TAGS = ["area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"]

stack = []

def lexer(html_raw):
    tokens = re.findall("(<[^>]+>)", html_raw.lower())
    return tokens


def parse_validate(tokens):
    for token in tokens:
        tag_name_start = re.match("<([A-z]+)", token)
        if tag_name_start is not None:
            tag_name_start = tag_name_start.group(1)
        tag_name_end = re.match("</([A-z]+)", token)
        if tag_name_end is not None:
            tag_name_end = tag_name_end.group(1)

        tag_name_single = (tag_name_start in VOID_TAGS)
        tag_self_closing = token.endswith("/>")

        print(f"Token: {token}, tag_name_start: {tag_name_start}, \
            tag_name_end: {tag_name_end}, tag_name_single: {tag_name_single}, \
            tag_self_closing: {tag_self_closing}")
        if tag_name_start is None and tag_name_end is None:
            print("Invalid tag: not start or end syntax")
            return False

        if not tag_name_single and not tag_self_closing:
            if tag_name_start is not None and not tag_name_single and not tag_self_closing:
                stack.append(tag_name_start)
            elif tag_name_end is not None:
                last_tag = stack.pop()
                if tag_name_end != last_tag:
                    print(f"tag_name_end: {tag_name_end} not equal to: {last_tag}")
                    return False
            else:
                raise "neither a start or end tag, fail."            

    if len(stack) != 0:
        print(f"Stack was not empty: {stack}")
        return False

    return True


eg1='''<HTML><img src="test">abc<img  src="a" src='a' a=b></html>'''
print(parse_validate(lexer(eg1)))

print()
eg2='<tag>I love coding <Component />!</tag>'
print(parse_validate(lexer(eg2)))

print()
eg2='<HTML>I love coding <TABLE>happy fail</HTML>'
print(parse_validate(lexer(eg2)))
