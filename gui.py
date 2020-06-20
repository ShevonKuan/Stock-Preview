import tkinter as tk
import tkinter.messagebox
import main
import requests
window = tk.Tk()
window.title('stock')
window.geometry('1280x720')
l = tk.Label(window,
             text='Hello, this is a simple stock information acquisition software, please enter the stock code in the form below.',
             font=('Arial', 16))
l.pack()
e = tk.Entry(window, show=None, font=('Arial', 20))
e.pack()


def insert():
    '''data transport to $var'''
    #global var
    var = e.get()
    try:
        main.main(var)
    except:
        tk.messagebox.showerror(title='Some thing error', message='Can\'t find the stock, please retry.')


    #t.insert('end', var)
b = tk.Button(window, text='Search', width=10,
              height=2, command=insert)
b.pack()
#t = tk.Text(window, height=3)
# t.pack()
window.mainloop()
