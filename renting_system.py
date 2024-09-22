import os
from datetime import datetime, timedelta

class UsableEquipment:
    def __init__(self, name, brand, price, Quantity):
        self.name = name
        self.brand = brand
        self.price = float(price.replace("$", ""))
        self.quantity = int(Quantity)

class RentalShop:
    def __init__(self):
        self.equipment_list = []
        self.equip_equipment_data()

    def equip_equipment_data(self):
        try:
            with open("beginning_available_equipment.txt", "r") as file:
                for line in file:
                    data = line.strip().split(",")
                    equipment = UsableEquipment(data[0], data[1], data[2], data[3])
                    self.equipment_list.append(equipment)
        except FileNotFoundError:
            pass
        except Exception as e:
         print("An error occurred while loading equipment data:", e)

    def display_available_equipment(self):
        print("Available Equipment:")
        for idx, equipment in enumerate(self.equipment_list, start=1):
            print(f"{idx}. {equipment.name} ({equipment.brand}) - Price: ${equipment.price}, Quantity: {equipment.quantity}")

    def rent_equipment(self, equipment_idx, customer_name):
        try:
            if equipment_idx < 1 or equipment_idx > len(self.equipment_list):
                print("Invalid equipment selection.")
                return

            equipment = self.equipment_list[equipment_idx - 1]
            if equipment.quantity <= 0 or equipment.quantity > 5  :
                print("Selected equipment is not available for rent.")
                return
            quantity_to_rent = 0 
            try:
             quantity_to_rent = int(input(f"How many {equipment.name} ({equipment.brand}) do you want to rent?: "))
            except ValueError:
              print("please input valid data")
              return

            if quantity_to_rent <= 0 or quantity_to_rent >= equipment.quantity:
              print("Invalid quantity to rent.")
              return

            rented_equipment = []
            rented_equipment.append(equipment)

            total_amount = equipment.price *   quantity_to_rent 
            rental_date = datetime.now()
            return_date = rental_date + timedelta(days=5)

            invoice_filename = f"{customer_name}_{rental_date.strftime('%Y%m%d%H%M%S')}.txt"
            with open(invoice_filename, "w") as invoice_file:
                invoice_file.write("Invoice:\n")
                invoice_file.write(f"Customer: {customer_name}\n")
                invoice_file.write("Rented Equipment:\n")
                invoice_file.write(f"{quantity_to_rent} x {equipment.name} ({equipment.brand}) - Price: ${equipment.price} each\n")
                invoice_file.write(f"Rental Date: {rental_date}\n")
                invoice_file.write(f"Return Date: {return_date}\n")
                invoice_file.write(f"Total Amount: ${total_amount:.2f} \n")
               

            equipment.quantity -= quantity_to_rent
            self.save_equipment_data()
            print(f"{quantity_to_rent} {equipment.name} rented successfully. Invoice saved as {invoice_filename}")
            
        except Exception as e:
          print("An error occurred while renting equipment:", e)  

    def return_equipment(self, invoice_filename):
        try:
          invoice_info = None
          with open(invoice_filename, "r") as invoice_file:
              invoice_info = invoice_file.read()

          if not invoice_info:
              print("Invalid invoice filename.")
              return

          return_date = datetime.now()
          rental_date_str = invoice_info.split("\n")[5].split(": ")[1]
          rental_date = datetime.strptime(rental_date_str, "%Y-%m-%d %H:%M:%S.%f")
         
          equipment_name_line = invoice_info.split("Rented Equipment:\n")[1].split("\n")[0]
          equipment_name = equipment_name_line.split(" x ")[1].split(" (")[0] 
          equipment = None
          for eq in self.equipment_list:
              if eq.name == equipment_name:
                equipment = eq
                break

          if equipment is None:
              print("Equipment details not found.")
              return

          duration = (return_date - rental_date).days
          fine = 0.0
          if duration > 5:
             fine = (duration - 5) * 10.0

          with open("returned_equipment.txt", "a") as returned_file:
            returned_file.write("Returned Item:\n")
            returned_file.write(f"Customer name: {customer_name}\n")
            returned_file.write(f"Equipment: {equipment.name} ({equipment.brand})\n")
            returned_file.write(f"Returned Date: {return_date}\n")
            returned_file.write(f"Rent Duration: {duration} days\n")
            returned_file.write(f"Fine for extra days: ${fine:.2f}\n\n")

          equipment.quantity += 1
          self.save_equipment_data()
          print(f"Equipment returned successfully. /n Invoice updated.")
          os.remove(invoice_filename)
          print(f"--Invoice '{invoice_filename}' has been deleted--")
          
        except Exception as e:
            print("An error occurred while returning equipment:", e)

    def save_equipment_data(self):
        try:
          with open("equipment.txt", "w") as file:
              for equipment in self.equipment_list:
                  file.write(f"{equipment.name}, {equipment.brand}, ${equipment.price:.2f}, {equipment.quantity}\n")
        except Exception as e:  
             print("An error occurred while saving equipment data:", e)       
  
if __name__ == "__main__":
    rental_shop = RentalShop()

    while True:
        try:
          print("\n====  Equipment Rental Shop ====")
          print("1. show Available Equipment")
          print("2. Rent Item")
          print("3. Return rented item")
          print("4. Exit from the system")

          choice = input("Enter your choice: ")

          if choice == "1":
            rental_shop.display_available_equipment()
          elif choice == "2":
             rental_shop.display_available_equipment()
             equipment_idx = int(input("Enter the number of the equipment to rent: "))
             customer_name = input("Enter customer name: ")
             rental_shop.rent_equipment(equipment_idx, customer_name)
            
          elif choice == "3":
             invoice_filename = input("Enter the invoice filename for returning equipment: ")
             rental_shop.return_equipment(invoice_filename)
          elif choice == "4":
             print("Exiting the system.")
             break
          else:
            print("Invalid choice. Please choose again.")
            
        except ValueError:
          print("invalid input please input correctly")
           
