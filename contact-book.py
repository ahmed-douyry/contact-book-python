from tkinter import * 
from tkinter import ttk


from sqlite3 import *
from tkinter import messagebox
class Contact:
    def __init__(self,root):
            
            self.root=root
            self.search_by=StringVar()
            self.search_txt=StringVar()
            root.geometry("1400x750+10+10")
            root.iconbitmap("aa.ico")
            root.title('contact book ')
            title=Label(root,text="The Contacts Book",bd=10,relief=GROOVE,font=("times new roman",30,"bold"),bg="purple" , fg="white")
            title.pack(side=TOP,fill=X)
            self.name_var=StringVar()
            self.Number = StringVar()
            self.ID = StringVar()
            Manage_Frame=Frame(root,bd=4,relief=RIDGE,bg="mint cream")
            Manage_Frame.place(x=10,y=100,width=500,height=400)
            m_title=Label(Manage_Frame,text="Welcome to our Contact Book",fg="black",font=("times new roman",20,"bold"))
            m_title.grid(row=0,columnspan=2,pady=15)
            lbl_name=Label(Manage_Frame,text="Name*    :",fg="black",font=("times new roman",15,"bold"))
            lbl_name.grid(row=1,column=0,pady=5,padx=30,sticky="w")
            txt_name=Entry(Manage_Frame,textvariable=self.name_var,font=("times new roman",15,"bold"),bd=3,relief=GROOVE)
            txt_name.grid(row=1,column=1,pady=5,padx=30,sticky="w")
            
            lbl_Number=Label(Manage_Frame,text="Number* :",fg="black",font=("times new roman",15,"bold"))
            lbl_Number.grid(row=4,column=0,pady=5,padx=30,sticky="w")
            txt_Number=Entry(Manage_Frame,textvariable=self.Number,font=("times new roman",14,"bold"),bd=5,relief=GROOVE)
            txt_Number.grid(row=4,column=1,pady=70,padx=30,sticky="w")
            lbl_footer = Label(root, text="Developed by douyrys", font=("goudy old style", 15, "bold"),
            bg="purple", fg="white").place(x=0, y=710, relwidth=1, height=40)
            
            Btn_Frame=Frame(Manage_Frame,bd=4,relief=RIDGE,bg="mint cream")
            Btn_Frame.place(x=10,y=250,width=450)
            addbtn=Button(Btn_Frame,text="Add",font=("times new roman",12,"bold"),width=10,bg="purple",fg="white",command=self.add_contacts).grid(row=0,column=0,padx=5,pady=5)
            updatebtn=Button(Btn_Frame,text="Update",font=("times new roman",12,"bold"),bg="purple",fg="white",width=10,command=self.update_data).grid(row=0,column=1,padx=5,pady=5)

            deletebtn=Button(Btn_Frame,text="Delete",font=("times new roman",12,"bold"),bg="purple",fg="white",width=10,command=self.delete_data).grid(row=0,column=2,padx=5,pady=5)
            clearbtn=Button(Btn_Frame,text="Clear",font=("times new roman",12,"bold"),bg="purple",fg="white",width=10,command=self.clear).grid(row=0,column=3,padx=5,pady=5)
            lbl_msg=Label(Manage_Frame,text="*Means Required fields",fg="black",font=("times new roman",15,"bold"))
            lbl_msg.grid(row=8,columnspan=2,pady=30)
            

            
        #detail frame
            Details_Frame=Frame(self.root,bd=4,relief=RIDGE,bg="mint cream")
            Details_Frame.place(x=525,y=100,width=850,height=600)
            
            lbl_search=Label(Details_Frame,text="Search",bg="mint cream",fg="black",font=("times new roman",20,"bold"))
            lbl_search.grid(row=0,column=0,pady=10,padx=30,sticky="w")
            combo_search=ttk.Combobox(Details_Frame,width=10,textvariable=self.search_by,font=("times new roman",13,"bold"),state="readonly")
            combo_search['values']=("Name","Number")
            combo_search.grid(row=0,column=1,padx=30,pady=10,sticky="w")
            txt_search=Entry(Details_Frame,textvariable=self.search_txt,width=20,font=("times new roman",10,"bold"),bd=5,relief=GROOVE)
            txt_search.grid(row=0,column=2,pady=10,padx=30,sticky="w")
            searchbtn=Button(Details_Frame,text="Search",bg="purple",fg="white",font=("times new roman",12,"bold"),command=self.search_data,width=10,pady=5).grid(row=0,column=3,padx=10,pady=10)
            showallbtn=Button(Details_Frame,text="Showall",bg="purple",fg="white",font=("times new roman",12,"bold"),command=self.fetch_data,width=10,pady=5).grid(row=0,column=4,padx=10,pady=10)
            
            #Table frame
            Table_Frame=Frame(Details_Frame,bd=4,relief=RIDGE,bg="mint cream")
            Table_Frame.place(x=10,y=70,width=800,height=500)
            scroll_x=Scrollbar(Table_Frame,orient=HORIZONTAL)
            scroll_y=Scrollbar(Table_Frame,orient=VERTICAL)
            self.contacts_table=ttk.Treeview(Table_Frame,columns=("ID","Name","Number"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
            scroll_x.pack(side=BOTTOM,fill=X)
            scroll_y.pack(side=RIGHT,fill=Y)
            scroll_x.config(command=self.contacts_table.xview)
            scroll_y.config(command=self.contacts_table.yview)
            self.contacts_table.heading("ID",text="ID")
            self.contacts_table.heading("Name",text="Name")
            self.contacts_table.heading("Number",text="Number")
            self.contacts_table['show']="headings"
            self.contacts_table.column("ID",width=50)
            self.contacts_table.column("Name",width=150)
            self.contacts_table.column("Number",width=150)
            self.contacts_table.pack(fill=BOTH,expand=1)
            self.contacts_table.bind("<ButtonRelease-1>",self.get_cursor)
            self.fetch_data()

    
    def checkvalidNumber(phone_number):
        if(len (phone_number) < 10 or len (phone_number) > 13):
            return False
        T={"-":0,"+":0,"_":0}
        for i in str(phone_number):
            if i in list(T.keys()):
                if (i=="_" or i=="-") and (T["-"]>=1 or T['_']>=1):
                    return False
                elif i=="+" and T[i]>=1:
                    return False
                else:
                    T[i]+=1
            elif not i.isdigit():
                return False
        return True

    def add_contacts(self):
            numbre = Contact.checkvalidNumber(self.Number.get())
            if (numbre == False):
                messagebox.showerror("Error","invalid phone number")
            elif(self.name_var.get()==""  or self.Number.get()==""): 
                messagebox.showerror("Error","Required fields are not filled")
            
            else:
                conn=connect("contacts.db")
                cur=conn.cursor()
                cur.execute("insert into contacts values(?,?,?)",(None, self.name_var.get(), self.Number.get()))
                conn.commit()
                self.fetch_data()
                self.clear()
                conn.close()
                messagebox.showinfo("Success", "Successfully added")
    def fetch_data(self):
            conn=connect("contacts.db")
            cur=conn.cursor()
            cur.execute("SELECT * FROM contacts")
            rows=cur.fetchall()
            if len(rows)!=0:
                self.contacts_table.delete(*self.contacts_table.get_children())
                for row in rows:
                    self.contacts_table.insert('', END,values=row)
                conn.commit()
            conn.close()
    def clear(self):
            self.name_var.set("")
            self.Number.set("")
    def get_cursor(self,ev):
            cursor_row=self.contacts_table.focus()
            content=self.contacts_table.item(cursor_row)
            row=content['values']

            self.ID.set(row[0])
            self.name_var.set(row[1])
            self.Number.set(row[2])
            
    def update_data(self):
            if(self.name_var.get()==""or self.Number.get()==""): 
                messagebox.showerror("Error","Required fields are not filled")
            else:
                conn=connect("contacts.db")
                cur=conn.cursor()
                cur.execute("update contacts set  Name=?, Number=? WHERE id =? ",(self.name_var.get(),self.Number.get(), self.ID.get()))
                conn.commit()
                self.fetch_data()
                self.clear()
                conn.close()
                messagebox.showinfo("Success","Successfully updated")
    def delete_data(self):
        if(self.name_var.get()=="" or self.Number.get()==""): 
            messagebox.showerror("Error","Required fields empty")
        else:
            conn=connect("contacts.db")
            cur=conn.cursor()
            sql_query=f"delete FROM contacts where ID={self.ID.get()}"
            
            cur.execute(sql_query)
            
            conn.commit()
            conn.close()
            self.clear()
            self.fetch_data()
            messagebox.showinfo("Success","Successfully Deleted")       
    def search_data(self):
            conn=connect("contacts.db")
            cur=conn.cursor()
            sql_query=f"SELECT * FROM contacts where {self.search_by.get()} like '%{self.search_txt.get()}%'"
            
            cur.execute(sql_query)
            rows=cur.fetchall()
            if len(rows)!=0:
                self.contacts_table.delete(*self.contacts_table.get_children())
                for row in rows:
                    self.contacts_table.insert('',END,values=row)
                conn.commit()
            else:
                messagebox.showerror("Error","No Data available")
                self.search_by.set("")
                self.search_txt.set("")
            conn.close()
root = Tk()
con=connect('contacts.db')
cur=con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS contacts( ID integer PRIMARY KEY AUTOINCREMENT, Name text NOT NULL, Number text NOT NULL UNIQUE); ")
con.commit()
con.close()
ob = Contact(root)
root.mainloop()
