def per(a, b = "pass"):
    if b != "pass":
        try:
            return (a+b)*2
        except:
            return "FATAL ERROR"
    else:
        try:
            return a*4
        except:
            return "FATAL ERROR"

def ser(a, b = "pass"):
    if b != "pass":
        try:
            return a*b
        except:
            return "FATAL ERROR"
    else:
        try:
            return a*a
        except:
            return "FATAL ERROR"
