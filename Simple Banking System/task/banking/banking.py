# Write your code here
import random
import sqlite3

card_database = {}
terminate = False
conn = sqlite3.connect('card.s3db')

cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS card(
    id INTEGER PRIMARY KEY,
    number text,
    pin text,
    balance INTEGER DEFAULT 0);''')
# Commit command
# conn.commit()

# Close connection
# conn.close()


class Bank:
    bank_bal = 0

    def __init__(self, pin, card_num):
        self.pin = pin
        self.card_num = card_num

    def show_bank(self):
        print("Your card number:")
        print(self.card_num)
        print("Your card PIN:")
        print(self.pin)
        pass

    def access(self):
        global terminate
        print("1. Balance")
        print("2. Add income")
        print("3. Do transfer")
        print("4. Close account")
        print("5. Log out")
        print("0. Exit")
        user_select = int(input())
        while user_select != 0:
            if user_select == 1:
                # print()
                # print("Balance: " + str(self.bank_bal))
                cur.execute("SELECT balance FROM card WHERE pin=?", (self.pin, ))
                total = cur.fetchone()
                print("Balance:", str(total).strip("(),"))
            elif user_select == 2:
                print("Enter income:")
                user_income = int(input())
                self.bank_bal += user_income
                cur.execute("UPDATE card SET balance = balance + ? WHERE pin = ?", (user_income, self.pin))
                conn.commit()
                print("Income was added!")
            elif user_select == 3:
                print("Transfer")
                print("Enter card number:")
                user_entry = input()
                cur.execute("SELECT number FROM card WHERE number=?", (user_entry,))
                card_check = cur.fetchone()
                if not check_luhn(user_entry):
                    print("Probably you made mistake in card number. Please try again!")
                elif int(user_entry) == self.card_num:
                    print("You can't transfer money to the same account!")
                # check database for card number
                elif not card_check:
                    print("Such a card does not exist")
                elif card_check:
                    print("Enter how much money you want to transfer:")
                    user_transfer = int(input())
                    cur.execute("SELECT balance FROM card WHERE pin=?", (self.pin, ))
                    grab_bal = cur.fetchone()
                    cur_balance = int(str(grab_bal).strip("(),"))
                    # print("cur", cur_balance)
                    if int(cur_balance) < user_transfer:
                        print("Not enough money!")
                    else:
                        cur.execute("UPDATE card SET balance = balance + ? WHERE number = ?", (user_transfer, user_entry))
                        cur.execute("UPDATE card SET balance = balance - ? WHERE number =?", (user_transfer, self.card_num))
                        conn.commit()
                        print("Success!")
            elif user_select == 4:
                cur.execute("DELETE FROM card WHERE number=? AND pin=?", (self.card_num, self.pin))
                conn.commit()
                print("This account has been closed!")
                break
            elif user_select == 5:
                print("You have successfully logged out!")
                break
            print()
            print("1. Balance")
            print("2. Add income")
            print("3. Do transfer")
            print("4. Close account")
            print("5. Log out")
            print("0. Exit")
            user_select = int(input())
        if user_select == 0:
            terminate = True


def user_credentials(card, pin):
    if pin in card_database:
        if card_database[pin].card_num == card:
            print("You have successfully logged in!")
            card_database[pin].access()
        else:
            print("Wrong card number or PIN!")
    else:
        print("Wrong card number or PIN!")


def verify_credentials(card_num, pin_num):
    # cur.execute("SELECT number FROM card WHERE number=?", (card_num, ))
    # c_check = cur.fetchone()
    # cur.execute("SELECT pin FROM card WHERE pin =?", (pin_num, ))
    # p_check = cur.fetchone()
    cur.execute("SELECT number, pin FROM card WHERE number=? AND pin=?", (card_num, pin_num))
    acc_check = cur.fetchone()
    if acc_check:
        print("You have successfully logged in!")
        new_card = Bank(pin_num, card_num)
        card_database[pin_num] = new_card
        card_database[pin_num].access()
    else:
        print("Wrong card number or PIN!")



def end_banking():
    print()
    return "Bye!"


def generate_card():
    ran_gen = random.randint(100000000, 999999999)
    card_nums = 400000000000000 + ran_gen
    list_ints = list(str(card_nums))
    convert = list()
    for i in list_ints:
        convert.append(int(i))
    for i in range(0, len(convert), 1):
        if i % 2 == 0:
            convert[i] *= 2
    list_sum = 0
    for i in range(len(convert)):
        if convert[i] > 9:
            convert[i] -= 9
        list_sum += convert[i]

    count = 0

    while list_sum % 10 != 0:
        list_sum += 1
        count += 1

    list_ints.insert(len(list_ints), str(count))
    final_num = convert_list(list_ints)

    if check_luhn(final_num):
        return final_num
    else:
        return 1


def check_luhn(id):
    list_id = list(str(id))
    convert = list()
    # print("List: ", list_id)
    check_sum = int(list_id[len(list_id) - 1])
    # print("Checksum", check_sum)
    for i in range(len(list_id) - 1):
        convert.append(int(list_id[i]))
    # print("Conversion: ", convert)
    for i, _ in enumerate(convert):
        #if i == 0:
         #   convert[i] *= 2
        if i % 2 == 0:
            convert[i] *= 2
    # print("Multi", convert)
    list_sum = 0
    for i in range(len(convert)):
        if convert[i] > 9:
            convert[i] -= 9
        list_sum += convert[i]
    # print("Sub", convert)
    # print("Sum", list_sum)

    count = 0
    while list_sum % 10 != 0:
        list_sum += 1
        count += 1
    # print("Count", count)

    if count == check_sum:
        return True
    else:
        return False


def convert_list(list):
    s = [str(i) for i in list]
    res = int("".join(s))
    return res


def sql_fetch(con):
    cursor = con.cursor()
    cursor.execute('SELECT * FROM card')
    rows = cursor.fetchall()
    for row in rows:
        print(row)


print("1. Create an account")
print("2. Log into account")
print("0. exit")

#generate_card()

user_choice = input()
while user_choice != "0":
    if user_choice == "1":
        # card_ran = random.randint(0000000000, 9999999999)
        # card_gen = (4000000000000000 + card_ran)
        card_gen = generate_card()
        while card_gen == 1:
            card_gen = generate_card()
        card_pin = random.randrange(1000, 9999)
        if card_pin in card_database:
            card_pin = random.randint(1000, 9999)
        new_card = Bank(card_pin, card_gen)
        card_database[card_pin] = new_card  # add to card database for login credentials.
        print("Your card has been created")
        cur.execute("INSERT INTO card(number, pin) VALUES(?,?);", (card_gen, card_pin))
        conn.commit()
        new_card.show_bank()
    elif user_choice == "2":
        print("Enter your card number:")
        cc_num = int(input())
        print("Enter your PIN:")
        pin_num = int(input())
        # user_credentials(cc_num, pin_num)
        verify_credentials(cc_num, pin_num)

    if terminate:
        break
    print()
    print("1. Create an account")
    print("2. Log into account")
    print("0. exit")
    user_choice = input()

print()
print("Bye!")
# sql_fetch(conn)

conn.close()

