import re

VOID_TAGS = ["area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"]


def lexer(html_raw):
    tokens = re.findall("(<[^>]+>)", html_raw.lower())
    print(tokens)
    return tokens


def parse_validate(tokens):
    stack = []
    for token in tokens:
        print(f"Stack: {stack}")
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

            if tag_name_start is not None:
                stack.append(tag_name_start)
            
            elif tag_name_end is not None:
                last_start_tag = stack.pop()

                if tag_name_end != last_start_tag:
                    print(f"The tag_name_end: {tag_name_end} not equal to the last start tag: {last_start_tag}")
                    return False
            else:
                print("Neither a start or end ta (or a void or single tag)g, fail.")
                return False            

    if len(stack) != 0:
        print(f"Stack was not empty after checking each token: {stack}")
        return False

    return True



eg1='''<HTML><img src="test">abc<img  src="a" src='a' a=b></html>'''
assert parse_validate(lexer(eg1)) == True, "Multiple void tags with attributes. Should validate."

print()
eg2='<tag>I love coding <Component />!</tag>'
assert parse_validate(lexer(eg2)) == True, "Single tag. Should validate."

print()
eg2='<HTML>I love coding <TABLE>happy fail</HTML>'
assert parse_validate(lexer(eg2)) == False,  "Unpaired table tag should fail."

print()
eg3='<HTML>I love coding <broken_tag happy fail</HTML>'
assert parse_validate(lexer(eg3)) == False,  "Half tag with only <, should fail."

print()
eg4='<html>Some stuff<TABLE></TABLE> stuff</HTML>'
assert parse_validate(lexer(eg4)) == True,  "Paired tags, should Validate."

print()
eg5='<html>Some stuff<TABLE></TABLE><BR><SPAN>Hello</SPAN> stuff</HTML>'
assert parse_validate(lexer(eg4)) == True,  "Multiple paired tags and void tag, should Validate."
