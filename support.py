#fetch comments fonksiyonu aynı yorumu sürekli ekliyor neden olduğunu bilmiyorum bi çözüm bul garip bi şekilde txtfiledata da 
#kullanılan ||| motifi comments arasında gözüküyor bu nası oluyor bi fikrim yok ama oluyor bi şekilde 

import requests
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from bs4 import BeautifulSoup as bs
import time,os,json
import os,datetime,random,sys
import traceback
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import undetected_chromedriver as uc 
import platform
from selenium.webdriver.common.by import By

def convert_str_to_number(x):
    total_stars = 0
    num_map = {'K': 1000, 'M': 1000000, 'B': 1000000000}
    if str(x).isdigit():
        total_stars = int(x)
    else:
        if len(x) > 1:
            total_stars = float(x[:-1]) * num_map.get(x[-1].upper(), 1)
    return int(total_stars)

def drv():
    global driver
    op = uc.ChromeOptions()
    #op.add_argument("--headless")
    op.add_argument("--mute-audio")
    if platform.system() == "Windows":
        op.binary_location = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        driver = uc.Chrome(options=op,enable_cdp_events=True)
    elif platform.system() == "Darwin":
        op.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        driver = uc.Chrome(options=op)
    else:
        return None

def movies_from_category(category, number_of_movies, wanted_stars):
    category_url = "https://www.imdb.com/search/title/?genres="
    movie_list = []
    # Read start_number from last_id.txt
    try: 
        os.makedirs(os.path.dirname("lastids/"), exist_ok=True)
    except:
        pass
    last_id_file = f"lastids/last_id_{category}.txt"
    if os.path.exists(last_id_file) and os.stat(last_id_file).st_size != 0:
        with open(last_id_file, "r") as f:
            start_number = f.readline().strip()
    else:
        start_number = "1"
    fetched_movie_number = 0
    # Fetch the current page with movies

    soup = bs(requests.get(category_url + category + "&start=" + start_number).content, 'html.parser').find_all("div", {"class": 'lister-item mode-advanced'})
    for movie_soup in soup:  
        try:
            movie = {
                "name": movie_soup.find('div', {"class": "lister-item-content"}).find("h3").find("a").text,
                "stars": movie_soup.find("div", class_='ratings-imdb-rating')['data-value'],
                "link": movie_soup.find('div', {"class": "lister-item-content"}).find("h3").find("a")['href'],
                "id": movie_soup.find('div', {"class": "lister-item-content"}).find("h3").find("span").text[:-1],
                "category": category
            }

            with open(last_id_file, "w") as f:
                f.write(str(movie["id"]))
            # Check if the movie already exists in movies.json
            if any(m["link"] == movie["link"] for m in movie_list):
                continue
            # Check if rate value is greater than or equal to wanted stars value
            if fetched_movie_number >= number_of_movies:
                break
            if float(movie['stars']) >= wanted_stars:
                fetched_movie_number += 1
                movie_list.append(movie)
            else:
                pass
        except IndexError:
            continue
        except TypeError:
            continue
        except Exception as e:
            print(e)
    return movie_list


def fetch_comments(driver):
    wait = WebDriverWait(driver,10)
    normal_more = '//*[@id="__next"]/main/div/section/div/section/div/div[1]/section[1]/div[1]/div[11]/div/span[1]/button/span/span'
    normal_all = '//*[@id="__next"]/main/div/section/div/section/div/div[1]/section[1]/div[1]/div[11]/div/span[2]/button/span/span'
    spoiler = '//*[@id="__next"]/main/div/section/div/section/div/div[1]/section[1]/div[2]/span/button/span/span'
    spoiler_more = '//*[@id="__next"]/main/div/section/div/section/div/div[1]/section[1]/div[3]/div[11]/div/span[1]/button/span/span'

    # Check if "all" button exists and is visible
    try:

        driver.execute_script("arguments[0].click()", WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, normal_more))))
        driver.execute_script("arguments[0].click()", WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, normal_all))))
        driver.execute_script("arguments[0].click()", WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, spoiler))))
        driver.execute_script("arguments[0].click()", WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, spoiler_more))))
    except Exception as e:
        pass
    
    #wait 5 seconds for comments to load 
    time.sleep(5)

    # Take comments
    comment_all = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "kFxVZc")))
    comments = [element.get_attribute("textContent") for element in comment_all]

    # Take likes
    likes = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ipc-voting__label__count--up")))
    likes = [element.get_attribute("textContent") for element in likes]

    # Take dislikes
    dislikes = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ipc-voting__label__count--down")))
    dislikes = [element.get_attribute("textContent") for element in dislikes]

    return comments, likes, dislikes

def trivial(movie_list, wanted_comment_number, interest_percent, interest_1_v):
    function_return = []
    comments_path = "old_comments/comments.txt"
    drv()
    
    def check_and_write_comments(comments_path, movie, comment_text, interest_per, function_return):
        if os.path.exists(comments_path):
            if os.stat(comments_path).st_size != 0:
                with open(comments_path, "r") as f:
                    comments = [i for i in f.read().split("\n")]
                    exists = False
                    for old_comment in comments:
                        if old_comment:
                            comments_split = old_comment.split("|||")
                            name = comments_split[0]
                            old_comment_text = comments_split[1]

                            if old_comment_text == comment_text:
                                exists = True
                                break

                    if not exists:
                        txtfiledata = f"{movie['name']}|||{comment_text}|||{interest_per}|||{movie['category']}\n"
                        function_return.append(txtfiledata)
                        with open(comments_path, "a",encoding="utf-8") as f:
                            f.write(txtfiledata)
            else:
                txtfiledata = f"{movie['name']}|||{comment_text}|||{interest_per}|||{movie['category']}\n"
                with open(comments_path, "a",encoding="utf-8") as f:
                    f.write(txtfiledata)
                function_return.append(txtfiledata)
        else:
            try:
                os.makedirs(os.path.dirname(comments_path), exist_ok=True)
            except OSError as e:
                print(f"An error occurred while creating the directory: {e}")
            else:
                with open(comments_path, "w",encoding="utf-8") as f:
                    txtfiledata = f"{movie['name']}|||{comment_text}|||{interest_per}|||{movie['category']}\n"
                    function_return.append(txtfiledata)
                    f.write(txtfiledata)

    for movie in movie_list:
        try:
            # Fetching comments for each movie
            trivia_url = "https://www.imdb.com" + movie['link'] + "trivia"
            driver.get(trivia_url)
            # Fetch comments using the fetch_comments function
            comments, likes, dislikes = fetch_comments(driver)
            
            if len(comments) == 0:
                continue  
            
            for i in range(len(comments)):
                try:
                    comment_text = comments[i]
                    comment_text = comment_text.replace('\n', '')  # Replace with space or empty string
                    interest_1 = convert_str_to_number(likes[i]) + convert_str_to_number(dislikes[i])
                    if interest_1 == 0:
                        continue
                    interest_per = (convert_str_to_number(likes[i]) / convert_str_to_number(interest_1)) * 100
                    
                    
                    if float(interest_per) >= float(interest_percent) and float(interest_1) >= float(interest_1_v):
                        check_and_write_comments(comments_path, movie, comment_text, interest_per, function_return)
                        
                except Exception:
                    print(traceback.format_exc())
                    continue
            
            driver.quit()  # quit the driver so Google won't stay open
        
        except Exception:
            print(traceback.format_exc())
            print(movie['link'])
            driver.quit()
            continue
        finally:
            driver.quit()
    return function_return


movie = [{"name": "Fringe","stars":"8.4","link":"/title/tt1119644/","id":"1","category":"Sci-Fi"} ]
complete_result = trivial(movie,1,60,100)

table_html = "<html><head><style>table {border-collapse: collapse; width: 100%;} th, td {text-align: left; padding: 8px;} th {background-color: #f2f2f2;}</style></head><body>"
table_html += "<h2>Results</h2>"
table_html += "<table>"
table_html += "<tr><th>Category</th><th>Movie</th><th>Comment</th><th>Interest Percentage</th></tr>"


for item in complete_result:
    name = item.split("|||")[0]
    comment = item.split("|||")[1]
    interest_percent = item.split("|||")[2]
    category = item.split("|||")[3]
    table_html += f"<tr><td>{category}</td><td>{name}</td><td>{comment}</td><td>{interest_percent}</td></tr>\n"
table_html += "</table></body></html>"

file_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".html"
with open(f"results{random.randint(0,99999)}.html", "w",encoding=sys.stdout.encoding) as file:
    file.write(table_html)