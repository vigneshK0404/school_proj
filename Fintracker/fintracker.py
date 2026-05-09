from PyPDF2 import PdfReader


parts = []

def visitor_body(text, cm, tm, font_dict, font_size):
    parts.append(text.rstrip())       


reader = PdfReader("statement.pdf")
page = reader.pages[2]
page.extract_text(visitor_text=visitor_body)

startidx = parts.index("Purchases and Adjustments")
endidx = parts.index("TOTAL PURCHASES AND ADJUSTMENTS FOR THIS PERIOD")

dates = []
prices = []
transactions = []  

for text in parts[startidx+1:endidx]:
    if text.rstrip() == "":
        continue

    texts = text.split()
    dates.append(texts[0])
    prices.append(float(texts[-1]))
    transactions.append(" ".join(a for a in texts[2:-3]))


print(dates)
print(prices)
print(transactions)

    



