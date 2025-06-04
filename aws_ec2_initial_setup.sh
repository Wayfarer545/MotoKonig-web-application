# 1. Подключаемся к серверу
ssh -i "Frankfurt_ec2.pem" ec2-user@ec2-3-71-173-220.eu-central-1.compute.amazonaws.com

# 2. Обновляем систему
sudo yum update -y

# 3. Устанавливаем Docker
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# 4. Устанавливаем Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 5. Устанавливаем git
sudo yum install -y git

# 6. Создаём директорию проекта
mkdir -p /home/ec2-user/motokonig
cd /home/ec2-user/motokonig

# 7. Генерируем SSH ключ для GitLab (без пароля)
ssh-keygen -t ed25519 -f ~/.ssh/gitlab_deploy -N ""
cat ~/.ssh/gitlab_deploy.pub  # Копируем и добавляем в Deploy Keys в GitLab

# 8. Выходим и заходим снова (для применения группы docker)
exit