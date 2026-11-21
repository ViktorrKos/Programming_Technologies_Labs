# Lab 4 Jenkins

CI/CD-конвеєр у Jenkins (Jenkins працює в Docker): `Check scm → Build → Test → Image building → Push to Docker Hub`.
Застосунок — простий Flask-сервіс, тести — `unittest` з XML-звітом для Jenkins.

## Файли

| Файл | Призначення |
|---|---|
| `app.py` | Flask-застосунок |
| `app_tests.py` | Модульні тести, пишуть звіт у `test-reports/*.xml` |
| `requirements.txt`, `requirements-test.txt` | Залежності застосунку / тестів |
| `Dockerfile` | Образ застосунку (його збирає й пушить конвеєр) |
| `Dockerfile.jenkins` | Образ Jenkins з Docker CLI |
| `Jenkinsfile` | Декларативний конвеєр |

## 1. Запуск Jenkins у Docker (PowerShell)

```powershell
docker volume create jenkins_home
docker network create jenkins

docker run --name jenkins-docker --detach --privileged --network jenkins --network-alias docker --env DOCKER_TLS_CERTDIR=/certs --volume jenkins-docker-certs:/certs/client --volume jenkins_home:/var/jenkins_home --restart unless-stopped docker:dind

docker build -f Dockerfile.jenkins -t lab4-jenkins:1.0 .

docker run --name jenkins-lab4 --detach --network jenkins --env DOCKER_HOST=tcp://docker:2376 --env DOCKER_CERT_PATH=/certs/client --env DOCKER_TLS_VERIFY=1 --volume jenkins_home:/var/jenkins_home --volume jenkins-docker-certs:/certs/client:ro --publish 8085:8080 --publish 50000:50000 --restart unless-stopped lab4-jenkins:1.0
```

Пароль для першого входу:

```powershell
docker logs jenkins-lab4
```

Відкрити http://localhost:8085 → вставити пароль → **Install suggested plugins** → створити адміністратора.
Потім **Manage Jenkins → Plugins → Available**: переконатись, що встановлені `Docker Pipeline`, `GitHub`, `Timestamper`, `JUnit`.

## 2. GitHub

1. GitHub → Settings → Developer settings → Personal access tokens (classic) → scopes `repo`, `admin:repo_hook`.
2. Jenkins → Manage Jenkins → Credentials → System → Global → Add Credentials:
   Kind **Secret text**, Secret = токен, ID = `github-token`.
3. Manage Jenkins → System → **GitHub Servers** → Add: API URL `https://api.github.com`, Credentials = `github-token`, **Test connection**.

Якщо репозиторій приватний, додайте ще credentials типу *Username with password* (логін GitHub + той самий токен) і вкажіть їх у налаштуваннях Pipeline. Для публічного репозиторію не потрібно.

## 3. Docker Hub

1. hub.docker.com → Account Settings → Personal access tokens → New (Read & Write).
2. Jenkins → Credentials → Add: Kind **Username with password**, Username = логін Docker Hub, Password = токен, ID = `dockerhub-creds`.
3. У `Jenkinsfile` замінити `YOUR_DOCKERHUB_LOGIN` на свій логін.

## 4. Задача Pipeline

New Item → `lab4-pipeline` → **Pipeline** → OK:

- Discard old builds: Max # of builds to keep = 10
- Definition: **Pipeline script from SCM**
- SCM: Git, Repository URL: `https://github.com/<логін>/lab4-jenkins.git`
- Branch Specifier: `*/main`
- Script Path: `Jenkinsfile`

Save → **Build Now** → дивитись Stage View і Console Output.

## 5. Тригери (Configure → Build Triggers)

| Тригер | Налаштування |
|---|---|
| Періодично | *Build periodically*: `H/5 * * * *` |
| Опитування SCM | *Poll SCM*: `* * * * *` (для демонстрації), потім зробити commit + push |
| GitHub hook | *GitHub hook trigger for GITScm polling*; webhook на `<публічний URL>/github-webhook/` (для localhost — тунель, напр. `ngrok http 8085`) |
| Віддалено | *Trigger builds remotely*: Authentication Token = `lab4-token` |

Віддалений запуск (API-токен: правий верхній кут → ім'я користувача → Security → Add new Token):

```powershell
curl.exe -X POST -u admin:<API_TOKEN> "http://localhost:8085/job/lab4-pipeline/build?token=lab4-token"
```

Очікувана відповідь — `201`, у списку збірок з'являється нова.

## 6. Перевірка образу з Docker Hub

```powershell
docker rmi <логін>/lab4-flask-app:latest
docker pull <логін>/lab4-flask-app:latest
docker run --rm -d -p 5000:5000 --name lab4-app <логін>/lab4-flask-app:latest
curl.exe http://localhost:5000
docker stop lab4-app
```

## Типові проблеми

- **`Cannot connect to the Docker daemon`** у збірці — перевірте `docker ps` (мають працювати `jenkins-docker` і `jenkins-lab4`) та що Jenkins запущено з `--network jenkins` і трьома `DOCKER_*` змінними.
- **`docker: not found`** — Jenkins запущено з готового образу, а не з `lab4-jenkins:1.0`.
- **`Waiting for next available executor`** — Manage Jenkins → Nodes → Built-In Node → Number of executors = 2.
- **`ModuleNotFoundError: xmlrunner`** — пакет називається `unittest-xml-reporting` (а не `xmlrunner`).
- **`denied: requested access to the resource is denied`** при push — `IMAGE_NAME` має починатись з вашого логіну Docker Hub, токен має права Read & Write.
- Щоб побачити «червону» збірку, змініть текст у `app.py`, не чіпаючи тест, і зробіть push.
