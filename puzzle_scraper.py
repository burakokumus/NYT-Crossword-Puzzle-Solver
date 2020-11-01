from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

class PuzzleScraper:
    def __init__(self):
        self.driver = webdriver.Chrome("./chromedriver")
        self.driver.get("https://www.nytimes.com/crosswords/game/mini")
        self.driver.maximize_window()
        print(self.driver.title)

    def click_button(self):
        clas = "buttons-modalButtonContainer--35RTh"
        class_element = self.driver.find_element_by_class_name(clas)
        children_by_css = class_element.find_elements_by_css_selector("*")
        for child in children_by_css:
            if "OK" in child.text:
                child.click()
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
        return across, down

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
        return result
    
    def close_driver(self):
        self.driver.quit()

if __name__ == "__main__":
    ps = PuzzleScraper()
    ps.click_button()
    grid = ps.get_grid()
    for row in grid:
        print(row)
    across, down = ps.get_clues()
    print("ACROSS")
    for clue in across:
        print(clue)
    print("DOWN")
    for clue in down:
        print(clue)
    ps.reveal_puzzle()
    ps.close_driver()