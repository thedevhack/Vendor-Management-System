## Steps To Run the Project

1. Run the Command to clone the repo and cd into it
```bash
git clone https://github.com/thedevhack/Vendor-Management-System.git
cd Vendor-Management-System
```
2. Create the environment of Python depending on your Operating System (NOTE: You should have python installed on your computer)
```bash
virtualenv venv - Linux
```
```bash
python -m venv venv - Windows
```
3. Activate the Virtual Environment
```bash
source venv/bin/activate - Linux
```
```bash
venv\Scripts\activate - Windows
```
4. Pip install all the python modules required using pip
```bash
pip install -r requirements.txt
```
5. Make migrations
```bash
python manage.py migrate
```
6. Run the django server on 127.0.0.1:8000 if you want to test manually or else below are instructions for test suite
```bash
python manage.py runserver
```

## To Run the Test suite
### This test will add 1 vendor and make 4 purchase order request regarding that Vendor 2 purchase order will be acknowledged and 1 purchase order will be completed and then the vendor perfromance will be printed

Performance Metrics units description
1. on_time_delivery_rate - shown as a float value between 0 to 1.0 where 1.0 means all orders are completed ontime
2. quality_rating_avg - shown as value out of 10 based on average of quality rating on completed purchase orders where quality rating was given
3. average_response_time - units in seconds which determines how many seconds it took for vendor to acknowledge a purchase order
4. fulfillment_rate - shown as a float value between 0 to 1.0 which shows how many orders are completed successfully
```bash
python manage.py test api
```
