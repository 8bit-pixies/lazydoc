import argparse

def main():
    from lazydoc.lazydoc import generate, document
    parser = argparse.ArgumentParser(description='Generate Documents. `gen` for gnerating outline, `doc` for documents.')
    parser.add_argument('type')
    args = parser.parse_args()
    
    if args.type.startswith("doc"):
        document()
    elif args.type.startswith("gen"):
        generate()
    else:
        print("Please enter 'generate' or 'document'")
        raise
