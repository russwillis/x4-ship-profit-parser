import gzip
import os
from tkinter import *
from tkinter import filedialog
import xml.etree.ElementTree as etree

pattern = re.compile('(.+) sold (\d+) (.+?) to.+? (\d+) Cr.*')


class X4(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()


def main():
    main_window = Tk()
    app = X4(master=main_window)
    app.master.title('X4 Save file parser')

    def browse_function():
        home = os.path.expanduser('~')
        default_save_location = os.path.join(home, 'Documents\\Egosoft\\X4\\')
        file_path = filedialog.askopenfilename(initialdir=default_save_location, title='Select save file')
        path_actual_entry.insert(0, file_path)

    def get_elements(save_file, tag):
        context = iter(etree.iterparse(save_file, events=('start', 'end')))
        _, root = next(context)
        for event, elem in context:
            if event == 'end' and elem.tag == tag and elem.get('title') == 'Trade Completed':
                yield elem
                root.clear()

    def generate_csv():
        with gzip.open(path_actual_entry.get(), 'rt') as gzipped_file:
            with open('extracted_logs.csv', 'w') as extracted_file:
                # Have to go out of the way to actually kill the UI bit otherwise it hangs about forever and
                # process won't run - learn threading?
                main_window.destroy()
                for elem in get_elements(gzipped_file, 'entry'):
                    match = pattern.match(elem.attrib['text'])
                    if match:
                        csv_line = '{}, {}, {}, {}'.format(match.group(1), match.group(2), match.group(3),
                                                           match.group(4))
                        extracted_file.writelines(csv_line)
                        extracted_file.write('\n')

    # Create widgets
    path_label = Label(app, text='Path to save file')
    browse_button = Button(app, text="Browse", command=browse_function)
    go_button = Button(app, text='Start generating', command=generate_csv)
    path_actual_entry = Entry(app, width=100)

    # Layout grid
    path_label.grid(row=1, column=0)
    browse_button.grid(row=2, column=0)
    path_actual_entry.grid(row=2, column=1, columnspan=3, sticky=E+W)
    go_button.grid(row=3, column=1, rowspan=2)

    app.mainloop()


if __name__ == "__main__":
    main()
