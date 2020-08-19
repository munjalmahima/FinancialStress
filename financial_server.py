from flask import Flask,render_template,request
risk_factor=[]
r={}
from datetime import datetime,timedelta
import termtables as tt
import numpy as np
import matplotlib
#matplotlib.use("Agg")
import matplotlib.pyplot as plt
current=datetime.now().date()
c,c1,types,food,groceries,utilities,transport,shopping,rent,entertainment,education,revenue=0,0,0,0,0,0,0,0,0,0,0,0
banks={'Allahabad Bank':10.65,'Axis Bank':12,'Bajaj Finserv':12.99,'Bank of Baroda':11.4,'Bank of India':10.5,
       'Bank of Maharashtra':10.85,'Central Bank':11.25,'City Bank':10.5,'Federal Bank':11.49,'SBI':10.5,'Yes Bank':10.99,'Tata Capital':10.99,'Union Bank of India':10.10}
gurgaon_bachelor={'food':2000,'groceries':2500,'transport':2500,'utilities':1000,'entertainment':500,'shopping':500,'rent':10500}
gurgaon_couple={'Community food':3000,'Community groceries':3250,'Community transport':3000,'Community utilities':3000,'Community entertainment':1000,'Community shopping':1200,'Community rent':13000}
gurgaon_family={'food':4000,'groceries':5500,'transport':5000,'utilities':5500,'entertainment':3500,'shopping':5000,'rent':20000,'education':11500}
app = Flask(__name__)
@app.route('/',methods = ['POST', 'GET'])
def student():
   return render_template('data.html')
@app.route('/result',methods = ['POST', 'GET'])
def result():
   global c,c1,types,food,groceries,utilities,transport,shopping,rent,entertainment,education,revenue
   future_dates=[]
   emi_amounts=[]
   if request.method == 'POST':
      result=request.form
      c='yes'
      types=request.form["type"]
      food=int(request.form["Food"])
      groceries=int(request.form["Groceries"])
      transport=int(request.form["Transport"])
      utilities=int(request.form["Utilities"])
      entertainment=int(request.form["Entertainment"])
      shopping=int(request.form["Shopping"])
      rent=int(request.form["House Rent"])
      if(types=='family'):
       education=int(request.form.get("Education"))
      revenue=int(request.form["revenue"])
      string3=''
      while(c=='yes'):
         if((types!='bachelor')and(types!='couple')and(types!='family')):
            continue
         tot=food+groceries+utilities+transport+shopping+entertainment+rent
         if(types=='family'):
            tot=food+groceries+utilities+transport+shopping+entertainment+rent+education
         c1=request.form["chkPassPort"]
         if(c1=='yes'):
            many=request.form.get("emis")
            sums=0
            for mm in range(int(many)):
               c2=request.form["emiorrate"+str(mm+1)]
               principal=int(request.form.get("principal"+str(mm+1)))
               time=int(request.form.get("time"+str(mm+1)))
               if(c2=='Yes'):
                   rate=float(request.form.get("rate"+str(mm+1)))
                   emi=emi_calculator(principal,rate,time)
                   string3=string3+"Your monthly EMI is:- "+str(emi)+"."
               else:
                   emi=float(request.form.get("rate"+str(mm+1)))
                   rate=0
                   l=[]
                   rates=[]
                   for i in range(7,21):
                       predicted_emi=emi_calculator(principal,i,time)
                       if(predicted_emi==emi):
                           rate=i
                           break
                       l.append(abs(predicted_emi-emi))
                       rates.append(i)
                   min1=min(l)
                   index1=l.index(min1)
                   index1=rates[index1]
                   l.remove(min1)
                   rates.remove(index1)
                   min2=min(l)
                   index2=l.index(min2)
                   index2=rates[index2]
                   if(index1>index2):
                       t=index1
                       index1=index2
                       index2=t
                   l1=[]
                   rates1=[]
                   for i in np.arange(index1,index2,0.01):
                       predicted_emi=emi_calculator(principal,round(i,2),time)
                       if(predicted_emi==emi):
                           rate=round(i,2)
                           break
                       l1.append(abs(predicted_emi-emi))
                       rates1.append(round(i,2))
                   min3=min(l1)
                   index3=l1.index(min3)
                   rate=rates1[index3]
                   string3=string3+"Rate of interest is:- "+str(rate)+"."
               previous=request.form["date"+str(mm+1)]
               dates=datetime.strptime(previous,'%Y-%m-%d').date()
               future=addYears(dates,time)
               day=(future-current).days
               if(day<=0):
                   string3=string3+"Loan is already paid."
                   continue
               string3=string3+"Future date of repayment:- "+future.strftime('%Y-%m-%d')+"."
               find(day)
               future_dates.append(future)
               emi_amounts.append(emi)
               sums+=emi
               for k in banks:
                   v=banks[k]
                   if(v<rate):
                       string3=string3+k+' is giving loans at lower rate of interest than your bank.'
                       string3=string3+'Emi:- '+str(emi_calculator(principal,v,time))+"."
            tot=tot+sums
            for i in range(0,len(future_dates)-1):
               for j in range(i+1,len(future_dates)):
                   if future_dates[i]>future_dates[j]:
                       temp=future_dates[i]
                       temp1=emi_amounts[i]
                       future_dates[i]=future_dates[j]
                       emi_amounts[i]=emi_amounts[j]
                       future_dates[j]=temp
                       emi_amounts[j]=temp1
            #string3=string3+"Future Dates:- "+future_dates
            #string3=string3+"Corresponding emi's:- "+emi_amounts
            return string3+final_evaluation(c1,types,sums,tot,future_dates,emi_amounts)
         else:
            sums=0
            return string3+final_evaluation(c1,types,sums,tot,future_dates,emi_amounts)


def risk(savings,emergency):
    if savings>0:
        if(savings==emergency):
            risk_factor.append(emergency-savings)
            return "You have 0 risk factor but you need to start saving more to sustain."
        if(savings>emergency):
            risk_factor.append(emergency-savings)
            return "You have Rs."+str(savings-emergency)+" extra in your emergency fund."
        else:
            if(emergency-savings>=30000):
                risk_factor.append(emergency-savings)
                return "You are under a great risk factor.You have Rs."+str(emergency-savings)+" less in your emergency fund."
            elif(emergency-savings>=20000):
                risk_factor.append(emergency-savings)
                return "You are under a heavy risk factor.You have Rs."+str(emergency-savings)+" less in your emergency fund."
            elif(emergency-savings>=10000):
                risk_factor.append(emergency-savings)
                return "You are under a mild risk factor.You have Rs."+str(emergency-savings)+"less in your emergency fund."
            elif(emergency-savings>0):
                risk_factor.append(emergency-savings)
                return "You are under a low risk factor.You have Rs."+str(emergency-savings)+"less in your emergency fund."       
    else:
        return "You are under a severe risk factor.You have 0 emergency fund.Please start saving immediately to avoid future crisis."
        return "Monthly Burden:- Rs."+str(savings*-1)

def emi_calculator(p, r, t): 
    r=r/(12*100)  
    t=t*12  
    emi=(p * r * pow(1 + r, t)) / (pow(1 + r, t) - 1)
    emi=round(emi,2)
    return emi

def addYears(d,years):
    try:        
        return d.replace(year=d.year+years)
    except ValueError:     
        return d+(date(d.year + years, 1, 1)-date(d.year, 1, 1))
def find(number_of_days): 
    year = int(number_of_days/365) 
    week = int((number_of_days%365)/7) 
    days = (number_of_days%365)%7 
    return(year,"years,",week, "weeks and ",days,"days are left for repayment of loan.")
def analysis_bachelor(sum_of_emis,total,stringmm):
        global risk_factor
        string=''
        string=string+"ANALYSIS"
        community_total=gurgaon_bachelor['food']+gurgaon_bachelor['groceries']+gurgaon_bachelor['utilities']+gurgaon_bachelor['transport']+gurgaon_bachelor['shopping']+gurgaon_bachelor['entertainment']+gurgaon_bachelor['rent']
        t1=round(revenue-total,2)
        t2=round(revenue-community_total,2)
        diff=round(t1-t2,2)
        emergency_fund=t1*6
        string = tt.to_string([["Food", food,gurgaon_bachelor['food'],food-gurgaon_bachelor['food']],
                               ["Groceries", groceries,gurgaon_bachelor['groceries'],groceries-gurgaon_bachelor['groceries']],
                               ["Utilities",utilities,gurgaon_bachelor['utilities'],utilities-gurgaon_bachelor['utilities']],
                               ["Transport",transport,gurgaon_bachelor['transport'],transport-gurgaon_bachelor['transport']],
                               ["Shopping",shopping,gurgaon_bachelor['shopping'],shopping-gurgaon_bachelor['shopping']],
                               ["Entertainment",entertainment,gurgaon_bachelor['entertainment'],entertainment-gurgaon_bachelor['entertainment']],
                               ["Rent",rent,gurgaon_bachelor['rent'],rent-gurgaon_bachelor['rent']],
                               ["EMI",sum_of_emis,0,sum_of_emis-0],["Total",total,community_total,total-community_total],
                               ["Savings",t1,t2,diff],["Savings(3 Months)",t1*3,t2*3,diff*3],["Savings(6 Months)",t1*6,t2*6,diff*6],
                               ["Savings(9 Months)",t1*9,t2*9,diff*9],["Savings(1 Year)",t1*12,t2*12,diff*12]],
                              header=["Domain", "Your expense","Community Expense","Difference"],style=tt.styles.ascii_thin_double,)
        string1=''
        string1=string1+"\n\n\n\n  Summary:-"
        string1=string1+"   Your Total expenses :  "+str(total)
        string1=string1+"   Community Total expenses :  "+str(community_total)
        string1=string1+"\n   Your Savings(1 month):  "+str(t1)+"\nYour Savings(3 months):-"+str(t1*3)+"\nYour Savings(6 months):-"+str(t1*6)+"\nYour Savings(1 year):-"+str(t1*12)
        string1=string1+"\n   Community Savings(1 month):   "+str(t2)+"\nCommunity Savings(3 months):-"+str(t2*3)+"\nCommunity Savings(6 months):-"+str(t2*6)+"\nCommunity Savings(1 year):-"+str(t2*12)
        string1=string1+"\n   Total Emi amount :  "+str(sum_of_emis)    

        if(food>gurgaon_bachelor['food']):
            string1=string1+'\n  You are spending'+str(food-gurgaon_bachelor['food'])+'Rs. extra on food per month.'
        if(groceries>gurgaon_bachelor['groceries']):
            string1=string1+'\n  You are spending'+str(groceries-gurgaon_bachelor['groceries'])+' Rs. extra on groceries/household items per month.'
        if(utilities>gurgaon_bachelor['utilities']):
           string1=string1+'\n   You are spending'+str(utilities-gurgaon_bachelor['utilities'])+' Rs. extra on bills per month.'
        if(transport>gurgaon_bachelor['transport']):
           string1=string1+'\n   You are spending'+str(transport-gurgaon_bachelor['transport'])+' Rs. extra on transportation per month.'
        if(shopping>gurgaon_bachelor['shopping']):
            string1=string1+'\n  You are spending'+str(shopping-gurgaon_bachelor['shopping'])+' Rs. extra on shopping per month.'
        if(entertainment>gurgaon_bachelor['entertainment']):
           string1=string1+'\n   You are spending'+str(entertainment-gurgaon_bachelor['entertainment'])+'Rs. extra on entertainment per month.'
        if(rent>gurgaon_bachelor['rent']):
            string1=string1+'\n  You are spending'+str(rent-gurgaon_bachelor['rent'])+' Rs. extra on house rent per month.'
        if(t1<t2):
            string1=string1+"\n  You can save "+str(t2-t1)+" more per month as per community standards."
        else:
            string1=string1+"\n  Your savings per month are optimal as per community standards."
        if t1>0:
            string1=string1+"\n  You have some savings in your account.You need an emergency fund of Rs. "+str(emergency_fund)
            date=current
            date_matrix=[]
            risk_factor.clear()
            string1=string1+"\n   RISK FACTOR ANALYSIS(AS PER YOUR CURRENT EXPENDITURE)"
            for i in range(1,7):
                string1=string1+"\nAfter "+date.strftime("%Y-%m-%d")+" : "
                mahima=risk(t1*i,emergency_fund)
                string1=string1+mahima
                date_matrix.append(date)
                if(date.month in[1,3,5,7,8,10,12]):
                    date=date+timedelta(31)
                elif(date.month in[4,6,9,11]):
                    date=date+timedelta(30)
                else:
                    date=date+timedelta(28)
            plt.plot(date_matrix,risk_factor,label="Your savings")
            if(diff<0):
                string1=string1+"\n   RISK FACTOR ANALYSIS(AS PER OUR SAVING PLAN)"
                date_matrix.clear()
                risk_factor.clear()
                date=current
                for i in range(1,7):
                    string1=string1+"\nAfter "+date.strftime("%Y-%m-%d")+" : "
                    mahima=risk(t2*i,emergency_fund)
                    string1=string1+mahima
                    date_matrix.append(date)
                    if(date.month in[1,3,5,7,8,10,12]):
                        date=date+timedelta(31)
                    elif(date.month in[4,6,9,11]):
                        date=date+timedelta(30)
                    else:
                        date=date+timedelta(28)
                plt.plot(date_matrix,risk_factor,label="Savings as per our plan")
            plt.title("DATE VS. RISK FACTOR "+stringmm)
            plt.xlabel("Date")
            plt.ylabel("Risk Factor")
            plt.legend()
            plt.show()
        else:
            string1=string1+risk(t1,emergency_fund)
        return(string1)
def analysis_couple(sum_of_emis,total,stringmm):
        global risk_factor
        string=''
        string=string+"ANALYSIS"
        community_total=gurgaon_couple['Community food']+gurgaon_couple['Community groceries']+gurgaon_couple['Community utilities']+gurgaon_couple['Community transport']+gurgaon_couple['Community shopping']+gurgaon_couple['Community entertainment']+gurgaon_couple['Community rent']
        t1=round(revenue-total,2)
        t2=round(revenue-community_total,2)
        diff=round(t1-t2,2)
        emergency_fund=t1*6
        string = tt.to_string([["Food", food,gurgaon_couple['Community food'],food-gurgaon_couple['Community food']],
                               ["Groceries", groceries,gurgaon_couple['Community groceries'],groceries-gurgaon_couple['Community groceries']],
                               ["Utilities",utilities,gurgaon_couple['Community utilities'],utilities-gurgaon_couple['Community utilities']],
                               ["Transport",transport,gurgaon_couple['Community transport'],transport-gurgaon_couple['Community transport']],
                               ["Shopping",shopping,gurgaon_couple['Community shopping'],shopping-gurgaon_couple['Community shopping']],
                               ["Entertainment",entertainment,gurgaon_couple['Community entertainment'],entertainment-gurgaon_couple['Community entertainment']],
                               ["Rent",rent,gurgaon_couple['Community rent'],rent-gurgaon_couple['Community rent']],["EMI",sum_of_emis,0,sum_of_emis-0],
                               ["Total",total,community_total,total-community_total],["Savings",t1,t2,diff],["Savings(3 Months)",t1*3,t2*3,diff*3],["Savings(6 Months)",t1*6,t2*6,diff*6],
                               ["Savings(9 Months)",t1*9,t2*9,diff*9],["Savings(1 Year)",t1*12,t2*12,diff*12]],
                              header=["Domain", "Your expense","Community Expense","Difference"],style=tt.styles.ascii_thin_double,)
        string1=''
        string1=string1+"\n\n\n\nSummary:-"
        string1=''
        string1=string1+"\n\n\n\n  Summary:-"
        string1=string1+"   Your Total expenses :  "+str(total)
        string1=string1+"   Community Total expenses :  "+str(community_total)
        string1=string1+"\n   Your Savings(1 month):  "+str(t1)+"\nYour Savings(3 months):-"+str(t1*3)+"\nYour Savings(6 months):-"+str(t1*6)+"\nYour Savings(1 year):-"+str(t1*12)
        string1=string1+"\n   Community Savings(1 month):   "+str(t2)+"\nCommunity Savings(3 months):-"+str(t2*3)+"\nCommunity Savings(6 months):-"+str(t2*6)+"\nCommunity Savings(1 year):-"+str(t2*12)
        string1=string1+"\n   Total Emi amount :  "+str(sum_of_emis)    
        if(food>gurgaon_couple['Community food']):
            string1=string1+'\n   You are spending'+str(food-gurgaon_couple['Community food'])+'Rs. extra on food per month.'
        if(groceries>gurgaon_couple['Community groceries']):
            string1=string1+'\n   You are spending'+str(groceries-gurgaon_couple['Community groceries'])+'Rs. extra on groceries/household items per month.'
        if(utilities>gurgaon_couple['Community utilities']):
            string1=string1+'\n   You are spending'+str(utilities-gurgaon_couple['Community utilities'])+'Rs. extra on bills per month.'
        if(transport>gurgaon_couple['Community transport']):
            string1=string1+'\n   You are spending'+str(transport-gurgaon_couple['Community transport'])+'Rs. extra on transportation per month.'
        if(shopping>gurgaon_couple['Community shopping']):
            string1=string1+'\n   You are spending'+str(shopping-gurgaon_couple['Community shopping'])+'Rs. extra on shopping per month.'
        if(entertainment>gurgaon_couple['Community entertainment']):
            string1=string1+'\n   You are spending'+str(entertainment-gurgaon_couple['Community entertainment'])+'Rs. extra on entertainment per month.'
        if(rent>gurgaon_couple['Community rent']):
            string1=string1+'\n   You are spending'+str(rent-gurgaon_couple['Community rent'])+'Rs. extra on house rent per month.'
        if(t1<t2):
            string1=string1+"\n   You can save "+str(t2-t1)+" more per month as per community standards."
        else:
            string1=string1+"\n   Your savings per month are optimal as per community standards."
        if t1>0:
            string1=string1+"\n   You have some savings in your account.You need an emergency fund of Rs."+str(emergency_fund)
            date=current
            date_matrix=[]
            risk_factor.clear()
            string1=string1+"\n    RISK FACTOR ANALYSIS(AS PER YOUR CURRENT EXPENDITURE)"
            for i in range(1,7):
                string1=string1+"\nAfter "+date.strftime("%Y-%m-%d")+" : "
                mahima=risk(t1*i,emergency_fund)
                string1=string1+mahima
                date_matrix.append(date)
                if(date.month in[1,3,5,7,8,10,12]):
                    date=date+timedelta(31)
                elif(date.month in[4,6,9,11]):
                    date=date+timedelta(30)
                else:
                    date=date+timedelta(28)
            plt.plot(date_matrix,risk_factor,label="Your savings")
            if(diff<0):
                string1=string1+"\n   RISK FACTOR ANALYSIS(AS PER OUR SAVING PLAN)"
                date_matrix.clear()
                risk_factor.clear()
                date=current
                for i in range(1,7):
                    string1=string1+"\nAfter "+date.strftime('%Y-%m-%d')+" : "
                    mahima=risk(t2*i,emergency_fund)
                    string1=string1+mahima
                    date_matrix.append(date)
                    if(date.month in[1,3,5,7,8,10,12]):
                        date=date+timedelta(31)
                    elif(date.month in[4,6,9,11]):
                        date=date+timedelta(30)
                    else:
                        date=date+timedelta(28)
                plt.plot(date_matrix,risk_factor,label="Savings as per our plan")
            plt.title("DATE VS. RISK FACTOR "+stringmm)
            plt.xlabel("Date")
            plt.ylabel("Risk Factor")
            plt.legend()
            plt.show()
        else:
            string1=string1+risk(t1,emergency_fund)
        return(string1)
        
def analysis_family(sum_of_emis,total,stringmm):
        global risk_factor
        string=''
        string=string+"ANALYSIS"
        community_total=gurgaon_family['food']+gurgaon_family['groceries']+gurgaon_family['utilities']+gurgaon_family['transport']+gurgaon_family['shopping']+gurgaon_family['entertainment']+gurgaon_family['rent']+gurgaon_family['education']
        t1=round(revenue-total,2)
        t2=round(revenue-community_total,2)
        diff=round(t1-t2,2)
        emergency_fund=t1*6
        string = tt.to_string([["Food", food,gurgaon_family['food'],food-gurgaon_family['food']],
                               ["Groceries", groceries,gurgaon_family['groceries'],groceries-gurgaon_family['groceries']],
                               ["Utilities",utilities,gurgaon_family['utilities'],utilities-gurgaon_family['utilities']],
                               ["Transport",transport,gurgaon_family['transport'],transport-gurgaon_family['transport']],
                               ["Shopping",shopping,gurgaon_family['shopping'],shopping-gurgaon_family['shopping']],
                               ["Entertainment",entertainment,gurgaon_family['entertainment'],entertainment-gurgaon_family['entertainment']],
                               ["Rent",rent,gurgaon_family['rent'],rent-gurgaon_family['rent']],["EMI",sum_of_emis,0,sum_of_emis-0],
                               ["Schooling of Kid",education,gurgaon_family['education'],education-gurgaon_family['education']],
                               ["Total",total,community_total,total-community_total],["Savings",t1,t2,diff],["Savings(3 Months)",t1*3,t2*3,diff*3],["Savings(6 Months)",t1*6,t2*6,diff*6],
                               ["Savings(9 Months)",t1*9,t2*9,diff*9],["Savings(1 Year)",t1*12,t2*12,diff*12]],
                              header=["Domain", "Your expense","Community Expense","Difference"],style=tt.styles.ascii_thin_double,)
        string1=''
        string1=string1+"Summary:- "
        string1=''
        string1=string1+"\n\n\n\n  Summary:-"
        string1=string1+"   Your Total expenses :  "+str(total)
        string1=string1+"   Community Total expenses :  "+str(community_total)
        string1=string1+"\n   Your Savings(1 month):  "+str(t1)+"\nYour Savings(3 months):-"+str(t1*3)+"\nYour Savings(6 months):-"+str(t1*6)+"\nYour Savings(1 year):-"+str(t1*12)
        string1=string1+"\n   Community Savings(1 month):   "+str(t2)+"\nCommunity Savings(3 months):-"+str(t2*3)+"\nCommunity Savings(6 months):-"+str(t2*6)+"\nCommunity Savings(1 year):-"+str(t2*12)
        string1=string1+"\n   Total Emi amount :  "+str(sum_of_emis)    
        if(food>gurgaon_family['food']):
            string1=string1+'   You are spending'+str(food-gurgaon_family['food'])+'Rs. extra on food per month.'
        if(groceries>gurgaon_family['groceries']):
            string1=string1+'   You are spending'+str(groceries-gurgaon_family['groceries'])+'Rs. extra on groceries/household items per month.'
        if(utilities>gurgaon_family['utilities']):
             string1=string1+'   You are spending'+str(utilities-gurgaon_family['utilities'])+'Rs. extra on bills per month.'
        if(transport>gurgaon_family['transport']):
             string1=string1+'   You are spending'+str(transport-gurgaon_family['transport'])+'Rs. extra on transportation per month.'
        if(shopping>gurgaon_family['shopping']):
             string1=string1+'   You are spending'+str(shopping-gurgaon_family['shopping'])+'Rs. extra on shopping per month.'
        if(entertainment>gurgaon_family['entertainment']):
             string1=string1+'   You are spending'+str(entertainment-gurgaon_family['entertainment'])+'Rs. extra on entertainment per month.'
        if(rent>gurgaon_family['rent']):
             string1=string1+'   You are spending'+str(rent-gurgaon_family['rent'])+'Rs. extra on house rent per month.'
        if(education>gurgaon_family['education']):
             string1=string1+'   You are spending'+str(rent-gurgaon_family['education'])+'Rs. extra on the school education of your kid per month.'
        string1=string1+"\n   Your Savings(1 month):-"+str(t1)+"\nYour Savings(3 months):-"+str(t1*3)+"\nYour Savings(6 months):-"+str(t1*6)+"\nYour Savings(1 year):-"+str(t1*12)
        string1=string1+"\n   Community Savings(1 month):-"+str(t2)+"\nCommunity Savings(3 months):-"+str(t2*3)+"\nCommunity Savings(6 months):-"+str(t2*6)+"\nCommunity Savings(1 year):-"+str(t2*12)
        if(t1<t2):
             string1=string1+"   You can save Rs."+str(t2-t1)+" more per month as per community standards."
        else:
             string1=string1+"   Your savings per month are optimal as per community standards."
        if t1>0:
            string1=string1+"   You have some savings in your account.You need an emergency fund of Rs."+str(emergency_fund)
            date=current
            date_matrix=[]
            risk_factor.clear()
            string1=string1+"   RISK FACTOR ANALYSIS(AS PER YOUR CURRENT EXPENDITURE)"
            for i in range(1,7):
                string1=string1+"After "+date.strftime('%Y-%m-%d')+" : "
                mahima=risk(t1*i,emergency_fund)
                string1=string1+mahima
                date_matrix.append(date)
                if(date.month in[1,3,5,7,8,10,12]):
                    date=date+timedelta(31)
                elif(date.month in[4,6,9,11]):
                    date=date+timedelta(30)
                else:
                    date=date+timedelta(28)
            plt.plot(date_matrix,risk_factor,label="Your savings")
            if(diff<0):
                string1=string1+"   RISK FACTOR ANALYSIS(AS PER OUR SAVING PLAN)"
                date_matrix.clear()
                risk_factor.clear()
                date=current
                for i in range(1,7):
                    string1=string1+"After "+date.strftime('%Y-%m-%d')+" : "
                    mahima=risk(t2*i,emergency_fund)
                    string1=string1+mahima
                    date_matrix.append(date)
                    if(date.month in[1,3,5,7,8,10,12]):
                        date=date+timedelta(31)
                    elif(date.month in[4,6,9,11]):
                        date=date+timedelta(30)
                    else:
                        date=date+timedelta(28)
                plt.plot(date_matrix,risk_factor,label="Savings as per our plan")
            plt.title("DATE VS. RISK FACTOR "+stringmm)
            plt.xlabel("Date")
            plt.ylabel("Risk Factor")
            plt.legend()
            plt.show()
        else:
            string1=string1+risk(t1,emergency_fund)
        return(string1)
#print("                               YOUR EXPENDITURE ANALYSIS                        ")
def final_evaluation(c1,types,sums,tot,future_dates,emi_amounts):
        string2=''
        if(types=='bachelor'):
            if(c1=='yes'):
                string2=string2+" XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
                stringmm="\n                            Before "+future_dates[0].strftime('%Y-%m-%d')
                string2=string2+stringmm
                string2=string2+analysis_bachelor(sums,tot,stringmm)
                for i in range(len(future_dates)):
                    string2=string2+" XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
                    stringmm="\n                           After "+future_dates[i].strftime('%Y-%m-%d')
                    string2=string2+stringmm
                    sums=round(sums-emi_amounts[i],2)
                    tot=round(tot-emi_amounts[i],2)
                    risk_factor.clear()
                    string2=string2+analysis_couple(sums,tot,stringmm)
                print(string2)
                return string2
            else:
                return analysis_bachelor(sums,tot,'')
        elif(types=='couple'):
            if(c1=='yes'):
                string2=string2+" XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
                stringmm="\n                                 Before "+future_dates[0].strftime('%Y-%m-%d')
                string2=string2+stringmm
                string2=string2+analysis_couple(sums,tot,stringmm)
                for i in range(len(future_dates)):
                    string2=string2+" XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
                    stringmm="\n                                 After "+future_dates[0].strftime('%Y-%m-%d')
                    string2=string2+stringmm
                    sums=round(sums-emi_amounts[i],2)
                    tot=round(tot-emi_amounts[i],2)
                    risk_factor.clear()
                    string2=string2+analysis_couple(sums,tot,stringmm)
                print(string2)
                return string2
            else:
                 return analysis_couple(sums,tot,'')
        elif(types=='family'):
            if(c1=='yes'):
                string2=string2+" XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
                stringmm="\nBefore"+future_dates[0].strftime('%Y-%m-%d')
                string2=string2+stringmm
                string2=string2+analysis_family(sums,tot,stringmm)
                for i in range(len(future_dates)):
                    string2=string2+" XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
                    stringmm="\nAfter "+future_dates[i].strftime('%Y-%m-%d')
                    string2=string2+stringmm
                    sums=round(sums-emi_amounts[i],2)
                    tot=round(tot-emi_amounts[i],2)
                    risk_factor.clear()
                    string2=string2+analysis_couple(sums,tot,stringmm)
                
                return string2
            else:
                 return analysis_family(sums,tot,'')
                 


if __name__ == '__main__':
   app.run(debug = True)
