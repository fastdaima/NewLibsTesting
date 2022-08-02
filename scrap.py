def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            print(f'creating new instance: {len(instances)}')
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return get_instance


@singleton
class A:
    def __init__(self, value):
        self.connection = value

    def __enter__(self):
        print(f'in enter for {self.connection}')

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f'in exit for {self.connection}')


def find():
    data = [1, 1, 3, 2, 4]
    for val in data:
        print(val)
        print("******8")
        value = A(val)
        print(value.connection)


if __name__ == '__main__':
    find()