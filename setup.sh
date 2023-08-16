sudo pip3 install -r requirements.txt

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic

sudo cp voximplant_medsenger_bot.conf /etc/supervisor/conf.d/
sudo cp voximplant_nginx.conf /etc/nginx/sites-enabled/
sudo supervisorctl update
sudo systemctl restart nginx
sudo certbot --nginx -d courses.ai.medsenger.ru
vim .env