from tkinter import *
from tkinter.ttk import Combobox
import sys
from src.modules import *
import glob

df = pd.DataFrame()


def load():
    try:
        dataset_watch.place_forget()
        dataset_watch.pack()

        global x_box, y_box, df, selected_y, selected_x

        df = drop_na(pd.read_csv(files_cmb.get() + '.csv'))
        dataset_summarize.set(df)

        dataset_lbl.place_forget()
        files_cmb.place_forget()
        load_btn.place_forget()

        columns = df.columns

        x_axis_lbl.pack()

        x_box = Combobox(values=tuple(columns), font=('TimesNewRoman', 12))
        x_box.bind("<<ComboboxSelected>>", setx)
        x_box.current(0)
        x_box.pack()
        selected_x = x_box.get()

        y_axis_lbl.pack()

        y_box = Combobox(values=tuple(columns), font=('TimesNewRoman', 12))
        y_box.bind("<<ComboboxSelected>>", sety)
        y_box.current(1)
        y_box.pack()
        selected_y = y_box.get()

        plot_btn.pack()

        back_btn.place(x=10, y=100)

    except:
        err_msg = 'Data Set Not Found !'
        dataset_summarize.set(err_msg)
        logger.log_error(err_msg)
        dataset_watch.place(x=350, y=200)


def sety(event):
    global selected_y
    selected_y = y_box.get()


def setx(event):
    global selected_x
    selected_x = x_box.get()


def show_plot():
    plot_2d(df, x=selected_x, y=selected_y, trendline=True)


def init_place():
    dataset_lbl.place(x=250, y=100)
    files_cmb.place(x=400, y=100)
    load_btn.place(x=350, y=150)


def back():
    try:
        back_btn.place_forget()
        init_place()
        x_box.pack_forget()
        y_box.pack_forget()
        x_axis_lbl.pack_forget()
        y_axis_lbl.pack_forget()
        dataset_watch.pack_forget()
        plot_btn.pack_forget()
    except:
        pass
    init_place()


files = [x.replace('.csv', '') for x in glob.glob('../data_sets/*.csv')]

screen = Tk()
screen.geometry('800x800')
screen.title('visualisation')

heading = Label(text='CSss 2019', bg='grey', fg='black', width='500', height='3', font=('TimesNewRoman', 20))
heading.pack()

dataset_lbl = Label(text='Data Set Name:', font=('TimesNewRoman', 15))

files_cmb = Combobox(values=tuple(files), font=('TimesNewRoman', 12))
files_cmb.current(0)
files_cmb.pack()


load_btn = Button(text='Load Data', command=load, font=('TimesNewRoman', 13))

dataset_summarize = StringVar()
dataset_watch = Label(textvariable=dataset_summarize, font=('TimesNewRoman', 13))


x_axis_lbl = Label(text='X axis', font=('TimesNewRoman', 12))
y_axis_lbl = Label(text='Y axis', font=('TimesNewRoman', 12))

x_box = Combobox()
y_box = Combobox()

selected_x = ''
selected_y = ''

plot_btn = Button(text='SHOW PLOT', font=('TimesNewRoman', 18), command=show_plot)

back()
back_btn = Button(text='Back', font=('TimesNewRoman', 18), command=back)


screen.mainloop()
