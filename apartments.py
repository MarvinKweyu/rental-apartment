import csv
import random  # randomize room selection


class Hostel(object):
    def __init__(
        self, name=None, apartment_type=None, room_type=None, internet_fee=None
    ):
        self.name = name
        self.apartment_type = apartment_type
        self.room_type = room_type
        self.internet_fee = internet_fee
        # variables from program
        self.apartments_available = 20  # available per type
        self.typeA_rooms = 2
        self.typeB_rooms = 3


    def recommend_room(self, room_type="single"):
        """
        Check number of occupants in room and recommend next available room
        """
        apartments_in_A = self.typeA_rooms * 20

        self.room_type = room_type

        if self.room_type == "master":
            self.monthly_rent = 500
        else:
            self.monthly_rent = 300

        self.room_number = random.randint(0, apartments_in_A)

    def calculate_rent(
        self, deposit=100, monthly_rent=500, semester=5, payment_plan="full",
    ):
        """
        payment opt: full/partial
        payment based on apartment:A=400, B500/300
        Default to calc rent for one semester
        """

        deposit = 100

        def based_on_room(percentage_of_rent=False):
            if self.apartment_type == "A":
                monthly_rent = 400
                if percentage_of_rent:
                    return 0.5 * (monthly_rent * semester) + deposit
                total = (5 * monthly_rent) + deposit
                return total
            else:  # chose B > monthly=500/300
                monthly_rent = 300
                if percentage_of_rent:
                    return 0.5 * (monthly_rent * semester) + deposit
                total = (5 * monthly_rent) + deposit
                return total

        if payment_plan == "partial":
            self.rent = based_on_room(percentage_of_rent=True)  # for partial
        # full payment
        else:
            self.rent = based_on_room()

        self.record_information()

    def record_information(self):
        """
        Record info in txt file
        """
        student_details = {
            "name": self.name,
            "apartment_type": self.apartment_type,
            "room_type": self.room_type,
            "room_number": self.room_number,
            "internet": self.internet_fee,
            "payable": self.rent,
        }

        with open("student_records.csv", mode="a+", newline="") as csv_file:
            fieldnames = [
                "name",
                "apartment_type",
                "room_type",
                "room_number",
                "internet",
                "payable",
            ]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writerow(student_details)

        print("Records updated\n")

    def checkout(self, months_stayed, rent_per_month):
        """
        Leave
        """

        rent = self.deposit + (months_stayed * rent_per_month)
        return rent

    def search(self, search_item):
        """
        Read storage field for records
        """

        with open("student_records.csv") as student_file:
            csv_reader = csv.reader(student_file, delimiter=",")
            line_count = 0

            for row in csv_reader:
                if search_item in row:
                    return row


def main():

    while True:
        print("Choose option:(1/2/3/4)")
        option = int(input("1.Register student \n2.Checkout\n3.Search\n4.Exit\n\n"))

        if option == 1:
            register()
        elif option == 2:
            student_checkout()
        elif option == 3:
            search_record()
        else:
            break
    return


def register():
    name = input("please enter your names:")
    apartment_type = input("please select an apartment you wish (A/B):\n").upper()
    internet_fee = input(
        "please select your internet subscription (1/2): \n1.50.00\n2.40.00\n"
    )

    if internet_fee == 1:
        internet_fee = 50
    else:
        internet_fee = 40

    hostel_client = Hostel(name, apartment_type, internet_fee)

    if apartment_type == "B":
        room_type = input("Room type: (master/single): \n")

        hostel_client.recommend_room(room_type)
    else:
        hostel_client.recommend_room()

    payment_plan = input(
        "Enter payment:(full/partial) \n1.partial(You will be required to pay 1/2 of initial rent)\n2.full\n"
    )

    hostel_client.calculate_rent(payment_plan)


def student_checkout():
    record_to_delete = input("Enter name:\n")
    months_stayed = input("Enter months stayed:\n")

    hostel_leave = Hostel()
    rent = hostel_leave.checkout(months_stayed)
    print(f"Amount payable: {rent}")


def search_record():
    search_term = input(
        "Enter student name, apartment_type, apartment_number or room_number: \n"
    )

    hostel_search = Hostel()
    details = hostel_search.search(search_term)
    print(f"{details}\n")
    return details


if __name__ == "__main__":
    main()
