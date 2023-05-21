from ProductFactory import ProductFactory


def main():
    factory = ProductFactory()
    factory.collect_all_products()


if "__main__" == __name__:
    main()
