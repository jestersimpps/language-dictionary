import gspread
from google.oauth2.service_account import Credentials
from typing import List, Dict


class TranslationSpreadsheet:
    def __init__(self, credentials_path: str, spreadsheet_name: str, gmail: str):
        self.scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        self.creds = Credentials.from_service_account_file(
            credentials_path, scopes=self.scope
        )
        self.client = gspread.authorize(self.creds)

        # Open the spreadsheet (create it if it doesn't exist)
        try:
            self.sheet = self.client.open(spreadsheet_name).sheet1
        except gspread.SpreadsheetNotFound:
            self.sheet = self.client.create(spreadsheet_name).sheet1

        # Set up headers if the sheet is empty
        last_row = self.get_last_row()
        print(f"Spreadsheet file: https://docs.google.com/spreadsheets/d/{self.sheet.spreadsheet.id}/edit?gid=0#gid=0")
        print(f"Spreadsheet ID: {self.sheet.spreadsheet.id}")
        print(f"Dictionary rows: {last_row}")
        # print(f"Data: {self.get_translations()}")

        if last_row == 0:
            try:
                self.sheet.append_row(["English", "Chinese", "Pinyin", "Notes"])
                spreadsheet = self.sheet.spreadsheet
                spreadsheet.share(gmail, perm_type="user", role="writer")
                print("Sheet initiated successfully")
            except Exception as e:
                print(f"Error adding row: {str(e)}")

    def get_last_row(self):
        str_list = list(
            filter(None, self.sheet.col_values(1))
        )  # Get all non-empty values in first column
        return len(str_list)

    def add_translation(self, english: str, chinese: str, pinyin: str, notes: str = ""):
        print("")
        try:
            self.sheet.append_row([english, chinese, pinyin, notes])
            print("Row added successfully")
        except Exception as e:
            print(f"Error adding row: {str(e)}")

    def get_translations(self) -> List[Dict[str, str]]:

        all_values = self.sheet.get_all_values()
        headers = all_values[0]
        translations = []

        for row in all_values[1:]:
            translation = {headers[i]: row[i] for i in range(len(headers))}
            translations.append(translation)

        return translations

    def update_translation(
        self, english: str, chinese: str, pinyin: str, notes: str = ""
    ):
        cell = self.sheet.find(english)
        if cell:
            self.sheet.update_cell(cell.row, 2, chinese)
            self.sheet.update_cell(cell.row, 3, pinyin)
            self.sheet.update_cell(cell.row, 4, notes)
        else:
            self.add_translation(english, chinese, pinyin, notes)

    def delete_translation(self, english: str):
        cell = self.sheet.find(english)
        if cell:
            self.sheet.delete_rows(cell.row)
        else:
            print(f"Translation for '{english}' not found.")
