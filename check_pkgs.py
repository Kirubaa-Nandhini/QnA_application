try:
    import markdown2
    print("markdown2 exists")
except ImportError:
    print("markdown2 missing")
try:
    import markdown
    print("markdown exists")
except ImportError:
    print("markdown missing")
