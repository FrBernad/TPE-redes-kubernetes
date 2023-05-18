# Autores
- [Francisco Bernad](https://github.com/FrBernad)
- [Nicolás Rampoldi](https://github.com/NicolasRampoldi)
- [Agustín Manfredi](https://github.com/imanfredi)

# TP Especial Kubernetes

## Consigna
- Crear un cluster de Kubernetes de un Master y al menos dos slave, que exponga
una API en un puerto genérico (distinto a 80)
- Implementar una base de datos local en un servidor y exponer un servicio que
redireccione el tráfico del cluster al servidor.
- Deployar un web server (nginx o Apache HTTPD escuchando en el 80) y hacer
un proxy reverso a la API. (Usar un ingress controller)
- Mostrar dos versiones de API distintas conviviendo (dos servicios distintos nomás bastan)
- Opcional: Integrar los servicios de Istio y Kiali al cluster.