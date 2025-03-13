#Roquia Ibrahim
#CIS261

from datetime import datetime


def CreateUsers():
    print('##### create users, passwords, and roles #####')
    with open("Users.txt", "a") as UserFile:
        while True:
            username = input("Enter user name or 'END' to quit:  ").strip()
            if username.upper() == "END":
                break
            password = input("Enter password: ").strip()
            role = input("Enter role (Admin or User): ").strip().upper()
            if role not in ["ADMIN", "USER"]:
                print("Invalid role. Enter  'Admin' or 'User'.")
                continue
             
            UserFile.write(f"{username} | {password} | {role}\n")
         
    
def Login():
    print("##### Login #####")
    username = input("Enter user name:  ").strip()
    password = input("Enter  password: ").strip()
    
    with open("Users.txt", "r") as UserFile:
        for line in UserFile:
            stored_username, stored_password, stored_role = line.strip().split("|")
            if username == stored_username and password == stored_password:
                return stored_role, username
            
    print("Invalid username or password!")
    return None, None
  

def  get_valid_date(prompt):
    """Keep asking for a valid data until entered correctly or 'All'  is provided."""
    while True:
        date_input = input(prompt).strip()
        if date_input.upper() == "ALL":
            return "ALL"
        try:
            return datetime.strptime(date_input, "%m/%d/%y")
        except ValueError:
            print("Invalid date formate. Please enter in MM/DD/YYYY format. ")
                          
 
def CalcTaxAndNetPay(hours, hourlyrate,taxrate):
     grosspay = hours * hourlyrate
     incometax =  grosspay * taxrate
     netpay = grosspay - incometax
     return grosspay, incometax, netpay
    
def main():
    CreateUsers()
  
    UserRole, UserName = Login()
    if UserRole is None:
        return
    
    EmpTotals = {"TotEmp":  0, "TotHours": 0, "TotGrossPay": 0, "TotTax": 0, "TotNetPay":  0}
                 
    print("##### Data Entry #####")
    rundate = get_valid_date("Enrer start date for report MM/DD/YYYY or 'ALL' for all data in file:  ")
   
    with open("Employees.txt", "r") as EmpFile:
        for line in EmpFile:
            EmpList = line.strip().split("|")
            if len(EmpList) < 6:
                 print("Error: Incomplete data in Employees.txt, skipping entry.")
                 continue
     
            try:
                fromdate = EmpList[0]
                checkdate = datetime.strptime(fromdate, "%m/%d/%Y")
                empname = EmpList[2]
                hours =  float(EmpList[3])
                hourlyrate = float(EmpList[4])
                taxrate = float(EmpList[5]) / 100
            except ValueError:
                  print(f"Debug: Checking Employees Record -> {EmpList}")  
                  print(f"Error: Invalid numeric data in Employees.txt -> {EmpList}, skipping entry.")
                  continue
     
            if rundate == "ALL" or checkdate >= rundate:
                grosspay, incometax, netpay = CalcTaxAndNetPay(hours, hourlyrate, taxrate)
         
                print(f"{fromdate} | {EmpList[1]} | {empname} | {hours:.2f} | {hourlyrate:.2f} | {grosspay:,.2f} | {taxrate / 100:.1%} | {incometax:,.2f} | {netpay:,.2f}")
                 
                EmpTotals["TotEmp"] += 1
                EmpTotals["TotHours"] +=  hours
                EmpTotals["TotGrossPay"] +=  grosspay
                EmpTotals["TotTax"]  +=  incometax 
                EmpTotals["TotNetPay"] += netpay

    if EmpTotals["TotEmp"] > 0:
        PrintTotals(EmpTotals)
    else:
         print("No payroll date to display.")
      
    input("\nPress any key to continue...")
  
def PrintTotals(EmpTotals):
    print("\nTotal  Number of Employees:", EmpTotals["TotEmp"])
    print("Total Hours Worked:", EmpTotals["TotHours"])
    print("Total Gross Pay: $", format(EmpTotals["TotGrossPay"], ".2f"))
    print("Total Income Taxe: $", format(EmpTotals["TotTax"], ".2f"))
    print("Total Net Pay: $", format(EmpTotals["TotNetPay"], ".2f"))
    

if __name__ == "__main__":
    main()
 
    

    