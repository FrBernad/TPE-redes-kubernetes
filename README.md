# Autores

- [Francisco Bernad](https://github.com/FrBernad)
- [Nicolás Rampoldi](https://github.com/NicolasRampoldi)
- [Agustín Manfredi](https://github.com/imanfredi)

# TP Especial Kubernetes

## Consigna

- Crear un cluster de Kubernetes de un Master y al menos dos slave, que exponga
  una API en un puerto genérico (distinto a 80). Exhibir como la información es enviada
  desde distintos Pods.
- Implementar una base de datos local en un servidor (fuera del cluster de Kubernetes)
  y exponer un servicio de Kubernetes que redireccione el tráfico del cluster al servidor.
- Deployar un web server (nginx o Apache HTTPD escuchando en el 80) y hacer
  un proxy reverso a la API. Puede utilizarse un ingress controller.
- Mostrar dos versiones de API distintas conviviendo.
- Opcional: Integrar los servicios de Istio y Kiali al cluster.

# Instalación

## Entorno

El proceso de instalación y ejecución será detallado para un ambiente de trabajo con Ubuntu 22.04.2 LTS y aproximadamente 10 GB de memoria libres.

## Docker

Para poder inicializar el cluster de Kubernetes es necesario contar con Docker instalado.
A continuación se mostrarán los pasos sobre cómo realizar la [instalación de Docker en Ubuntu](https://docs.docker.com/engine/install/ubuntu/).

### Desintalación de versiones obsoletas

Para asegurar una instalación desde cero se asegurará que el sistema no cuente con versiones ya instaladas de las componentes de Docker.

```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
```

### Instalación utilizando el repositorio apt

### Set up del repositorio

Se agregará el repositorio con las componentes de Docker al administrador de paquetes del sistema.

```bash
sudo apt-get update
```

```bash
sudo apt-get install ca-certificates curl gnupg
```

```bash
sudo install -m 0755 -d /etc/apt/keyrings
```

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

```bash
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

```bash
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### Instalación del docker engine

Una vez agregado el repositorio, se procederá a instalar las componentes de Docker.

```bash
sudo apt-get update
```

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

```bash
sudo docker run --rm hello-world
```

Este último comando descarga la imagen hello-world y ejecuta el contenedor. Si ves un mensaje de confirmación, Docker ha sido instalado correctamente.

Puede encontrar más detalles sobre cómo realizar la instalación en otros sistemas operativos en el siguiente [link](https://docs.docker.com/engine/install/)

### Creación de usuario y grupo de docker

Para evitar ejecutar los contenedores como root, será necesario crear el grupo docker y agregar el usuario del sistema al mismo. Esto se logra con los siguientes comandos.

Se crea el grupo de docker.

```bash
sudo groupadd docker
```

Se agrega el usuario del sistema al grupo.

```bash
sudo usermod -aG docker ${USER}
```

Será necesario reiniciar la sesión del usuario para que se apliquen los cambios.

Una vez realizado esto, verificar que se pueda ejecutar el siguiente comando y que se obtenga la salida mencionada anteriormente.

```bash
docker run --rm hello-world
```

Ya instalado Docker, procederemos a eliminar la imagen descargada.

```bash
docker rmi hello-world
```

## Kubectl

Kubectl es una herramienta de línea de comandos que permite interactuar y gestionar el clúster de Kubernetes. Más aún, brinda la capacidad de desplegar, escalar, gestionar recursos, inspeccionar y depurar aplicaciones, como así también realizar actualizaciones en el clúster.

### Instalación

Se procederá a descargar la última versión con el siguiente comando:

```bash
- Para AMD64 / x86_64:
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
- Para ARM64:
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/arm64/kubectl" 
```

Una vez descargado, se instalará Kubectl

```bash
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

Una vez instalado, deberá asegurarse que la versión instalada sea la correcta utilizando el comando:

```bash
kubectl version --client
```

Este comando va a generar el siguiente warning:

```
WARNING: This version information is deprecated and will be replaced with the output from kubectl version --short.
```

Este warning puede ser ignorado ya que solo estamos asegurando que la instalación fue exitosa.

Puede encontrar más detalles sobre cómo realizar la instalación en otros sistemas operativos en el siguiente [link](https://kubernetes.io/docs/tasks/tools/#kubectl).

## Kind

Kind (Kubernetes IN Docker) es una herramienta ligera y fácil de utilizar que permite crear clústers de Kubernetes de manera local utilizando contenedores de Docker como nodos. Proporciona un entorno de desarrollo y de pruebas rápido y aislado para desplegar y probar aplicaciones en Kubernetes. Más aún, permite especificar la cantidad de nodos worker y de nodos del control plane del clúster sin necesidad de infraestructura compleja ni recursos adicionales.

### Instalación

A continuación se indicarán los pasos a seguir para realizar la[instalación de Kind en Linux](https://kind.sigs.k8s.io/docs/user/quick-start/#installing-from-release-binaries).

Primero, deberá descargarse el ejecutable compatible con la arquitectura del sistema a utilizar.

```bash
- Para AMD64 / x86_64
[ $(uname -m) = x86_64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.19.0/kind-linux-amd64
- Para ARM64
[ $(uname -m) = aarch64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.19.0/kind-linux-arm64
```

Una vez descargado, se le dará permiso de ejecución al binario.

```bash
chmod +x ./kind
```

Finalmente, se desplazará el archivo hacia un directorio que se encuentre dentro de la variable de entorno $PATH.

```bash
sudo mv ./kind /usr/local/bin/kind
```

Puede encontrar más detalles sobre cómo realizar la instalación en otros sistemas operativos en el siguiente [link](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)

### Creación de cluster

Antes de comenzar, deberá clonar el repositorio del siguiente [link de Github](https://github.com/FrBernad/TPE-redes-kubernetes)
Puede ejecutar el siguiente comando para hacerlo:

```bash
git clone https://github.com/FrBernad/TPE-redes-kubernetes.git
```

Una vez clonado, deberá cambiar al directorio del repositorio.

```bash
cd ./TPE-redes-kubernetes
```

En los pasos a continuación, se indicará cómo levantar un clúster de kubernetes para obtener una aplicación con la siguiente arquitectura:

![alt text](./assets/diagram.png "Diagrama")

En primer lugar, se realizará el build de la imagen de la base de datos. Esta imagen no será instanciada dentro del clúster de Kubernetes. El clúster se comunicará con la base de datos mediante un servicio de Kubernetes encargado de exponerla. De esta manera, se podrá simular que la base de datos actúe como un servicio externo cumpliendo con la consigna pedida.

Se instanciará el contenedor con docker-compose, que se encargará de buildear la imagen de la base de datos, establecer las variables de entorno necesarias, configurar el volumen persistente para el almacenamiento y por último llenarla con registros con información de películas.

```bash
docker compose  -f ./database/docker-compose.yml up -d
```

A continuación, se creará el clúster de Kubernetes utilizando la configuración que se encuentra en el archivo kind-config/multi-cluster-config.yaml bajo el nombre de "redes". En el archivo se especifica la cantidad de nodos worker y de nodos del control plane. Para cumplir con el enunciado, se configurará un nodo master y dos slaves.

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
  - role: worker
  - role: worker
```

Para la creación del clúster deberá ejecutarse el siguiente comando:

```bash
kind create cluster --config kind-config/multi-cluster-config.yaml --name redes
```

Esto instancia un clúster dentro del contexto "redes". Tener en cuenta que puede demorar unos minutos.
Una vez inicializado el clúster, se podrán visualizar los clústers disponibles con el siguiente comando:

```bash
kind get clusters
```

Además, podrá observarse información específica del clúster de la siguiente manera:

```bash
kubectl cluster-info
```

Por último, podrán visualizarse los tres nodos en ejecución con el siguiente comando:

```bash
kubectl get nodes
```

A continuación, se generarán las imágenes para instanciar los contenedores que ejecutarán en los nodos worker.

El objetivo es tener dos versiones distintas de la misma API que consulten la base de datos externa levantada previamente. A diferencia de la versión 1, la versión 2 retornará campos adicionales en la respuesta. Más adelante se detallará un ejemplo.

Para generar la versión 1 de la API, deberá ejecutarse el siguiente comando:

```bash
docker build -t movies:v1 ./k8/backend/movies/v1/image
```

Esto creará una imagen con el tag **_movies:v1_**

Para generar la versión 2 de la API, deberá ejecutarse el siguiente comando:

```bash
docker build -t movies:v2 ./k8/backend/movies/v2/image
```

Esto creará una imagen con el tag **_movies:v2_**

Será necesario cargar las imágenes dentro clúster para poder instanciarlas. Esto puede realizarse utilizando los comandos a continuación:

```bash
kind load docker-image movies:v1 --name redes
```

```bash
kind load docker-image movies:v2 --name redes
```

En ambos casos, las imágenes no se encontrarán presentes en los nodos y por lo tanto serán añadidas.

Luego, se procederá a aplicar el manifiesto de la base de datos que se encargará de levantar un servicio de tipo ExternalName. Este tipo de servicios, permiten la comunicación mediante DNS de los demás servicios y/o pods dentro del clúster con la base de datos externa levantada anteriormente.

```bash
kubectl apply -f ./k8/database
```

Para poder resolver consultas DNS hacia la base de datos, se deberá configurar una entrada de manera local en la máquina del host. Primero, deberá obtenerse la ip del host.

```bash
ip a
```

Deberá seleccionarse una IP asignada a cualquier interfaz que no sea loopback. Por ejemplo podría ser la interfaz de docker o la interfaz física.

Agregaremos en nuestro archivo /etc/hosts la siguiente línea.Se procederá a agregar en el archivo /etc/hosts la siguiente línea con la IP seleccionada previamente.

> [IP base de datos] database

Una vez hecho esto, se aplicarán los manifiestos encargados de desplegar las componentes backend y los servicios que permitirán la comunicación con los pods del mismo.

Primero, se aplicará el objeto de kubernetes de tipo Secret. Este permite establecer variables de entorno para configurar los Pods del backend.

```bash
kubectl apply -f ./k8/backend/movies/secret.yaml
```

Luego, se procederá a aplicar los manifiestos de ambas versiones del backend. Estos podrán ser encontrados dentro del directorio V1 y  el directorio V2 dentro de archivos .yaml. 

Por un lado, el manifiesto "backend-deployment.yaml", se encargará de levantar un Deployment con un Replica Set de tres réplicas. De esta manera, se asegurará redundancia y escalabilidad en la arquitectura. En la declaración de los Pods se define el label app:movies-vX-backend (donde X será 1 o 2 según la versión que corresponda), y en el Replica Set un selector para los mismos que le permitirá monitorear el estado de los Pods. El Replica Set  se utiliza para garantizar que se encuentren tres Pods ejecutándose en todo momento. En el caso de que alguno se encuentre caído, se encargará de eliminarlo y crear uno nuevo.

Cada una de estas réplicas se ejecuta en un Pod distinto, otorgándoles un ID diferente. Incluso, puede haber Pods que se encuentren en distintos nodos. En la respuesta de la API, podrá observarse en qué nodo worker se encuentra el Pod que emite la respuesta, el  identificador del mismo y su IP dentro de la red del clúster de Kubernetes.

Por otro lado, el manifiesto "backend-service.yaml" se encargará de levantar un Service de tipo Cluster IP que permitirá el acceso centralizado a los Pods para las distintas componentes dentro del clúster. Dado que los Pods son efímeros, estos pueden fallar y reiniciarse en cualquier momento, provocando cambios en la IP asignada. El Service utiliza un selector que monitorea el label definido en cada una de las réplicas permitiendo acceder a los Pods de manera centralizada, sin tener que contar con conocimiento sobre la IP de los mismos. Este componente posee una IP fija, solucionando el problema del cambio constante de IPs.  Como se mencionó previamente, los servicios son utilizados para permitir la comunicación interna dentro del clúster sin tener que conocer la IP de cada pod. Estos exponen un nombre que será resuelto por el servicio DNS interno que posee Kubernetes para facilitar el acceso al mismo. Cada vez que se realice un pedido al servicio, este se encargará de delegarlo a uno de los Pods utilizando un algoritmo de balanceo round robin.

De este modo, por cada versión de la API se tendrá: un Deployment, un Replica Set con tres réplicas y un servicio para exponer el acceso centralizado a los Pods.

Se procederá a aplicar los manifiestos:


```bash
kubectl apply -f ./k8/backend/movies/v1
```

```bash
kubectl apply -f ./k8/backend/movies/v2
```

Por último, se aplicará el manifiesto del Ingress. Este componente actuará como punto de acceso externo al clúster de kubernetes. Recordar que los servicios de tipo Cluster IP levantados previamente, son accesibles únicamente dentro del clúster. A diferencia de estos, el ingress permite el acceso desde afuera del cluster.

Para poder configurar un Ingress, deberá utilizarse un Ingress Controller. En este caso se configurará el Ingress Controller de Nginx. Este es uno de los más utilizados hoy en día debido a las funcionalidades que brinda. Entre estas destacan: enrutamiento basado en hosts y rutas, balanceo de carga, soporte para TLS/SSL y redirecciones y reescrituras.

El Ingress definirá reglas de redirección para el nombre api.movies.com. Para poder ser accedido localmente mediante DNS, será necesario agregar la siguiente entrada en el archivo /etc/hosts.

```
127.0.0.1 api.movies.com
```

Se procederá a aplicar los manifiestos del Ingress con el siguiente comando:

```bash
kubectl apply -f ./k8/ingress --recursive
```

Luego, se deberá verificar que el ingress-controller esté ejecutando correctamente mediante el comando:

```bash
kubectl -n ingress-nginx get pods
```

Una vez verificado esto, se realizará un port forwarding del servicio del ingress-controller:

```bash
kubectl -n ingress-nginx port-forward svc/ingress-nginx-controller --address 0.0.0.0 5000:80&
```

Esto es necesario ya que en un caso real, el Ingress tendría asignada una IP pública para accederlo. En este caso, al estar trabajando en un ambiente local, no contará con una IP pública. Debido a esto, se fowardeará el servicio para que pueda ser accedido desde fuera del clúster por la máquina host.

Una vez configurado el Ingress, se podrán realizar llamados a la API en sus respectivos endpoints.

```bash
curl -i "api.movies.com:5000/v1/"
curl -i "api.movies.com:5000/v1/movies?name=titanic"
```

```bash
curl -i "api.movies.com:5000/v2/"
curl -i "api.movies.com:5000/v2/movies?name=titanic"
```

Si desea, puede probar con diferentes nombres de películas, cambiando el valor del parámetro name.

En las respuestas de cada llamado, además de la información del endpoint, puede observarse la IP y nombre del Pod que emitió la respuesta y el nombre del nodo en el que se encuentra.

### Monitoreo del cluster

Para el monitoreo del clúster se utilizarán las herramientas Istio y Kiali, junto a otras utilidades como Prometheus. Istio es un service mesh que permite controlar el tráfico entre las componentes dentro del clúster de kubernetes. Por otro lado, Kiali permite visualizar, mediante una interfaz gráfica, el estado de cada componente de la red recolectando métricas con Prometheus.

Para realizar el monitoreo, es necesario eliminar los manifiestos aplicados anteriormente para que la herramienta sea capaz de configurar las componentes.


```bash
kubectl delete -f ./k8/database
kubectl delete -f ./k8/backend/movies/secret.yaml
kubectl delete -f ./k8/backend/movies/v1
kubectl delete -f ./k8/backend/movies/v2
kubectl delete -f ./k8/ingress --recursive
```

- Tener en cuenta que el último comando puede llevar unos minutos.

#### Instalación

```bash
curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.18.0 sh -
```

```bash
cd istio-1.18.0
```

```bash
export PATH="$PATH:$PWD/bin"
```

```bash
cd ..
```

Verificamos la instalación con el comando:

```bash
istioctl x precheck
```

#### Monitoreo

Se configurará el servicio de Istio dentro del cluster con el siguiente comando:

```bash
istioctl install --set profile=default -y
```

```bash
kubectl label namespace default istio-injection=enabled
```

Luego, se agregarán Kiali y Prometheus al clúster con los siguientes comandos:

```bash
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.18/samples/addons/kiali.yaml
```

```bash
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.18/samples/addons/prometheus.yaml
```

Una vez levantados estos servicios, se volverán a aplicar los manifiestos levantando los componentes del cluster.

```bash
kubectl apply -f ./k8/database
kubectl apply -f ./k8/backend/movies/secret.yaml
kubectl apply -f ./k8/backend/movies/v1
kubectl apply -f ./k8/backend/movies/v2
kubectl apply -f ./k8/ingress --recursive
```

Puede observarse el estado de los Pods dentro del namespace default con el siguiente comando:

```bash
kubectl get pods
```

Puede observarse  el estado de los pods dentro del namespace del Ingress de Nginx. Nuevamente se deberá esperar hasta que se encuentren en el siguiente estado:

```bash
kubectl -n ingress-nginx get pods
```

Analizando la salida de los comandos anteriores, puede observarse que se cuenta con dos contenedores corriendo en cada Pod. Esto se debe a que Istio inyecta un contenedor extra para poder funcionar. Este contenedor es conocido como "side-car".

Para poder visualizar la configuración de Istio, se realizará un port forwarding de la interfaz visual de Kiali.


```bash
istioctl dashboard kiali --address 0.0.0.0 &
```

Para generar tráfico en el clúster y observar a Istio en acción, se ejecutará el siguiente comando:

```bash
while sleep 1; do curl "api.movies.com:5000/v1/movies?name=titanic" && curl  "api.movies.com:5000/v2/movies?name=titanic"; done
```

## Frontend

Adicionalmente, se puede interactuar con el clúster desde un frontend con una interfaz visual. Para ello será necesario instalar node 18 LTS con el siguiente comando:

```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - &&\
sudo apt-get install -y nodejs 
```

Luego, se deberá ingresar a la carpeta del frontend y ejecutar:

```bash
cd frontend
npm install
npm run dev
```

Por último, se deberá acceder desde un browser a la IP indicada por el output del comando anterior.

La interfaz permitirá realizar consultas hacia las distintas APIs. De esta manera, se podrá observar como para la misma película se obtienen salidas distintas. 

Además, se podrá visualizar la siguiente información sobre el Pod que emite la respuesta:
- IP del Pod.
- Nombre del Pod.
- Nodo donde se encuentra el Pod.