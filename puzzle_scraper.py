from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

class PuzzleScraper:
    def __init__(self, trace_mod=False):
        self.trace_mod = trace_mod
        self.option = webdriver.ChromeOptions()
        self.option.add_argument('--log-level=3')
        self.driver = webdriver.Chrome("./chromedriver", options=self.option)
        self.driver.get("https://www.nytimes.com/crosswords/game/mini")
        self.driver.maximize_window()
        self.driver.execute_script("window.scrollTo(0, 300)") 

    def click_button(self):
        clas = "buttons-modalButtonContainer--35RTh"
        class_element = self.driver.find_element_by_class_name(clas)
        children_by_css = class_element.find_elements_by_css_selector("*")
        for child in children_by_css:
            if "OK" in child.text:
                child.click()
                if self.trace_mod:
                    print("OK button clicked")
                break
        return

    def get_grid(self):
        grid = []
        for i in range(25):
            cell_path = "//*[@id=\"cell-id-" + str(i) + "\"]"
            c = self.driver.find_elements_by_xpath(cell_path)[0]
            attribute = c.get_attribute("class")
            if "block" in attribute:
                grid.append(1)
            else:
                grid.append(0)
        result = []
        for i in range(5):
            result.append(grid[i * 5: (i * 5 + 5)])
        if self.trace_mod:
            print("Received grid:")
            for i in range(5):
                for j in range(5):
                    print(result[i][j], end=' ')
                print()
                
        return result
    
    def get_clues(self):
        across = []
        down = []
        clues = self.driver.find_elements_by_class_name("Clue-li--1JoPu")
        for clue in clues:
            p = clue.find_element_by_xpath("..//..")
            parent_children = p.find_elements_by_css_selector("*")
            if parent_children[0].text == "ACROSS":
                across.append((clue.text[0], clue.text[2:]))
            else:
                down.append((clue.text[0], clue.text[2:]))
        if self.trace_mod:
            print("Received clues:")
            print("ACROSS:")
            for i, clue in enumerate(across):
                print(i, clue)
            print("DOWN:")
            for i, clue in enumerate(down):
                print(i, clue)
                
        return across, down

    def get_grid_numbers(self):
        numbers_grid = []
        for i in range(25):
            cell_path = "//*[@id=\"cell-id-" + str(i) + "\"]"
            c = self.driver.find_elements_by_xpath(cell_path)[0]
            p = c.find_element_by_xpath("..")
            children = p.find_elements_by_css_selector("*")
            try:
                if children[1].text.isnumeric():
                    numbers_grid.append(children[1].text)
                else:
                    numbers_grid.append(0)
            except:
                numbers_grid.append(0)
                continue
        
        result = []
        for i in range(5):
            number_row = []
            for j in range(5):
                number_row.append(numbers_grid[i * 5 + j])
            result.append(number_row)
        if self.trace_mod:
            print("Received question numbers on the grid")
        return result



    def reveal_puzzle(self):
        # not reliable
        # reveal_xpath = "/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div/ul/div[2]/li[2]/button"
        # self.driver.find_element_by_xpath(reveal_xpath).click() # 1
        
        toolbar = self.driver.find_element_by_class_name("Toolbar-expandedMenu--2s4M4")
        toolbar_children = toolbar.find_elements_by_css_selector("*")
        toolbar_children[11].click()

        puzzle_element = self.driver.find_element_by_link_text("Puzzle")
        puzzle_element.click() # 2

        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/article/div[2]/button[2]/div").click() # worked!
        self.driver.find_element_by_class_name("ModalBody-closeX--2Fmp7").click() # solution is shown after this (X button)
        
        grid = []
        for i in range(25):
            cell_path = "//*[@id=\"cell-id-" + str(i) + "\"]"
            c = self.driver.find_elements_by_xpath(cell_path)[0]
            p = c.find_element_by_xpath("..")
            children = p.find_elements_by_css_selector("*")
            try:
                if children[1].text.isnumeric():
                    grid.append(children[3].text)
                else:
                    grid.append(children[1].text)
            except:
                grid.append(' ')
                continue
        
        result = []
        for i in range(5):
            row = []
            for j in range(5):
                row.append(grid[i * 5 + j])
            result.append(row)
        if self.trace_mod:
            print("Received offical solution:")
            for i in range(5):
                for j in range(5):
                    print(result[i][j], end=' ')
                print()    
        return result
    
    def close_driver(self):
        self.driver.quit()
        if self.trace_mod:
            print("Webdriver is closed")