import tkinter as tk
from tkinter import *
import dns
import dns.resolver, dns.reversename

class NoEntry(Exception):
    pass

class DoubleEntry(Exception):
    pass

root = Tk()
root.title("DNS Resolver")

window_width = 355
window_height = 200

# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.resizable(False, False)
root.iconbitmap('./emoryFav.ico')

# configure the grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=5)

# store either domain name or ip address
name = StringVar()
ip = StringVar()
outputText = StringVar()

# forward dns lookup
nameLabel = Label(root, text='Name :')
nameLabel.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

nameEntry = Entry(root, width=55)
nameEntry.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

# reverse dns lookup
ipLabel = Label(root, text='IP :')
ipLabel.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

ipEntry = Entry(root, width=55)
ipEntry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

# resolve info
outputLabel = Label(root, font=("Arial", 12), textvariable=outputText, wraplength=300, justify=LEFT)
outputLabel.grid(column=0, columnspan=2, row=3, sticky=tk.W, padx=5, pady=5)

# frame to hold all buttons in one cell
gridframe = Frame(root)

# clear all text from display
def clear_clicked():
    outputText.set("")
    nameEntry.delete(0, END)
    ipEntry.delete(0, END)

# clear display button
clearButton = Button(gridframe, text="Clear", command=clear_clicked)
clearButton.pack(side=tk.RIGHT)
    
# copy result to clipboard
def copy_clicked():
    root.clipboard_clear()
    root.clipboard_append(outputText.get())
    root.update()

# copy button
copyButton = Button(gridframe, text="Copy", command=copy_clicked)
#copyButton.grid(column=0, row=2, sticky=tk.E, padx=5, pady=5)
copyButton.pack(side=tk.RIGHT)

# find dns record
def resolve_clicked():
    try:
        if nameEntry.get() != '' and ipEntry.get() != '':
            raise DoubleEntry()
        elif nameEntry.get() != '':
            name = nameEntry.get()
            result = dns.resolver.resolve(name, 'A')
            nameText = StringVar()
            for ipval in result:
                nameText ="\nIP:         " + ipval.to_text()
            labelText = "Name:  " + name + nameText
            outputText.set(labelText)
        elif ipEntry.get() != '':
            ip = ipEntry.get()
            result = dns.reversename.from_address(ip)
            result = dns.resolver.resolve(result, "PTR")
            ipText = StringVar()
            for ipval in result:
                ipText = "Name: " + ipval.to_text()
            labelText = ipText + "\nIP:         " + ip
            outputText.set(labelText)
        else:
            raise NoEntry()
    except DoubleEntry:
        error = "Only one record is needed."
        outputText.set(error)
    except NoEntry:
        error = "There was no information entered."
        outputText.set(error)
    except:
        error = "Invalid input. Please try again."
        outputText.set(error)

# resolve button
resolveButton = Button(gridframe, text="Resolve", command=resolve_clicked)
#resolveButton.grid(column=1, row=2, sticky=tk.E, padx=5, pady=5)
resolveButton.pack(side=tk.RIGHT)

gridframe.grid(column=1, row=2, sticky=tk.E, padx=5, pady=5)

root.mainloop()
