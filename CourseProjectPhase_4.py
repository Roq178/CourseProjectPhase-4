#Roquia Ibrahim
#CIS261

from datetime import datetime


def CreateUsers():
    print('##### create users, passwords, and roles #####')
    UserFile = open("Users.txt", "a")
    
    while True:
        username = GetUserName()
        if (username.upper() == "END"):
            break
        userpwd = GetUserPassword()
        userrole = GetUserRole()
        
        UserDetail = username + "|" + userpwd + "|" + userrole + "\n"
        UserFile.write(UserDetail)
     
    UserFile.close()
   
    
def GetUserName():
    return input("Enter user name or 'END'to quit: ")


def GetUserPassword():
    return input("Enter password: ")
    

def GetUserRole():
    while True:
        role = input("Enter role (Admin or User): ").upper()
        if role in ["ADMIN",  "USER"]:
            return role
        else:
            print("Invalid role. please enter role 'Admin' or 'User': ")
           
    
def Login():
    UserFile = open("Users.txt", "r")
    UserName = input("Enter user name: ")
    UserRole = "None"
    
    while True:
        UserDetail = UserFile.readline()
        if not UserDetail:
            return UserRole, UserName
        
        UserDetail = UserDetail.replace("\n", "")
        UserList = UserDetail.split("|")
        
        if UserName == UserList[0]:
            UserRole = UserList[2]
            return UserRole, UserName
        
    return UserRole, UserName


def GetEmpName():
    return input("Enter employee name: ")
    
def GetDateWorked():
    return input("Enter the start date (MM/DD/YYYY):  ")

def GetEndDate():
    return input("Enter the end date (MM/DD/YYYY): ")
 
def GetHoursWorked():
    return float(input("Enter amount of hours worked:  "))
        
def GetHourlyRate():
    return float(input("Enter hourly rate: "))
      
  
def GetTaxRate():
    return float(input("Enter tax rate:  "))
 
 
def CalcTaxAndNetPay(hours, hourlyrate,taxrate):
     grosspay = hours * hourlyrate
     incometax =  grosspay * (taxrate / 100)
     netpay = grosspay - incometax
     return grosspay, incometax, netpay

def PrintTotals(EmpTotals):
    print("\nTotal  Number of Employees:", EmpTotals["TotEmp"])
    print("Total Hours Worked:", EmpTotals["TotHours"])
    print("Total Gross Pay: $", format(EmpTotals["TotGrossPay"], ".2f"))
    print("Total Income Taxe: $", format(EmpTotals["TotTax"], ".2f"))
    print("Total Net Pay: $", format(EmpTotals["TotNetPay"], ".2f"))
    
def main():
    CreateUsers()
    
    print("##### Data Entry #####")
    
    UserRole, UserName = Login()
    
    DetailsPrinted = False
    EmpTotals = {"TotEmp":  0, "TotHours": 0, "TotGrossPay": 0, "TotTax": 0, "TotNetPay":  0}
    
    if UserRole is "None":
        print(UserName, "is invalid.")
    else:
        if UserRole.upper() == "ADMIN":
            EmpFile = open("Employees.txt", "a+")
            while True:
                empname = GetEmpName()
                if empname.upper() == "END":
                    break
                
                fromdate = GetDateWorked()
                todate = GetEndDate()
                hours = GetHoursWorked()
                hourlyrate = GetHourlyRate()
                taxrate = GetTaxRate()
                
                grosspay, incometax, netpay = CalcTaxAndNetPay(hours, hourlyrate, taxrate)
               
                EmpDetail = fromdate + "|" + todate + "|" + empname + "|" + str(hours) + "|" + str(hourlyrate) + "|"+ str(taxrate) + "\n"
                EmpFile.write(EmpDetail)
                
            EmpFile.close()
            
        print("\n#### Payroll Summary ####")
        
        rundate = input("Enter start date for report (MM/DD/YYYY) or 'ALL' for all date in file: ")
        if rundate.upper() == "ALL":
            pass
        else:
            try:
                 rundate = datetime.strptime(rundate, "%m/%d?%Y")
            except ValueError:
                 print("Invalid date format. Please try again.")
                 return
         
        EmpFile = open("Employees.txt", "r")
        
        while True:
              EmpDetail = EmpFile.readline()
              if not EmpDetail:
                  break
             
              EmpDetail = EmpDetail.replace("\n", "")
              EmpList = EmpDetail.split("|")
         
              fromdate = EmpList[0]
              checkdate = datetime.strptime(fromdate,  "%m/%d/%Y")
         
              if rundate.upper()  ==  "ALL" or checkdate >= rundate:
                  empname = EmpList[2]
                  hours =  float(EmpList[3])
                  hourlyrate = float(EmpList[4])
                  taxrate = float(EmpList[5])
         
                  grosspay, incometax, netpay = CalcTaxAndNetPay(hours, hourlyrate, taxrate)
         
                  print(f"{fromdate} {EmpList[1]} {empname} {hours:6.2f} {hourlyrate:6.2f} {grosspay:8.2f} {taxrate:6.1f}% {incometax:8.2f} {netpay:8.2f}")
                 
                  EmpTotals["TotEmp"] += 1
                  EmpTotals["TotHours"] +=  hours
                  EmpTotals["TotGrossPay"] +=  grosspay
                  EmpTotals["TotTax"]  +=  incometax 
                  EmpTotals["TotNetPay"] += netpay
        
        EmpFile.close()

        if EmpTotals["TotEmp"] > 0:
            PrintTotals(EmpTotals)
        else:
             print("No payroll date to display.")
      
    input("\nPress any key to continue...")

if __name__ == "__main__":
    main()
 
    

    