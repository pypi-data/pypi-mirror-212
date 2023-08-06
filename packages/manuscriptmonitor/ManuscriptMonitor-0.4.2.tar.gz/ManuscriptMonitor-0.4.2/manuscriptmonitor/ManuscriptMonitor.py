from pathlib import Path
import json
import re
import sys

from natsort import natsorted
from rich.table import Table
from rich.live import Live
import pandas as pd
import PySimpleGUI as sg
from watchfiles import watch, Change, DefaultFilter

class CaptureOneFilter(DefaultFilter):
    allowed_extensions = '.iiq'
    def __call__(self, change: Change, path: str) -> bool:
        return (
            super().__call__(change, path) and 
            path.endswith(self.allowed_extensions)
        )

def generate_table(prev_row: dict, now_row: dict, next_row: dict) -> Table:
    """Make a new table."""
    table = Table()
    table.add_column('Landmark')
    table.add_column('Actual Folio')
    table.add_column('Notes for Imagers')

    table.add_row(f"{prev_row.get('Landmark')}", f"{prev_row.get('Actual Folio')}", f"{prev_row.get('Notes for Imagers')}")
    table.add_row(f'[bold green]{now_row.get("Landmark")}', f'[bold green]{now_row.get("Actual Folio")}', f'[bold green]{now_row.get("Notes for Imagers")}')
    table.add_row(f"{next_row.get('Landmark')}", f"{next_row.get('Actual Folio')}", f"{next_row.get('Notes for Imagers')}")
    return table

def get_rows(just_captured: dict, guide_dict, version: bool):
    prev = {}
    now = {}
    next = {}
    for i, d in enumerate(guide_dict):
        if f"{d['Image #']}" == just_captured:
            prev = d.copy()
            if version:
                prev['Landmark'] = f'!{d["Landmark"]}{version}!'
            try:
                now = guide_dict[i+1]
            except:
                pass
            try:
                next = guide_dict[i+2]
            except:
                pass

    return prev, now, next

def get_folders():
    settings_path = Path(__file__).parent.joinpath('settings.json').as_posix()
    try:
        with open(settings_path, 'r') as f:
            settings = json.load(f)
        settings['last_folder']
        settings['excel_folder']
    except:
        settings = {'last_folder': '', 'excel_folder': ''}
    sg.popup_ok('Select the capture folder for this session', title='Set Capture Folder')
    capture_output = sg.popup_get_folder('', no_window=True, initial_folder=settings['last_folder'])
    if not capture_output:
        sys.exit()
    sg.popup_ok('Now select the Excel spreadsheet file that has been\ngenerated for this artifact.', title='Select Spreadsheet')
    excel_file = sg.popup_get_file('', no_window=True, initial_folder=settings['excel_folder'], file_types=(('Excel File', '*.xlsx'),))
    if not excel_file:
        sys.exit()
    excel_folder = Path(excel_file).parent.as_posix()
    settings['last_folder'] = capture_output
    settings['excel_folder'] = excel_folder
    with open(settings_path, 'w') as f:
        json.dump(settings, f)
    return capture_output, excel_file

def get_spreadsheet_data(excel_file):
    df = pd.read_excel(excel_file)
    df = df.fillna('')
    list_of_dicts = df.to_dict('records')
    return list_of_dicts

def main():
    capture_output, excel_file = get_folders()
    guide_dict = get_spreadsheet_data(excel_file)
    with Live(generate_table({}, {}, {}), refresh_per_second=10) as live:
        sg.popup_ok(f'ManuscriptMonitor is watching for new image files in {capture_output}\nTo quit, press CTRL + C or close the terminal.')
        for changes in watch(capture_output, watch_filter=CaptureOneFilter()):
            for change, file in natsorted(changes):
                if change.name == 'added':
                    created = Path(file).name.replace('.iiq', '')
                    version = None
                    for ending in ('_1', '_2', '_3'):
                        if not created.endswith(ending):
                            continue
                        else:
                            created = created.replace(ending, '')
                            version = ending
                            break
                    created = re.sub(r'_.+_', '', created).replace('M', '').replace('P', '').lstrip('0')
                    prev, now, next = get_rows(created, guide_dict, version)
                    live.update(generate_table(prev, now, next))

if __name__ == '__main__':
    main()
