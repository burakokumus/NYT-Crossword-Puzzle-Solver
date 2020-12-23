from puzzle_scraper import PuzzleScraper
import json
import time
from PyQt5.QtCore import QDate, Qt

if __name__ == "__main__":
    
    ps = PuzzleScraper()
    ps.click_button()
    grid = ps.get_grid()
    across, down = ps.get_clues()
    grid_numbers = ps.get_grid_numbers()
    ps.reveal_puzzle()
    answer = ps.extract_answers()
    ps.close_driver()

    data = {}
    data["date"] = QDate.currentDate().toString(Qt.DefaultLocaleLongDate)
    data["grid"] = grid
    data["grid_numbers"] = grid_numbers
    data["answer"] = answer
    data["across"] = across
    data["down"] = down
    print(data["down"][3])
    with open("./PuzzleDatabases/December_22.json", "w") as outfile:
        json.dump(data, outfile)