# Jenkins

## [Instalación](https://www.jenkins.io/doc/book/installing/linux/)
Ejemplo CentOs 7:
```bash
sudo yum install epel-release -y
sudo yum install java-11-openjdk -y
sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo --no-check-certificate
sudo rpm --import http://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key
sudo yum install jenkins -y
```
```bash
sudo systemctl enable jenkins
sudo systemctl start jenkins
sudo systemctl status jenkins
```

> La cantidad de integraciones `plugins` que tiene Jenkins es lo que lo hace una herramienta tan relevante.

## Backups
Utilizando el plugins `ThinBackups` podemos realizar backups y restores de servidor de Jenkins

## Pipelines
Presentan una estructura similar a:
```groovy
pipeline {
    agent any
    stages {
        stage(<nombre>) {
            steps {
                <plugin> ...
                ...
            }
        }
    }
}
```
> La lógica dentro de steps son llamadas a los diferentes plugins

## Seguridad
Recomiendan el uso de `Matrix-based security` (hace falta instalar el plugin correspondiente)
> [!IMPORTANT]  
> Se debe comprobar la visibilidad de los usuarios cuando se cambian los permisos, ya que es realivamente fácil hacer que un usuario no pueda acceder a ningún recurso

## Plugins
Algunos plugins destacados son:
- **SSH Build Agents:** Nos permite usar agentes sobre el protocolo SSH
- **Pipeline:** Nos ofrece una suite de funcionalidades para automatizar nuestras tareas de *Continuous Delivery (CD)*
- **Blue Ocean:** Mejora de la UI de Jenkins. Una vez instaldo podemos cargarla apuntando al la URL `<url de Jenkins>/blue`

## Extra
### Ejercicio de Kodekloud
<details>
Our application development team has recently finished the MVP development for one of the applications and it's ready to be deployed on production.

The `go-app` repository on the Gitea server contains the source code of this application. The `dev` branch of this repository is used for testing, hence we want to deploy it on the `dev` environment and the `master` branch should be deployed on the production environment.

On `dev` server `/opt/go-app` is the document root of the application and we have already setup the `dev` branch over there for your convenience. In your build step, you will just need to pull the latest `dev` branch code from the repository using `git pull` command. 


Similarly on `production` server `/opt/go-app` is the document root of the application and we have already setup the master branch over there for your convenience. In your build step, you will just need to pull the latest master branch code from the repository using `git pull` command.

Create a pipeline job in Jenkins, and configure it as per details mentioned below:
#### Prerequisites:
- Install the required plugins which are needed for adding SSH agent nodes and for creating pipeline jobs.
- Add dev and production servers as SSH node agents in Jenkins.
- You can use /opt as the Remote root directory for both of these nodes to avoid any permission issues.
- To make nodes work, you will also need to add the respective credentials in Jenkins for these servers.

#### Job configuration:
- The job name should be `go-app-deployment`
- It must be a `pipeline job`.
- The first stage here should be to build the dev branch code which must be deployed on the dev server/environment, you can name the stage as per your choice. As we have already setup the repo/branch on the server so you will just need to run the git pull command.
- The second stage should be to run some unit tests (again you can name the stage as per your choice)
- The last stage for dev would be to deploy the application. You can use a stage like:
```groovy
stage('Deploy Dev') {
    agent {
        label {
            label 'dev'
            customWorkspace "/opt/go-app"
        }
    }
    steps {
        script {
            withEnv(['JENKINS_NODE_COOKIE=do_not_kill']) {
                sh 'go run main.go &'
            }
        }
    }
}
```
> [!TIPS]   
> You must have noticed an extra parameter in this stage i.e `withEnv(['JENKINS_NODE_COOKIE=do_not_kill'])`, it is needed to make sure Jenkins doesn't kill the background process we are starting in this stage on the respective server.

- Similarly configure the same stages (with different name and prod specific values) for the production deployment. So the pipeline will have total 6 stages (three for each environment).
- Make sure to build the job at least once and make sure its building successfully.
</details>

La pipeline creada se encuentra en el fichero [go-app.groovy](./content/go-app.groovy)
- Ya que hemos definido los agentes en cada stage configuramos `agent none` al inicio de la pipeline
- Las label `dev` y `prod` son las que hemos configurado en Jenkins para los nodos

