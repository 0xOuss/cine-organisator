def input_err_handling(text, text_err, list_cho):
    try:
        cho=int(input(text))
        if cho not in list_cho:
            1/0    
    except:
        while True:
            try:
                cho=int(input(text_err))
                if cho in list_cho:
                    break
            except:
                pass
    return cho


def update_loading(varp, text):
    if varp<5:
        print(f"{text}\n\n| . . . . . . . . . . |     {varp:2.2f} %")
    elif varp<15:
        print(f"{text}\n\n| # . . . . . . . . . |     {varp:2.2f} %")
    elif varp<25:
        print(f"{text}\n\n| # # . . . . . . . . |     {varp:2.2f} %")
    elif varp<35:
        print(f"{text}\n\n| # # # . . . . . . . |     {varp:2.2f} %")
    elif varp<45:
        print(f"{text}\n\n| # # # # . . . . . . |     {varp:2.2f} %")
    elif varp<55:
        print(f"{text}\n\n| # # # # # . . . . . |     {varp:2.2f} %")
    elif varp<65:
        print(f"{text}\n\n| # # # # # # . . . . |     {varp:2.2f} %")
    elif varp<75:
        print(f"{text}\n\n| # # # # # # # . . . |     {varp:2.2f} %")
    elif varp<85:
        print(f"{text}\n\n| # # # # # # # # . . |     {varp:2.2f} %")
    elif varp<95:
        print(f"{text}\n\n| # # # # # # # # # . |     {varp:2.2f} %")
    else:
        print(f"{text}\n\n| # # # # # # # # # # |    {varp:3.2f} %")