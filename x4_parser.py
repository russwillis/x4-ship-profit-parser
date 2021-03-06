import gzip
import os
import xml.etree.ElementTree as etree
from tkinter import *
from tkinter import filedialog

# Regex to pull out the relevant data from the text line
# example : MINER_4 DGA-872 sold 476 Silicon to HOP High Tech Factory II FLQ-580 in Holy Vision for 56701 Cr
pattern = re.compile('(.+) sold (\d+) (.+?) to.+? (\d+) Cr.*')


class X4(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()


def main():
    main_window = Tk()
    main_window.geometry('1200x800')
    app = X4(master=main_window)
    app.master.title('X4 Save file parser')

    def browse_function():
        home = os.path.expanduser('~')
        # The next line only seems to work on Windows but doesn't blow up on Mac so it can stay:)
        default_save_location = os.path.join(home, 'Documents\\Egosoft\\X4\\')
        file_path = filedialog.askopenfilename(initialdir=default_save_location, title='Select save file')
        # Put the resultant file path in the GUI so the action buttons know what to work on
        path_actual_entry.insert(0, file_path)

    def get_elements(save_file, tag):
        context = iter(etree.iterparse(save_file, events=('start', 'end')))
        _, root = next(context)
        for event, elem in context:
            # I only care about the log entries that match 'Trade Completed' as it holds all the data I care about
            if event == 'end' and elem.tag == tag and elem.get('title') == 'Trade Completed':
                yield elem
                # helps to keep the program from keeping all 300mb + in memory
                root.clear()

    def generate_csv():
        # Update the status text field in GUI by removing old message and supplying new
        response_text.delete("1.0", END)
        response_text.insert(END, 'Processing CSV')
        generate_correct_view('csv')

    def convert_string_to_time(str_to_convert):
        minutes, seconds = divmod(int(float(str_to_convert)), 60)
        hours, minutes = divmod(minutes, 60)
        return '{}:{:0>2d}:{:0>2d}'.format(hours, minutes, seconds)

    def generate_correct_view(filetype):
        with gzip.open(path_actual_entry.get(), 'rt') as gzipped_file:
            if filetype == 'csv':
                with open('extracted_logs.csv', 'w') as extracted_file:
                    # Just need to check the log entry elements
                    for elem in get_elements(gzipped_file, 'entry'):
                        match = pattern.match(elem.attrib['text'])
                        if match:
                            # have a stab at converting the string 'time' to an actual time
                            format_time = convert_string_to_time(elem.get('time'))
                            csv_line = '{}, {}, {}, {}, {}, {}'.format(elem.get('time'), format_time,
                                                                       match.group(1), match.group(2),
                                                                       match.group(3), match.group(4))
                            extracted_file.writelines(csv_line)
                            extracted_file.write('\n')
                            # Update the status text field in GUI by removing old message and supplying new
                response_text.delete("1.0", END)
                response_text.insert(END, 'CSV file generated')
            elif filetype == 'onscreen':
                # Just need to check the log entry elements
                reformatted_text = {}
                for elem in get_elements(gzipped_file, 'entry'):
                    match = pattern.match(elem.attrib['text'])
                    if match:
                        if match.group(1) in reformatted_text:
                            reformatted_text[match.group(1)]['cash'] = reformatted_text[match.group(1)]['cash'] + int(
                                match.group(4))
                            reformatted_text[match.group(1)]['count'] += 1
                        else:
                            reformatted_text[match.group(1)] = {'count': 0, 'cash': int(match.group(4))}

                # Update the status text field in GUI by removing old message and supplying new
                response_text.delete("1.0", END)
                response_text.insert(END, 'List generated')
                # Now prep the data ready for display on screen
                all_keys = list(reformatted_text.keys())

                for i in range(len(all_keys)):
                    # format the prices to have comma separators
                    cash = format(int(reformatted_text[all_keys[i]]['cash']), ',d')
                    trip_count = int(reformatted_text[all_keys[i]]['count'])
                    average_cash = format(int(reformatted_text[all_keys[i]]['cash']) //
                                          int(reformatted_text[all_keys[i]]['count']), ',d')

                    # try to make a nice grid style
                    ship_name = Entry(app, justify=LEFT)
                    ship_cash = Entry(app, justify=RIGHT)
                    ship_average = Entry(app, justify=RIGHT)
                    ship_trips = Entry(app, justify=CENTER)
                    ship_name.delete(0, END)
                    ship_cash.delete(0, END)
                    ship_average.delete(0, END)
                    ship_trips.delete(0, END)
                    ship_name.insert(0, all_keys[i])
                    ship_cash.insert(0, cash)
                    ship_average.insert(0, average_cash)
                    ship_trips.insert(0, trip_count)
                    ship_name.grid(row=i + 6, column=0)
                    ship_cash.grid(row=i + 6, column=1)
                    ship_average.grid(row=i + 6, column=2)
                    ship_trips.grid(row=i + 6, column=3)

    def on_screen_view():

        # Update the status text field in GUI by removing old message and supplying new
        response_text.delete("1.0", END)
        response_text.insert(END, 'Processing List')
        ship_name_header = Entry(app, justify=CENTER)
        ship_cash_header = Entry(app, justify=CENTER)
        ship_average_header = Entry(app, justify=CENTER)
        ship_trips_header = Entry(app, justify=CENTER)

        ship_name_header.insert(0, 'Ship Name')
        ship_cash_header.insert(0, 'Total Credits Earned')
        ship_average_header.insert(0, 'Average Credits')
        ship_trips_header.insert(0, 'Total Trips Made')

        ship_name_header.grid(row=5, column=0)
        ship_cash_header.grid(row=5, column=1)
        ship_average_header.grid(row=5, column=2)
        ship_trips_header.grid(row=5, column=3)
        generate_correct_view('onscreen')

    # Create widgets
    path_label = Label(app, text='Path to save file')
    browse_button = Button(app, text="Browse", command=browse_function)
    csv_button = Button(app, text='Generate CSV', command=generate_csv)
    json_button = Button(app, text='On screen view (WIP)', command=on_screen_view)
    path_actual_entry = Entry(app, width=50)
    response_text = Text(app, height=2, width=50)

    # Layout grid (not pretty but straightforward)
    path_label.grid(row=1, column=0)
    browse_button.grid(row=2, column=0)
    path_actual_entry.grid(row=2, column=1, columnspan=3, sticky=E + W)
    csv_button.grid(row=3, column=1)
    json_button.grid(row=3, column=2)
    response_text.grid(row=4, column=1)

    # for testing
    # path_actual_entry.insert(0, 'x4-ship-profit-parser/save_001.xml.gz')

    # Initial setup
    response_text.insert(END, 'Results go here')

    app.mainloop()


if __name__ == "__main__":
    main()
