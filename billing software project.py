from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
import datetime
from tkinter import filedialog


mysqldb=mysql.connector.connect(host="localhost",user="root",passwd="youtube24/7",database="mp_enterprises")
cursor=mysqldb.cursor()
GT=[]


def login():
    user=admin_id.get()
    passwd=admin_passwd.get()

    logindb(user,passwd)
def logindb(user,passwd):
    if passwd:
        cursor.execute("select passsword from admin_account where admin_name='{}'".format(user))
        data=cursor.fetchall()
        if passwd!=data[0][0]:
            messagebox.showwarning("INVALID","Sorry Wrong Password or Admin id")
        else:
            main_program()
def main_program():
    

    def saveall():
        cursor.execute("insert into purchase values('{}','{}','{}',{},{},'{}')".format(ndate,ntime,cname.get(),grtotal.get(),phoneno.get(),payselected.get()))
        mysqldb.commit()

        text=filedialog.asksaveasfilename(initialdir=r"C:\Users\user\AppData\Local\Programs\Python\Python39\project billing",title="SAVE BILL",filetypes=(("text files","*.txt"),))
        text_file=open(text,'w')
        text_file.write(textarea.get(1.0,END))

        cname.set('')
        grtotal.set('')
        phoneno.set('')
        textarea.delete(1.0,END)
        
        
    def intobill():
        if len(GT)==0:
            TOT=tamt.get()
            GT.append(TOT)
        else:
            TOT=tamt.get()
            GT.append(TOT)
        global GGTOT
        GGTOT=sum(GT)
        cursor.execute("select product_quantity from stock where product_name='{}'".format(nam.get()))
        data=cursor.fetchall()
        oldqty=data[0][0]
        newqty=int(oldqty)-int(qty1.get())
        cursor.execute("""update stock set product_quantity={}
                        where product_name='{}'""".format(newqty,nam.get()))
        mysqldb.commit()
        
        
        
        if textarea.get(1.0,1.1)!=(''):
            textarea.insert(END,f"{nam.get()}")
            textarea.insert(END,f"\t{mrp1.get()}")
            textarea.insert(END,f"\t{opr.get()}")
            textarea.insert(END,f"\t{qty1.get()}")
            textarea.insert(END,f"\t{tamt.get()}\n")
          
            
                            
        else:
            textarea.delete(1.0,END)
            textarea.insert(END,"                        MP ENTERPRISES\n")
            textarea.insert(END,f"\nDate:{ndate}                             Day:{day}\n")
            textarea.insert(END,f"Customer:{cname.get()}\n")
            textarea.insert(END,f"Ph:{phoneno.get()}\n")
            textarea.insert(END,f"Payment Type:{payselected.get()}\n")
            textarea.insert(END,"____________________________________\n")
            textarea.insert(END,"********************************************************\n")
            textarea.insert(END," item")
            textarea.insert(END,"\tMRP")
            textarea.insert(END,"\tour")
            textarea.insert(END,"\tqty")
            textarea.insert(END,"\tTotal\n")
            textarea.insert(END,"                                  price\n")
            textarea.insert(END,"********************************************************\n")
            textarea.insert(END,f"{nam.get()}")
            textarea.insert(END,f"\t{mrp1.get()}")
            textarea.insert(END,f"\t{opr.get()}")
            textarea.insert(END,f"\t{qty1.get()}")
            textarea.insert(END,f"\t{tamt.get()}\n")
            
        


        cod.set('')
        nam.set('')
        mrp1.set('')
        qty1.set('')
        opr.set('')
        tamt.set('')

    def finish():
        textarea.insert(END,"********************************************************\n")
        textarea.insert(END,f"\t\t     GRAND TOTAL: {GGTOT}\n")
        textarea.insert(END,f"\nCashier:{admin_id.get()}\t\t\tTime:{ntime}\n")
        textarea.insert(END,"********************************************************\n")
        textarea.insert(END,"\t            THANK YOU\n\tFOR SHOPPING WITH US\n")
        textarea.insert(END,"____________________________________\n")
        grtotal.set(GGTOT)
        
    def additm():    #add item button

        def adddata():
            cursor.execute("""insert into stock values({},"{}",{},{},{})""".format(itcodeety.get(),itnameety.get(),itqtyety.get(),itMRPety.get(),itoprcety.get()))
            mysqldb.commit()

            itcodeety.delete(0,END)
            itnameety.delete(0,END)
            itMRPety.delete(0,END)
            itqtyety.delete(0,END)
            itoprcety.delete(0,END)

            treedata.delete(*treedata.get_children())      #*=splat used for unpacking iterable objects

            data()
            

        def data():
            cursor.execute("select * from stock")
            data=cursor.fetchall()

            global cnt
            cnt=0

            for x in data:
                if cnt%2==0:
                    treedata.insert(parent='',index='end',iid=cnt,text='',values=(x[0],x[1],x[3],x[2],x[4]))
                else:
                    treedata.insert(parent='',index='end',iid=cnt,text='',values=(x[0],x[1],x[3],x[2],x[4]))

                cnt+=1
           
    
        def selectrec(e):
            itcodeety.delete(0,END)
            itnameety.delete(0,END)
            itMRPety.delete(0,END)
            itqtyety.delete(0,END)
            itoprcety.delete(0,END)

            selected=treedata.focus()
            values=treedata.item(selected, "values")
            itcodeety.insert(0,values[0])
            itnameety.insert(0,values[1])
            itMRPety.insert(0,values[2])
            itqtyety.insert(0,values[3])
            itoprcety.insert(0,values[4])


        
        sub1=Toplevel()
        sub1.title("ADD ITEM")
        sub1.geometry("900x530")
        
        style=ttk.Style()

        style.theme_use("default")   #theme

        style.configure("Treeview",bg="#D3D3D3",fg="black",rowheight=25,feildbackground="#D3D3D3")


        treeframe=Frame(sub1)           #frame
        treeframe.pack(pady=10)

        treescroll=Scrollbar(treeframe)    #scrollbar
        treescroll.pack(side=RIGHT,fill=Y)

        treedata=ttk.Treeview(treeframe,yscrollcommand=treescroll.set,selectmode="extended")
        treedata.pack()

        treescroll.config(command=treedata.yview)

        treedata['columns']=("item code","item name","MRP","quantity","our price")

        treedata.column("#0",width=0,stretch=NO)
        treedata.column("item code",anchor=W,width=100)
        treedata.column("item name",anchor=CENTER,width=250)
        treedata.column("MRP",anchor=CENTER,width=100)
        treedata.column("quantity",anchor=CENTER,width=120)
        treedata.column("our price",anchor=CENTER,width=120)

        treedata.heading("#0",text='',anchor=W)
        treedata.heading("item code",text='item code',anchor=CENTER)
        treedata.heading("item name",text='item name',anchor=CENTER)
        treedata.heading("MRP",text='MRP',anchor=CENTER)
        treedata.heading("quantity",text='quantity',anchor=CENTER)
        treedata.heading("our price",text='our price',anchor=CENTER)



        inputfrm=LabelFrame(sub1,text="INPUT")
        inputfrm.pack(fill="x",expand="yes",padx=20)

        itcodelbl=Label(inputfrm,text="item code")
        itcodelbl.grid(row=0,column=0,padx=10,pady=10)
        itcodeety=Entry(inputfrm)
        itcodeety.grid(row=0,column=1,padx=10,pady=10)
        
        itnamelbl=Label(inputfrm,text="item name")
        itnamelbl.grid(row=0,column=2,padx=10,pady=10)
        itnameety=Entry(inputfrm)
        itnameety.grid(row=0,column=3,padx=10,pady=10)

        
        itMRPlbl=Label(inputfrm,text="MRP")
        itMRPlbl.grid(row=0,column=4,padx=10,pady=10)
        itMRPety=Entry(inputfrm)
        itMRPety.grid(row=0,column=5,padx=10,pady=10)

        
        itqtylbl=Label(inputfrm,text="quantity")
        itqtylbl.grid(row=1,column=0,padx=10,pady=10)
        itqtyety=Entry(inputfrm)
        itqtyety.grid(row=1,column=1,padx=10,pady=10)


        itoprclbl=Label(inputfrm,text="our price")
        itoprclbl.grid(row=1,column=2,padx=10,pady=10)
        itoprcety=Entry(inputfrm)
        itoprcety.grid(row=1,column=3,padx=10,pady=10)


        addbtn=Button(sub1,text="ADD NEW ITEM",command=adddata,bd=3,width=40)
        addbtn.pack(pady=40)

        treedata.bind("<ButtonRelease-1>",selectrec)

        data()
        
        status=Label(sub1,text="Add item Page",bd=1,relief=SUNKEN,anchor=E).pack(side=BOTTOM,fill=X)
        sub1.mainloop()




    def removeitm():            #remove item button


        def remdata():
            cursor.execute("delete from stock where product_code={}".format(values[0]))
            mysqldb.commit()

            treedata.delete(*treedata.get_children())      #*=splat

            data()

            messagebox.showinfo("DELETED!!","Your Item has been deleted!")


        def remalldata():
            resp=messagebox.askquestion("Are you sure?","Do you want to delete all items?")
            if resp=="yes":
                cursor.execute("delete from stock")
                mysqldb.commit()

                treedata.delete(*treedata.get_children())      #*=splat

                data()
        


        def data():
            cursor.execute("select * from stock")
            data=cursor.fetchall()

            global cnt
            cnt=0

            for x in data:
                if cnt%2==0:
                    treedata.insert(parent='',index='end',iid=cnt,text='',values=(x[0],x[1],x[3],x[2],x[4]))
                else:
                    treedata.insert(parent='',index='end',iid=cnt,text='',values=(x[0],x[1],x[3],x[2],x[4]))

                cnt+=1
           



        def selectrec(e):
            global values
            selected=treedata.focus()
            values=treedata.item(selected, "values")

        
        sub1=Toplevel()
        sub1.title("REMOVE ITEM")
        sub1.geometry("800x430")
        
        style=ttk.Style()

        style.theme_use("default")   #theme

        style.configure("Treeview",bg="#D3D3D3",fg="black",rowheight=25,feildbackground="#D3D3D3")

        treeframe=Frame(sub1)           #frame
        treeframe.pack(pady=10)

        treescroll=Scrollbar(treeframe)    #scrollbar
        treescroll.pack(side=RIGHT,fill=Y)

        treedata=ttk.Treeview(treeframe,yscrollcommand=treescroll.set,selectmode="extended")
        treedata.pack()

        treescroll.config(command=treedata.yview)

        treedata['columns']=("item code","item name","MRP","quantity","our price")

        treedata.column("#0",width=0,stretch=NO)
        treedata.column("item code",anchor=W,width=100)
        treedata.column("item name",anchor=CENTER,width=250)
        treedata.column("MRP",anchor=CENTER,width=100)
        treedata.column("quantity",anchor=CENTER,width=120)
        treedata.column("our price",anchor=CENTER,width=120)

        treedata.heading("#0",text='',anchor=W)
        treedata.heading("item code",text='item code',anchor=CENTER)
        treedata.heading("item name",text='item name',anchor=CENTER)
        treedata.heading("MRP",text='MRP',anchor=CENTER)
        treedata.heading("quantity",text='quantity',anchor=CENTER)
        treedata.heading("our price",text='our price',anchor=CENTER)


        rembtn=Button(sub1,text="REMOVE SELECTED ITEM",command=remdata,bd=3,width=40)
        rembtn.pack(pady=15)

        remallbtn=Button(sub1,text="REMOVE ALL ITEMS",command=remalldata,bd=3,width=20,bg="red")
        remallbtn.pack(pady=5,anchor=S)
        
        treedata.bind("<ButtonRelease-1>",selectrec)

        data()
        
        status=Label(sub1,text="Remove item Page",bd=1,relief=SUNKEN,anchor=E).pack(side=BOTTOM,fill=X)
        sub1.mainloop()




    def modifyitm():      #modify item button

        def moddata():
            selected=treedata.focus()
            treedata.item(selected,text='',value=(itcodeety.get(),itnameety.get(),itMRPety.get(),itqtyety.get(),itoprcety.get(),))

            cursor.execute("""update stock set product_name='{x}',product_quantity={y},purchase_price={z},selling_price={a}
                where product_code={b}""".format(x=itnameety.get(),y=itqtyety.get(),z=itMRPety.get(),a=itoprcety.get(),b=itcodeety.get()))
            mysqldb.commit()

            itcodeety.delete(0,END)
            itnameety.delete(0,END)
            itMRPety.delete(0,END)
            itqtyety.delete(0,END)
            itoprcety.delete(0,END)
        

        def data():
            cursor.execute("select * from stock")
            data=cursor.fetchall()
            
            global cnt
            cnt=0

            for x in data:
                
                if cnt%2==0:
                    treedata.insert(parent='',index='end',iid=cnt,text='',values=(x[0],x[1],x[3],x[2],x[4]))
                else:
                    treedata.insert(parent='',index='end',iid=cnt,text='',values=(x[0],x[1],x[3],x[2],x[4]))

                cnt+=1       
            

        def selectrec(e):
            itcodeety.delete(0,END)
            itnameety.delete(0,END)
            itMRPety.delete(0,END)
            itqtyety.delete(0,END)
            itoprcety.delete(0,END)

            selected=treedata.focus()
            values=treedata.item(selected, "values")
            itcodeety.insert(0,values[0])
            itnameety.insert(0,values[1])
            itMRPety.insert(0,values[2])
            itqtyety.insert(0,values[3])
            itoprcety.insert(0,values[4])


        
        sub1=Toplevel()
        sub1.title("MODIFY ITEM")
        sub1.geometry("900x530")
        
        style=ttk.Style()

        style.theme_use("default")   #theme

        style.configure("Treeview",bg="#D3D3D3",fg="black",rowheight=25,feildbackground="#D3D3D3")


        treeframe=Frame(sub1)           #frame
        treeframe.pack(pady=10)

        treescroll=Scrollbar(treeframe)    #scrollbar
        treescroll.pack(side=RIGHT,fill=Y)

        treedata=ttk.Treeview(treeframe,yscrollcommand=treescroll.set,selectmode="extended")
        treedata.pack()

        treescroll.config(command=treedata.yview)

        treedata['columns']=("item code","item name","MRP","quantity","our price")

        treedata.column("#0",width=0,stretch=NO)
        treedata.column("item code",anchor=W,width=100)
        treedata.column("item name",anchor=CENTER,width=250)
        treedata.column("MRP",anchor=CENTER,width=100)
        treedata.column("quantity",anchor=CENTER,width=120)
        treedata.column("our price",anchor=CENTER,width=120)

        treedata.heading("#0",text='',anchor=W)
        treedata.heading("item code",text='item code',anchor=CENTER)
        treedata.heading("item name",text='item name',anchor=CENTER)
        treedata.heading("MRP",text='MRP',anchor=CENTER)
        treedata.heading("quantity",text='quantity',anchor=CENTER)
        treedata.heading("our price",text='our price',anchor=CENTER)

        inputfrm=LabelFrame(sub1,text="INPUT")
        inputfrm.pack(fill="x",expand="yes",padx=20)

        itcodelbl=Label(inputfrm,text="item code")
        itcodelbl.grid(row=0,column=0,padx=10,pady=10)
        itcodeety=Entry(inputfrm)
        itcodeety.grid(row=0,column=1,padx=10,pady=10)
        
        itnamelbl=Label(inputfrm,text="item name")
        itnamelbl.grid(row=0,column=2,padx=10,pady=10)
        itnameety=Entry(inputfrm)
        itnameety.grid(row=0,column=3,padx=10,pady=10)

        
        itMRPlbl=Label(inputfrm,text="MRP")
        itMRPlbl.grid(row=0,column=4,padx=10,pady=10)
        itMRPety=Entry(inputfrm)
        itMRPety.grid(row=0,column=5,padx=10,pady=10)

        
        itqtylbl=Label(inputfrm,text="quantity")
        itqtylbl.grid(row=1,column=0,padx=10,pady=10)
        itqtyety=Entry(inputfrm)
        itqtyety.grid(row=1,column=1,padx=10,pady=10)


        itoprclbl=Label(inputfrm,text="our price")
        itoprclbl.grid(row=1,column=2,padx=10,pady=10)
        itoprcety=Entry(inputfrm)
        itoprcety.grid(row=1,column=3,padx=10,pady=10)

        modbtn=Button(sub1,text="MODIFY ITEM",command=moddata,bd=3,width=30)
        modbtn.pack(pady=40)

        treedata.bind("<ButtonRelease-1>",selectrec)

        data()
        
        status=Label(sub1,text="Modify item Page",bd=1,relief=SUNKEN,anchor=E).pack(side=BOTTOM,fill=X)
        sub1.mainloop()

    def totfitem():
        totitmprc=int(qty1.get())*int(opr.get())
        tamt.set(int(totitmprc))

    def newf():
        cname.set("")
        phoneno.set("")
        grtotal.set("")
        cod.set('')
        nam.set('')
        mrp1.set('')
        qty1.set('')
        opr.set('')
        tamt.set('')
        clear()

    def comboclick(e):
        cursor.execute("select product_code,purchase_price,selling_price from stock where product_name='{}'".format(nam.get()))
        data=cursor.fetchall()
        cod.set(data[0][0])
        mrp1.set(data[0][1])
        opr.set(data[0][2])
   
    def clear():
        textarea.delete(1.0,END)       #** txtarea staring from=1.0

    
    main=Toplevel()
    main.title("billing software")
    main.geometry("1245x645")
            
    frmA=LabelFrame(main, text="DETAILS",relief="ridge",fg="black",bg="#edebe1",bd=5)   #code=hex colour code
    frmA.place(x=0,y=0,relwidth=1)

    now=datetime.datetime.now()
    ndate=now.strftime("%d-%m-%y")
    ntime=now.strftime("%H:%M:%S")
    day=now.strftime("%A")

    dy=Label(frmA,text="DAY:-",font=("geordia bold",10),bg="#edebe1").grid(row=0,column=0)
    dyselected=StringVar()
    dyselected.set(day)
    dydrop=OptionMenu(frmA,dyselected,"Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday").grid(row=0,column=1)

    date=Label(frmA,text="DATE:-",font=("geordia bold",10),bg="#edebe1").grid(row=1,column=0)
    dateselected=StringVar()
    dateselected.set(ndate)
    datenow=Entry(frmA,textvariable=dateselected,width=8,font="american 14",relief=SUNKEN,bd=1).grid(row=1,column=1)
    
    pay=Label(frmA,text="PAYMENT:-",font=("geordia bold",10),bg="#edebe1").grid(row=2,column=0)
    payselected=StringVar()
    payselected.set("Cash")
    paydrop=OptionMenu(frmA,payselected,"Cash","Credit Card","Debit Card","Google Pay","Bharat Pe").grid(row=2,column=1)

    labelspace=Label(frmA,text="       ",bg="#edebe1").grid(row=1,column=2)#between date and name
    
    customers_name=Label(frmA,text="CUSTOMERS:-",font=("geordia bold",10),bg="#edebe1").grid(row=0,column=3)
    cname=StringVar()
    name_entry=Entry(frmA,textvariable=cname,width=19,font="american 14",relief=SUNKEN,bd=2).grid(row=0,column=4)

    
    phone_no=Label(frmA,text="PHONE:-",font=("geordia bold",10),bg="#edebe1").grid(row=1,column=3)
    phoneno=IntVar()
    phoneno.set('')
    phone_entry=Entry(frmA,textvariable=phoneno,width=19,font="american 14",relief=SUNKEN,bd=2).grid(row=1,column=4)

    new=Button(frmA,text="NEW",command=newf,padx=40,pady=7,bd=2).grid(row=2,column=3,rowspan=2,pady=10)

    save=Button(frmA,text="SAVE",command=saveall,padx=40,pady=7,bd=2).grid(row=2,column=4,rowspan=2,pady=10)

    labelspace1=Label(frmA,text="                       ",bg="#edebe1").grid(row=0,column=5)#disstance between the buttons
    labelspace2=Label(frmA,text="                       ",bg="#edebe1").grid(row=0,column=7)
    labelspace3=Label(frmA,text="                       ",bg="#edebe1").grid(row=0,column=9)

    add_item=Button(frmA,text="ADD ITEM",command=additm,padx=33,pady=15,bd=2).grid(row=0,column=6,rowspan=2)

    remove_item=Button(frmA,text="REMOVE ITEM",command=removeitm,padx=23,pady=15,bd=2).grid(row=0,column=8,rowspan=2)

    modify_stock=Button(frmA,text="MODIFY STOCK",command=modifyitm,padx=20,pady=15,bd=2).grid(row=0,column=10,rowspan=2)


    frmB=LabelFrame(main, text="BILLING",relief="ridge",fg="black",bg="#edebe1",bd=5)   #code=hex colour code
    frmB.place(x=0,y=138)

    code=Label(frmB,text="CODE",font=("geordia bold",10),bg="#c9cb8f",width=10).grid(row=0,column=0)
    cod=IntVar()
    cod.set('')
    cd=Entry(frmB,textvariable=cod,width=10,font=('Arial',10,'bold')).grid(row=1,column=0)

    totitm=Button(frmB,text="TOTAL FOR ITEM",padx=40,command=totfitem,pady=7,bd=2).grid(row=3,column=2,columnspan=2,pady=10)

    sitmtobill=Button(frmB,text="SAVE ITEM INTO BILL",command=intobill,padx=40,pady=7,bd=2).grid(row=3,column=4,columnspan=4,pady=10)

    name=Label(frmB,text="NAME",font=("geordia bold",10),bg="#c9cb8f",width=30).grid(row=0,column=1,padx=5)
    nam=StringVar()
    cursor.execute("select product_name from stock")
    downitem=tuple(cursor.fetchall())
    itnm=ttk.Combobox(frmB,textvariable=nam,width=33,font=('Arial',10,'bold'),values=downitem)
    itnm.grid(row=1,column=1)                                                                        

    mrp=Label(frmB,text="MRP",font=("geordia bold",10),bg="#c9cb8f",width=13).grid(row=0,column=2)
    mrp1=IntVar()
    mrp1.set('')
    itmr=Entry(frmB,textvariable=mrp1,width=15,font=('Arial',10,'bold')).grid(row=1,column=2)

    qty=Label(frmB,text="QTY",font=("geordia bold",10),bg="#c9cb8f",width=11).grid(row=0,column=3,padx=5)
    qty1=IntVar()
    qty1.set('')
    itqt=Entry(frmB,textvariable=qty1,width=13,font=('Arial',10,'bold'))
    itqt.grid(row=1,column=3) 

    ouprice=Label(frmB,text="OUR PRICE",font=("geordia bold",10),bg="#c9cb8f",width=13).grid(row=0,column=4)
    opr=IntVar()
    opr.set('')
    ourprice=Entry(frmB,textvariable=opr,width=14,font=('Arial',10,'bold')).grid(row=1,column=4)

    totamt=Label(frmB,text="TOTAL AMOUNT",font=("geordia bold",10),bg="#c9cb8f",width=15).grid(row=0,column=5,padx=5)
    tamt=IntVar()
    tamt.set('')
    totalamt=Entry(frmB,textvariable=tamt,width=17,font=('Arial',10,'bold')).grid(row=1,column=5)
    

    frmC=LabelFrame(main, text="",relief="ridge",fg="black",bg="#edebe1",bd=5)   #code=hex colour code
    frmC.place(x=817,y=139)


    
    bill_hed=Label(frmC,text='Bill',font=('arial',15,'bold'),bd=8,relief=GROOVE,width=32).pack(fill=X)
    scroll=Scrollbar(frmC,orient=VERTICAL)
    scroll.pack(side=RIGHT,fil=Y)
    textarea=Text(frmC,font=('arial','14'),height=13,width=36,yscrollcommand=scroll.set)
    textarea.pack(fill=BOTH,expand=1)
    scroll.config(command=textarea.yview)
    clr=Button(frmC,text="CLEAR",command=clear,pady=7,bd=4,width=15).pack(side=LEFT,expand=True)
    fns=Button(frmC,text="FINISH",command=finish,pady=7,bd=4,width=15).pack(side=RIGHT,expand=True)


    frmD=LabelFrame(main, text="TOTAL",relief="ridge",fg="black",bg="#edebe1",bd=5,width=50,height=99)
    frmD.place(x=0,y=525,relwidth=1)

    totamt=Label(frmD,text="TOTAL AMOUNT:-",font=("geordia bold",15),bg="#edebe1").place(x=850,y=25)
    grtotal=IntVar()
    grtotal.set('')
    totamtnow=Entry(frmD,textvariable=grtotal,width=15,font="american 14",relief=SUNKEN,bd=3).place(x=1025,y=28)

    crtuser=Label(frmD,text="current user:-",font=("geordia bold",10),bg="#edebe1").place(x=5,y=45)
    admin_id1=StringVar()
    admin_id1.set(admin_id.get())#.get() should be used 
    crtusernow=Entry(frmD,textvariable=admin_id1,width=10,font="american 14",relief=SUNKEN,bd=1).place(x=90,y=38)


    status=Label(main,text="Billing Page",bd=1,relief=SUNKEN,anchor=E).pack(side=BOTTOM,fill=X)

    itnm.bind("<<ComboboxSelected>>",comboclick)
    
    main.mainloop()
            


root=Tk()
root.title("MP Enterprises")
root.iconbitmap("c:/Users/user/Downloads/unnamed.ico")
root.geometry("900x500")


admin_id=StringVar()
id=Label(root,text="Enter your admin id:",font=("geordia bold",15,"bold")).place(x=260,y=150)
admin_id.set("mpadmin1")
idtxt=Entry(root,width=15,textvariable=admin_id,font="american 14",relief=SUNKEN,bd=2).place(x=470,y=150)


admin_passwd=StringVar()
passwd=Label(root,text="Enter your password:",font=("geordia bold",15,"bold")).place(x=250,y=200)
admin_passwd.set("123")
passwdtxt=Entry(root,width=15,textvariable=admin_passwd,font="american 14",relief=SUNKEN,bd=2).place(x=470,y=200)

trm_cond=Checkbutton(root,text="I Agree to the Terms and Conditions.").place(x=330,y=300)

status=Label(root,text="Login Page",bd=1,relief=SUNKEN,anchor=E).pack(side=BOTTOM,fill=X)

loginbtton=Button(root,text="Login",command=login,padx=70,pady=10,bd=4).place(x=350,y=250)

root.mainloop()


           
   


