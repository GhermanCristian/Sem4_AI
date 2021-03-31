from GUI import GUI
from service import Service


def main():
    service = Service()
    ui = GUI(service)
    ui.start()


if __name__ == "__main__":
    main()
