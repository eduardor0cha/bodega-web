# Bodega Web

Para rodar o projeto no seu dispositivo, siga os seguintes passos:

> Antes de iniciar, é recomendável que faça os procedimentos dentro de um ambiente virtual
> Acesse a [documentação do Python](https://docs.python.org/pt-br/3/tutorial/venv.html) para saber mais.

## Instale as bibliotecas

Já dentro do diretório desse projeto, execute o seguinte comando:

```shell
pip install -r requirements.txt
```

## Gere o arquivo do banco de dados

Para criar/sincronizar o arquivo do banco de dados, execute:

```shell
python3 manage.py migrate
```

## Insira os dados base (opcional)

Para adicionar alguns dados pré-definidos, como os produtos, execute:

```shell
python3 manage.py loaddata default-data.json
```

Esse comando adicionará alguns produtos iniciais, e um super usuário de username "admin" e senha "admin".

# Rode o programa

Para iniciar o servidor local, execute: 

```shell
python3 manage.py runserver 
```
