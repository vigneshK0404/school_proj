from PyPDF2 import PdfReader



def visitor_body(text, cm, tm, font_dict, font_size):
    print(f"text : {text}")
    print(f"cm : {cm}")
    print(f"tm : {tm}")
    y = tm[5]
    parts = []
    #if 50 < y < 720 or y == 0:
    parts.append(text)

    return parts


reader = PdfReader("statement.pdf")
page = reader.pages[2]
parts = page.extract_text(visitor_text=visitor_body)
#print(parts)
