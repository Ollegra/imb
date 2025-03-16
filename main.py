import ttkbootstrap as ttk


def mcasse_bmi(bmi):
    match bmi:
        case bmi if bmi < 16:
            return "Очень большой дефицит массы тела", "info"
        case bmi if bmi >= 16 and bmi < 17:
            return "Выраженный дефицит массы тела", "info"
        case bmi if bmi >= 17 and bmi < 18.5:
            return "Недостаточная масса тела", "primary"
        case bmi if bmi >= 18.5 and bmi < 25:
            return "Нормальная масса тела", "success"
        case bmi if bmi >= 25 and bmi < 30:
            return "Избыточная масса тела", "warning"
        case bmi if bmi >= 30 and bmi < 35:
            return "Ожирение 1-й степени", "danger"
        case bmi if bmi >= 35 and bmi < 40:
            return "Ожирение 2-й степени", "danger"
        case bmi if bmi >= 40:
            return "Ожирение 3-й степени", "danger"
        case _:
            return "Индекс массы тела не определен", "light"
def calculate_bmi():
    weight = float(weight_entry.get())
    height = float(height_entry.get())
    bmi = weight / (height ** 2)
    rezult, b_style = mcasse_bmi(bmi)
    bmi_label.config(text=f"{rezult}", bootstyle=b_style)
    bmi_meter.configure(amountused=round(bmi, 2), bootstyle=b_style)

win = ttk.Window(title="BMI. Индекс массы тела", themename='darkly', resizable=(False, False))
photos = ttk.PhotoImage(file='risk.png')
win.iconphoto(False, photos)
w_width = 500
w_height = 300
s_width = win.winfo_screenwidth()
s_height = win.winfo_screenheight()
x = (s_width / 2) - (w_width / 2)
y = (s_height / 2) - (w_height / 2)
win.geometry(f"{w_width}x{w_height}+{int(x)}+{int(y)}")
#for c in range(4): win.columnconfigure(index=c, weight=1)
#for r in range(2): win.rowconfigure(index=r, weight=1)
weight_label = ttk.Label(win, text='Введите вес, кг', bootstyle='info')
weight_label.grid(row=0, column=0, padx=15, pady=5, sticky='ew')
height_label = ttk.Label(win, text='Введите рост, м', bootstyle='info')
height_label.grid(row=0, column=1, padx=15, pady=5, sticky='ew')
weight_entry = ttk.Entry(win, justify='right', width=15)
weight_entry.grid(row=1, column=0, padx=15, pady=3, sticky='ew')
height_entry = ttk.Entry(win, justify='right', width=15)
height_entry.grid(row=1, column=1, padx=10, pady=3, sticky='ew')
calculate_button = ttk.Button(win, text="Рассчитать", command=calculate_bmi)
calculate_button.grid(row=1, column=2, padx=20, pady=3, sticky='ew')
exit_button = ttk.Button(win, text="Выход", command=lambda: win.destroy())
exit_button.grid(row=1, column=3, padx=10, pady=3, ipadx=15, sticky='ew')
bmi_separator = ttk.Separator(win, bootstyle='primary')
bmi_separator.grid(row=2, column=0, columnspan=4, padx=10, pady=15, sticky='ew')
bmi_label = ttk.Label(win, text=" 0 ", justify="center")
bmi_label.grid(row=3, column=0, columnspan=4, padx=10, pady=10)
bmi_meter = ttk.Meter(
    bootstyle='secondary',
    arcrange=180,
    arcoffset=180,
    metersize=300,
    amounttotal=70,
    padding=5,
    amountused=0,
    metertype="semi",
    subtext="BMI",
    interactive=False,
    meterthickness=75,
    showtext=True,
    textfont='-size 16 -weight bold',
)
bmi_meter.grid(row=4, column=0, columnspan=4, padx=3, pady=3, sticky='ew')

"""
Очень большой дефицит массы тела	< 16
Выраженный дефицит массы тела	16.0 - 16.9
Недостаточная масса тела	17.0 - 18.4
Норма	18.5 - 24.9
Избыточная масса тела	25.0 - 29.9
Ожирение 1-й степени	30.0 - 34.9
Ожирение 2-й степени	35.0 - 39.9
Ожирение 3-й степени	≥ 40.0
"""

win.mainloop()