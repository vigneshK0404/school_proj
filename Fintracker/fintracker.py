from PyPDF2 import PdfReader

def boa_process(parts):
    startidx = parts.index("Purchases and Adjustments")
    endidx = parts.index("TOTAL PURCHASES AND ADJUSTMENTS FOR THIS PERIOD")

    dates = []
    prices = []
    transactions = []  

    for text in parts[startidx+1:endidx]:
        if text.strip() == "":
            continue

        texts = text.split()
        dates.append(texts[0])
        prices.append(float(texts[-1]))
        transactions.append(" ".join(a for a in texts[2:-3]))

    return dates, transactions, prices

def discover_process(parts): 

    print(parts)

    refined = []

    for i in range(len(parts)):
        x = parts[i].strip()
        if x == "":
            continue

        refined.append(x)
        
    startidx = refined.index("Category")
    endidx = -11

    refined = refined[startidx+1:endidx]
    #print(refined)

    dates = refined[::6]
    prices = refined[1::6]
    transactions = refined[2::6]

    return dates,transactions,prices



parts = []

def visitor_body(text, cm, tm, font_dict, font_size):
    parts.append(text.rstrip())

reader = PdfReader("Discover_statement.pdf")
page = reader.pages[0]
page.extract_text(visitor_text=visitor_body)

page = reader.pages[1]
page.extract_text(visitor_text=visitor_body)

dates,transactions,prices = discover_process(parts)

#print(dates)
#print(transactions)
#print(prices)
    

