# Infraestrutura: Configuração e dependências externas

1. Consumindo uma API externa:
    * Utilizaremos a API BrasilAPI, para verificar os feriados.
    * Utilizaremos a biblioteca requests, para verificarmos os dados das datas, para verificar os feriados.
    * Precisamos instalar a biblioteca requests, para instalarmos precisamos fazer o pip install requests.
    * Colocamos geralmente funções que são utilizadas mais de uma vez no mesmo código no arquivo utils.py.
    * Colocamos o nome da variável.json(), para convertermos os elementos recuperados na API.
    * Precisamos colocar a validação no nosso serializer e na nossa view de horários.
    * Além disso precisamos converter a data de str para um tipo data, para que possamos comparar com a data passada pelo usuário.
    * Devemos considerar as regras de negócios, para variar como resolver as situações.

2. Testes e dependências externas:
    * Precisamos ajustar os testes, para evitar que falhem por conta da API externa.
    * Podemos utilizar uma variável de configuração, para ajustar os erros.
    * Utilizamos o django.conf, para ajustar as variáveis de ambiente.
    * Utilizamos a biblioteca sys, para analizarmos os elementos que estão chamando o manage.py.
    * Criamos a variável TESTING, com alguns parametros utilizando o sys.argv e assim testamos para ver se é um teste ou não.
    * Ao utilizamos o TESTING, nós estamos enganando o código.

3. Evitando chamadas externas nos testes:
    * Precisamos importar de Django.conf import settings, para podermos acessar as variáveis do arquivo settings.py, utilizamos essa maneira, pois não é uma boa prática chamar direto o arquivo.
    * Podemos chamar o último elemento da lista utilizando o [-1], assim evitando fazer um código extremamente mirabolante para chegar ao resultado.
    * Como nos outros testes, aqui nós também passamos as coisas como padrão, os query_params e elementos da url.

4. Utilizando mocks:
    * O jeito certo de testar dependências é mockando, ou seja isolando as dependências.
    * Utilizamos os mocks para substituir um comportamento.
    * Precisamos importar mock do unittest.
    * Precisamos adicionar um decorator no método com o mock, para que possamos passar os valores.
    * Utilizaremos mock.patch(), para que possamos substituir os elementos.
    * Passamos o caminho da função que queremos mockar no patch e podemos colocar a forma de retorno do valor.
    * Precisamos colocar uma variável para receber o mock no método.

5. O que é Test coverage:
    * Verifica quantos % do código está coberto por testes.
    * Geralmente testes não cobrem 100% do programa, por isso o coverage é útil, com ele podemos verificar o que está faltando para testarmos.
    * Não é muito comum termos 100% do código sempre.
    * Facilita a interação do dev com o código em si.

6. Adicionando Test Coverage ao nosso projeto:
    * Pytest é uma biblioteca que é um framework de tests, é compativel com o unittest.
    * Facilita fazer a integração de teste coverage no projeto django.
    * Precisamos instalar "pip install pytest-cov pytest-django"
    * Precisamos criar na raiz do projeto o arquivo pytest.ini.
    * Precisamos fazer o arquivo pytest indicar para o settings da aplicação.
    * Precisamos informar como os testes são encontrados, pela variável python_files=.
    * Para rodarmos o teste, precisamos utilizar apenas o comando pytest.
    * Pytest, roda tanto testes do unittes, quanto testes mais simples que são apenas funções.
    * Para usarmos junto o coverage, ao rodarmos o pytest, devemos chamar o comando como pytest --cov.
    * O addopts serve para configurar algumas coisas dos testes. Podendo trazer um relatório mais enxuto e de fácil compreensão.
    * A cobertura de testes, não significa que o código não tem bugs, porém ajuda a ver quais trechos de código não foram testados e precisam ser averiguados.

7. Django Settings:
    * Geralmente temos dois ambientes:
        * Desenvolvimento -> Onde nós podemos fazer coisas mais "livres"
        * Produção -> Com mais restrições, mais engessado 
    * Quando debug está igual a True, e ALLOWED_HOSTS é igual a uma lista vazia, temos o ambiente e formato de desenvolvimento.
    * Devemos criar uma pasta nomeada de settings e devemos renomear o arquivo settings.py para base.py, pois todas as novas configurações devem "herdar" de base.py.
    * É comum cada arquivo de configuração ter sua própria secret key.
    * Precisamos criar o arquivo __init__.py na pasta para ser considerado um módulo.
    * Para que o programa rode normalmente precisamos mudar algumas configurações padrão.
        * Arquivo asgi.py -> Devemos modificar o setdefault, para o nome da pasta com o arquivo que desejamos utilizar.
        * Arquivo wsgi.py -> Devemos modificar também o setdefault, para o nome da pasta com o arquivo que utilizaremos.
        * Arquivo manage.py -> Também devemos modificar o setdefault, para o novo nome do arquivo.
    * Precisamos adicionar mais um parent no BASE_DIR do arquivo base.py, para que ele acesse o db na raiz do projeto.
    * As configurações tendem a crescer junto do projeto.
    * É comum utilizarmos diferentes db nos projetos e nos ambientes.
    * Não é correto ter valores como a secret key subindo para o git
    * Precisamos usar a biblioteca os, para pegarmos os elementos de outro arquivo, neste caso utilizamos o os.environ.get().

8. Arquivo dotenv:
    * Usar variáveis de ambiente ajuda na segurança do projeto.
    * Utilizamos o arquivo ".env", para ajustar variáveis de ambiente, para evitar passarmos pela linha de comando ou deixarmos expostas no código.
    * Podemos utilizar a biblioteca python-dotenv, para acessarmos variáveis nos arquivos ".env".
    * Precisamos importar do dotenv load_dotenv.
    * Podemos gerar uma nova secret key pela biblioteca secret, com o método token_urlsafe().

9. Logging:
    * São utilizados para fornecer um "rastro" do que aconteceu.
    * Existem 5 níveis.
        * Debug
        * Info
        * Warning
        * Error
        * Critical
    * Utilizamos a biblioteca logging e dela mesma podemos utilizar os níveis dentro do código.
    * Podemos utilizar o logging, para evitar raises.
    * Precisamos configurar o logging no base.py, para termos acesso em todos os arquivos de settings.
    * Para uma "melhor" configuração, devemos modificar a configuração, para que no ambiente de desenvolvimento possamos ter um controle maior.
    * Por utilizarmos a biblioteca logging, é criado um arquivo na raiz, para demonstrar os logs que ocorreram.
    * Grande parte das aplicações vão ter logs configurados e pode ter uma ferramenta para verificação de logs, como datadog ou splank.

10. Gerenciando dependências do projeto:
    * Podemos usar o comando pip list, para listar todas as bibliotecas que temos no projeto.
    * Utilizamos o comando pip freeze > requirements.txt para salvar os elementos instalados no projeto.
    * Para instalar as bibliotecas utilizamos o comando pip install -r requirements.txt, com a venv ativa.
    * Algumas dependências não precisam ser instaladas em todos os ambientes, um exmplo são os testes.
    * Podemos criar uma pasta com os requirements.txt e passar os requirements necessários para cada ambiente.
    * Podemos fazer com que os requirements de diferentes ambientes herdem de um base, para que possamos organizar as coisas necessárias.
    * Colocamos no topo -r "nome do arquivo.txt" para que ele herde as coisas que existam.
    * Para instalar as coisas quando organizamos dessa maneira, utilizamos o comando "pip install -r requirements/"ambiente.txt"
    