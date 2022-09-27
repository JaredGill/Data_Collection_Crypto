# Data_Collection_CoinMarket
This project is a data scrape of the website https://coinmarketcap.com/ with Selenium to get crypto coin data. It will involve the use of various python packages(see below) to scrape data and then to connect to Amazon Web Services S3 Bucket and RDS. The python script will be saved as a Docker image to be ran on a AWS EC2 instance which will pull the Docker Image and run the scraper everyday at 12:00pm using crontab. The Docker and EC2 metrics will be observed and monitored using prometheus and grafana using a node exporter. Lastly a CI/CD pipeline will be created to update the Docker image upon a push to Github.
### Built with
- selenium==4.4.3         (To scrape data)
- pandas==1.4.3           (To handle data)
- numpy==1.23.1           (To clean data)
- boto3==1.24.53          (To connect to AWS S3 Bucket and upload)
- psycopg2==2.9.3         (To connect to RDS)
- SQLAlchemy==1.4.40      (To upload data to RDS)

## Building a Scraper 
- The package Selenium was used to open and control a webpage in Microsoft Edge to coinmarket using the code 
```python
def __init__ (self, URL: str = "https://coinmarketcap.com/"):
        self.driver = webdriver.Edge()
        self.driver.get(URL)
```
- Selenium finds specific features via xpaths, which can be found using ctrl + shift + c whilst on the webpage and hovering over elements.
- A unique xpath is preferred, or making a list of all elements found by xpath and choosing which to use.
- A common way to find unique xpaths is to obtain a parent xpath of element and set a variable equal to it called a container where you can then refine the xpath search.
- Several methods were designed on this page to navigate it including change currency.
- Change currency finds and clicks option, waits for elements to load before clicking the british pound option.
```python
settings_button = self.driver.find_element(by=By.XPATH, value='//*[@class="sc-1pyr0bh-0 bSnrp sc-1g16avq-0 kBKzKs"]')
            settings_button.click()
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//*[@class="vxp8h8-0 VMCHA"]')))
            select_currency_button = self.driver.find_element(by=By.XPATH, value='//button[@data-qa-id="button-global-currency-picker"]')
            select_currency_button.click()
            currency = self.driver.find_element(by=By.XPATH, value='//*[@class="ig8pxp-0 jaunlC"]')
            time.sleep(2)
            currency.click()
```
- Search bar method functions similarly to the above, but takes a string as parameter to input text.
- Scroll bottom finds the maximum height of the page then uses window.scrollTo() to descend by 2000
```python
max_page_height = self.driver.execute_script("return document.documentElement.scrollHeight")
        scroll_down_y_axis = 2000

        while scroll_down_y_axis < max_page_height:
            self.driver.execute_script(f"window.scrollTo(0, {scroll_down_y_axis});")
            self.get_links()
            time.sleep(3)
            scroll_down_y_axis += 2000
```            
- In the above method there was a get_links() called. This method obtains the links for each coin via their "a" tag in the main container for the table on the homepage.
- It then saves the href's from the tags to a list.
```python 
self.coin_container = self.driver.find_elements(by=By.XPATH, value='//div[@class="h7vnx2-1 bFzXgL"]//div[@class="sc-16r8icm-0 escjiH"]')
        for crypto_coin in self.coin_container:
            a_tag = crypto_coin.find_element(by=By.TAG_NAME, value='a')
            link = a_tag.get_attribute('href')
            link_list.append(link)
```
- As the website had dynamic pages, the page must scroll down to obtain the all the links.
    
## Retrieving Data and Images
- The method data_scrape() was created to iterate through unique links to travel to the coins pages and obtain relevant data.
- By passing in a number, you can look at the coins in order of their market rank descending from Bitcoin at rank #1
```python
url_counter = 0
        coin_link_list = self.get_links()
        
        while url_counter < coins_to_scrape:
            URL = coin_link_list[url_counter]
            self.driver.get(URL)
            self.get_image()
            self.get_text_data()
```
- In a While loop, two methods were called: get_image() and get_text_data().
- get_image() functioned similar to get_links working through a container, then finding image src for link/download, and alt for imgage name.
- get_text_data() also found some elements either by direct xpath, or container usage as well. But one container's data couldnt be refined to individual xpaths as all the class names were exactly the same. So instead the container located all elements and stored them in a list to be called upon as required.
```python
data_container = self.driver.find_elements(by=By.XPATH, value='//div[@class="sc-19zk94m-4 eYCtRS"]//div[@class="sc-16r8icm-0 iutcov"]//div[@class="sc-16r8icm-0 nds9rn-0 cQtSIv"]')
data_list = data_container[0].text.split('\n')
volume_tag = data_list[12]
self.coin_data_dict['Volume (£)'].append(volume_tag)
```
- In addition a universally unique ID was generated using the UUID4 package.

pip3 freeze > requirements.txt was used to produce requirements.txt for docker

## Local Save
To store the scraped data locally a raw_data folder was created inside of which had two child directories for images, and numerical data.
```python
data_folder_path = f"C:/Users/jared/AiCore/Data_Collection_Pipeline/raw_data/total_data"
if not os.path.exists(data_folder_path):
    os.makedirs(data_folder_path)

current_date = date.today()

df_for_save.to_json(f'C:/Users/jared/AiCore/Data_Collection_Pipeline/raw_data/total_data/{current_date}_total_data.json')

image_folder_path = f"C:/Users/jared/AiCore/Data_Collection_Pipeline/raw_data/images"
if not os.path.exists(image_folder_path):
    os.makedirs(image_folder_path)

img_name_list = self.img_dict["ImageName"]
img_link_list = self.img_dict["ImageLink"]

# zip function allows iteration for 2+ lists and runs until smallest list ends
for (name, link) in zip(img_name_list, img_link_list):
    if not os.path.exists(f"C:/Users/jared/AiCore/Data_Collection_Pipeline/raw_data/images/{name}_logo.jpeg"):
        image_path = f"C:/Users/jared/AiCore/Data_Collection_Pipeline/raw_data/images/{name}_logo.jpeg"
        urllib.request.urlretrieve(link, image_path)
```
- The numerical data for the crypto coins was created as a prior to this function and passed in as the variable "df_for_save".
- As this data changes every second, this project attempts to scrape at 12:00 every day to create some historical data. 
- The images were saved by iterating between 2 lists, both of which had strings added as the coins were scraped so all positions in list will be linked to another.
- E.g. Bitcoin is 1st in market rank so its name and link will be at position 0 in both lists.
- To save on AWS refer to AWS S3 and RDS sections.

## Inheritance
The structure of the project was one child class (CoinScraper) inherits from two parent classes(General_Scraper and AWS_Data_Storage). This required several stapes:
- The method resolution order was found with cmd
```python 
        print(CoinScraper.mro())
```
- Which gave [<class 'Scraper.CoinScraper'>, <class 'Scraper.General_Scraper'>, <class 'AWS_storage.AWS_Data_Storage'>, <class 'object'>]
- The class on the left inherits from the previous two, similarly the class in the middle must inherit any attributes to be passed on.
- So both the left hand side, and middle class will have a super().__init__() in their __init__ method.
        - The General_Scraper class will have super().__init__(*args, **kwargs) to inherit and pass any arguements
    
## Unit Tests
Each public function was unit tested to ensure they were working correctly.
- For some it involved calling the function and testing the return value.
- In other cases the return value could change such as:
```python
links = self.cs.get_links()
first_url = "https://coinmarketcap.com/currencies/bitcoin/"
length_urls = 17
self.assertEqual(first_url, links[0])
#as top 100 crytpos change daily, last url may fail
last_url = "https://coinmarketcap.com/currencies/multi-collateral-dai/"
self.assertEqual(last_url, links[11])
self.assertEqual(length_urls, len(links))
self.assertIsInstance(links, list)
```
- Here the amount of links scraped and last url are subject to change as the webpage loads dynamically so this test may fail.

- For some functions the ability to call on specific functions in different classes or files were tested using Mock.
- This Mock class simulates the given function.
```python
@patch('selenium.webdriver.support.wait.WebDriverWait.until')
@patch('selenium.webdriver.remote.webelement.WebElement.click')
def test_accept_cookies(self,
                    mock_click_element: Mock,
                    mock_until: Mock):

self.s.accept_cookies()
mock_until.assert_called_once()
mock_click_element.assert_called_once()
```
- Here the patch line finds the location of the function being mocked by inputting the definition which can be found be right-clicking the function where it is used.
- The patch's must be in the inverse order of where they are called in script.

## Docker
Docker is a platform that allows users to save their development environment and files to a "image". This image can be pulled to other systems and will have everything needed to run the program such as software and libraries isolated to itself. This image can be run in a instance called a container. These allow for quick testing and sharing are built with a DockerFile. 
- The Docker image is first made with a docker build line.
- The image is tagged and pushed to dockerhub where it an then be pulled to EC2 for easy deployment.

## Amazon Web Services
AWS was chosen as a cloud service provider. Of these services a Amazon Simple Storage Service (S3 Bucket), Relation Database (RDS), and Amazon Elastic Compute Cloud (EC2). 
To connect to the AWS through command line a IAM user was created and the package awscli was used to connect to the user account on the local machine using the keys through enironment variables. On the EC2 awscli was not required as the program was run through docker image so keys were passed as environment variables on the crontab file. 
### Environmental Variables
- Environmental variables were used to handle senstitive details for connecting to AWS RDS and S3.
- For the local windows machine this was done by searching and clicking "Edit the systems Environmental Variables".
        -Then selected the "Environmental variables option, and adding a new variable for AWS_Access_Key and AWS_Secret_key
- For the EC2 Linux machine they were edited into the bottom of the bashrc file.
        - E.g. export AWS_ACCESS_KEY='example'
- These were called in the python script using the os.environ.get() function
- To pass these in the script when running the docker image they were called individually in the docker run line:
        - sudo docker run -it -e AWS_SECRET_KEY=$AWS_SECRET_KEY -e AWS_ACCESS_KEY=$AWS_ACCESS_KEY --name github_example jared22/crypto_scraper_repo
### S3 Bucket
The S3 bucket is a container that was used for data.jsons and images. In order to prepare for upload the files must first be saved locally, then the package boto3 was used to connect:
```python
session = boto3.Session( 
        aws_access_key_id=AWS_ACCESS_KEY, 
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION_NAME)
s3 = session.client('s3')
```
### RDS
The RDS holds the historial data from everyday the scraper was ran, as well as a image table. The connection was made with psycopg2 and then the tables were uploaded through sqlalchemy:
```python
engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
engine.connect()
input_df.to_sql(table_name, engine, if_exists='replace')
```
### EC2
Once created the EC2 was connected to using a Remote - SSH extension on VSCode made by Microsoft.
This required a config file to be set up:
```config
Host EC2_address
HostName path_to_pem_file
User ubuntu
```
The crontab was then setup to run at 12:00pm everyday and prune the docker images, pull the latest, then run a Docker container of the image.

## Grafana and Prometheus
- Grafana was used to observe and monitor the metrics of the EC2 instance and the docker containers through Prometheus. 
- Initially a docker.daemon.json file for docker metrics and sudo nano /etc/systemd/system/node_exporter.service to create a node exporter for the EC2.
### Creating docker.daemon
- This  gives prometheus an address to track docker container metrics which are ran from the EC2. The file contains:
``` 
{
    "metrics-addr" : "127.0.0.1:9323",
    "experimental": true,
    "features": {
    "buildkit": true
    }
}
```
### Creating a Node Exporter
- The node exporter sends the computers local system metrics to prometheus and grafana. In this case the local system is the EC2.
- Navigated to /etc/systemd/system and created a node_exporter.service with the following contents:
```service
[Unit]
Description=Node Exporter
After=network.target

[Service]
User=ubuntu
Type=simple
ExecStart=/home/ubuntu/node_exporter-1.1.2.linux-amd64/node_exporter (path to node exporter in EC2)

[Install]
WantedBy=multi-user.target
```
- Then started the node with sudo systemctl start node_exporter and checked its status with sudo systemctl status node_exporter
### Prometheus
- Prometheus can gather and process data for data visualisation. Here it was configured to observe the mertics of the EC2 and docker container through the node and docker exporter setup.
- A prometheus.yml file was set up to scrape metrics for each:
```python
# OS monitoring
  - job_name: 'node'
    scrape_interval: '30s'
    static_configs:
      - targets: ['localhost:9100']
```
- The prometheus.yml was then started as a docker container that will run indefinetly whilst the EC2 is running with command:
        - sudo docker run --rm -d --network=host --name prometheus -v /home/ubuntu/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus --config.file=/etc/prometheus/prometheus.yml --web.enable-lifecycle
### Grafana
- Grafana was utilised to make a dashboard of the prometheus metrics for clearer data visualisation
- This allowed various metrics to be observed such as:
![image](https://user-images.githubusercontent.com/108297203/192539443-ae14d17b-9ee7-47d6-91ab-70bd60861609.png)
![image](https://user-images.githubusercontent.com/108297203/192539584-61367f70-f6a1-4bf3-acd3-791492f93db7.png)

## Future updates
- More functionality with the generaly scraper class could be implemented. A change page option, or passing in the chosen currency would make it more robust.
- The website does have a tab for historical data for each coin (https://coinmarketcap.com/currencies/bitcoin/historical-data/). These could be scraped for an analysis of coins historical data through the previous crashes and observe where the current price is relative to the trends already observed in the market years ago.
