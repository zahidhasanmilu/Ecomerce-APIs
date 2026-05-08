# Naraz Ecommerce 

## Development Setup
#Cloning the repository
1. Create a repository using this template or clone the repository
    ```    
    git clone https://github.com/zahidhasanmilu/Ecomerce-APIs.git
    ```

2. Create a virtual environment
   ```
   python -m venv env
   ```
3. Activate the virtual environment
   ```
   #in Windows
    .\env\Scripts\activate

    #in Linux
    source env/bin/activate
   ```
4.  Move into the directory where we have the project files :
    ```
    cd Ecomerce-APIs
    ```
5. Install modules
   ```
   pip install -r requirements.txt
   ```
7. Create .env file
   ```
   touch .env

   ```

8. Migrate database
   ```
   python manage.py migrate
   ```
9. Create superuser
    ```
    python manage.py createsuperuser
    ```
10. Run the project
    ```
    python manage.py runserver
    ```
