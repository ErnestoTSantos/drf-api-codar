# REST API com django Rest Framework

## Testes para a API

1. Escrevendo um teste para a API:
    - Precisamos substituir o TestCase do Django, por APITestCase do rest_framework.test.
    - Essa biblioteca é uma sub biblioteca do TestCase do Django, mas com modificações para realizarmos os testes da API.
    - self.client, é o mesmo client que utilizamos anteriormente, só que não precisamos importar de outra classe para poder realizar a ação.
    - Para convertermos os objetos recebidos nos testes, podemos utilizar json.loads, para trocar o tipo de objeto que estamos recebendo, de binário para um objeto python.

2. Testando a criação de Agendamento:
    - Utilizamos o self.client.post('nome da url', dados a serem persistidos)
    - Quando utilizamos POST, PATCH ou PUT, é importante que passemos o formato, se não a requisição pode não ler como está sendo enviado o arquivo.
    - Temos 3 maneiras de verificar se o POST funcionou.
        - Utilizamos o Scheduling.objects.get(), pois o get falha caso não exista nada no objeto ou tenha mais de uma resposta.
        - Podemos testar também utilizando o método get e convertendo os elementos da resposta, para que possamos fazer a verificação dos elementos do dicionário recebido.
    - Podemos colocar no arquivo de settings a seguinte variável: REST_FRAMEWORK = {'TEST_REQUEST_DEFAULT_FORMAT': 'json',}, ela fará com que todos os elementos nos testes sejam no formato JSON

3. Timezones:
    - naive datetime -> É um datetime que não tem noção de fuso horário.
    - O datetime irá verificar o tempo onde estivermos.
    - O django utiliza a variável de ambiente TIME_ZONE, para identificar o fuso horário do lugar.
    - Precisamos passar o timezone no django ao criarmos um objeto.
    - Utilizamos o tzinfo=timezone.utc, para que o objeto adera a essa data.
    - O formato ISO 8601 tenta unificar a apresentação de uma data e hora.
    - Manter sempre duas coisas em mente ao usar datas:
        - Utilizar o padrão ISO 8601, pois é aceito pela maior parte das aplicações.
        - Sempre considerar que o horário será representado/salvo em utc, para representar, não é uma responsabilidade nossa do back, é uma responsábilidade do front converter para o horário local do usuário.
    - É uma boa prática salvarmos em utc.

4. Class Based Views(CBVs):
    - Utilizamos a estrutura FunctionBasedViews.
    - Devemos importar APIView de rest_framework.views.
    - Devemos fazer com que a classe herde de APIView, além disso devemos criar os http methods que iremos utilizar nessa view, com eles recebendo self e a request normalmente.
    - No método, iremos fazer a mesma coisa que fazemos na função, porém como um método da classe.
    - Nas url's precisamos passar a classe e colocar .as_view(), pois não podemos passar como se fossem apenas classes e esse método retorna a classe como uma função para o Django.
    - Além de que, o código fica mais limpo.
    - Os nossos testes devem continuar funcionando, pois não mudamos o comportamento do código, mas sim sua estruturação.

5. Utilizando Mixins:
    - A utilização do ClassBasedViews, trás como principal vantagem a utilização de mixins.
    - Mixins, são objetos que adicionam comportamentos ao método.
    - Podemos importar o pacote todo de mixins, do rest_framework.
    - Precisamos importar também o pacote generics.
    - Para os mixins utilizamos o ListModelMixin para listar os elementos, o CreateModelMixin para criar elementos.
    - Nos generics, utilizamos GenericAPIView sendo uma classe genérica.
    - Para utilizarmos o ListModelMixin, precisamos utilizar self.list() e adicionar ao nosso método *args e **kwargs. Sendo estes argumentos passados pela própria framework. Ao invés de fazermos os passos manualmente, precisamos apenas retornar o self.list com as coisas necessárias.
    - Porém, para fazermos o ListModelMixin funcionar corretamente, precisamos informar duas coisas:
        - A nossa qs.
            - Para instanciarmos ela, no escopo da classe colocamos queryset = forma de buscar objeto no banco...
        - Nosso serializer.
            - Para instanciarmos qual será o serializer, escrevemos serializer_class = Nome do serializer do objeto.
            - Além disso, não precisamos inicar o serializer.
    - Para utilizar o post, precisamos fazer um return em self.create(), passando os *args e **kwargs também.
    - O post também irá utilizar as coisas pré cadastradas.
    - Tudo o que fizemos manualmente antes, é feito por baixo dos panos com a utilização dos mixins.
    - Para pegarmos um elemento específico utilizamos o RetriveModelMixin.
    - Para atualizarmos utilizamos o UpdateModelMixin.
    - Para deletarmos utilizamos o DestroyModelMixin.
    - Precisamos utilizar também o GenericAPIView.
    - No caso do elemento específico, não é necessário ter no método get o id que iremos receber, pois ele será incerido nos kwargs.
    - Para chamarmos o elemento específico, utilizamos o self.retrive(), passando a request, *args e **kwargs.
    - Para realizarmos uma alteração, utilizamos o self.update(), passando a request, *args e **kwargs.
    - Para deletarmos um elemento, utilizamos self.destroy(), passando a request, *args e **kwargs.
    - Precisamos pré setar também a queryset e o serializer.
    - As views genéricas do Django esperam que seja passado como uma pk o elemento a ser buscado.
    - Podemos utilizar lookup_field, para setar qual o valor que iremos utilizar para pesquisar no db.
    - Em teoria é melhor utilizarmos realmente a PK, pois estamos utilizando muitas abstrações no DRF.
    - Ao invés de utilizarmos update no patch, precisamos utilizar self.partial_update(), passando as mesmas coisas.
    - Por conta da utilização dos mixins, podemos ter uma API muito mais rápida e enxuta por conta das abstrações utilizadas.

6. Generics Views:
    - Podemos utilizar a classe ListCreateAPIView, do pacote generics.
    - Podemos remover os métodos get e post, pois como são métodos padrões de um CRUD, já estão sendo realizados por baixo dos panos. Precisamos apenas passar a queryset e a serializer_class.
    - Para pegar elementos específicos, podemos utilizar os generics também.
    - No caso dos elementos específicos, utilizamos a classe RetriveUpdateDestroyAPIView do pacote generics.
    - Os generics, utilizam também os mixins, sendo assim os generics são as mesmas coisas que os mixins, porém com algumas outras coisas.
    - Nem sempre trabalhar com generics ou mixins é a melhor coisa para o projeto.

7. Associando Agendamentos à Usuários:
    - Precisamos a agregar valor para diferentes estabelecimentos.
    - Utilizamos as ForeignKey para linkar com elementos de outras tabelas.
    - related_name é um atalho para interagirmos com o modelo, para conseguirmos referenciar agendamentos pelo modelo do prestador.
    - Para user o related_name='nome da classe que será linkado'.
    - Precisamos usar o atributo on_delete, para ajustarmos o que irá acontecer caso a classe seja excluída.
    - Ao usarmos o models.CASCADE, ao deletarmos a foreignkey, tudo que está relacionado a ela também será excluído.
    - No caso do projeto, como já temos alguns agendamentos, precisaremos passar algum valor, então utilizaremos o usuário administrador, colocaremos o id para que o projeto coloque como default nos agendamentos atuais.
    - Para utilizarmos algo específico na request, criamos o método get_queryset, que é o método chamado pelo DRF.
    - Precisamos pegar o nome do usuário em self.request.query_params.get('username'), para que o nome passado possa ser utilizado na qs.
    - Utilizamos o atributo provider__username=username, para que possamos comparar o nome de usuário do prestador com o passado.
    - Precisamos passar o username da seguinte maneira -> ?username=Ernesto, não é necessário colocar a barra no final.

8. Atualizando nosso serializer:
    - É importante adicionarmos o campo provider no nosso serializer, para que quem consuma a API, possa ver tudo o que é necessário e realizer as validações.
    - Precisamos passar no campo do prestador uma PK, para que o atributo seja relacionado a outra tabela.
    - Podemos validar o provider no serializer, para que possamos passar um nome no post do objeto e não necessariamente a PK.
    - Podemos buscar o elemento pelo id ou pelo usuário, pois ambos tem que ser únicos. Não precisamos passar necessáriamente o id no retorno, podemos retornar apenas o objeto, pois o Django por baixo dos panos pode resolver a situação.
    - Precisamos utilizar um try/except, no except precisamos utilizar User.DoesNotExist.
    - Para que possamos passar como uma str, precisamos colocar o provide como um charfield do serializers.
    - Com isso conseguimos ter uma associação de agendamentos a um certo usuário a um username.
    - No campo fields, podemos colocar '__all__', para que o serializer utilize todos os campos.

9. Autenticação e Autorização:
    - Precisamos ajustar quem pode fazer o que na API, ajustando seus acessos e permissões.
    - Precisamos adicionar um atributo chamado permission_classes, precisamos colocar em uma lista. Precisamos também importar o pacote de permissões, uma das que mais utilizaremos é a IsAuthenticatedOrReadOnly(Para realizar algumas ações o usuário precisa estar logado ou apenas para ler algumas coisas o usuário pode ser anônimo) que vem do pacote permissions do rest_framework.
    - Por padrão quando passamos a utilizar permissões, precisamos ter autenticações também. Por padrão todas as views que tem permissão esperam que passemos alguma autenticação.
    - A forma mais simples de fazermos a autorização é indo em authorization do postman, selecionar Basic Auth que é necessário colocar o usuário e a senha do usuário.
    - Existem inúmeras classes de permissões.

10. Criando uma permissão customizada:
    - Precisamos criar uma nova classe, para que possamos ajustar as permissões.
    - A classe que criamos precisa herdar de permissions.BasePermission.
    - Precisamos colocar nossa classe de permissões em permission_classes.
    - Podemos ter permissões que atuam sobre uma API inteira e outras que atuam apenas sobre algum objeto.

11. Relacionando serializers:
    - Forma de listar ou representar coisas relacionadas a atributos de chaves estrangeiras.
    - Precisamos criar um novo serializer.
    - Como colocarmos um related_name, nós podemos acessar alguns atributos da outra tabela.
    - Precisamos criar uma view, para realizar as listagens do usuário.
    - A classe ListAPIView, só tem o método get atribuido a ela.
    - Ao listarmos algum objeto de outro lugar, o ideal é mostrarmos todas as informações importantes.
    - Podemos acessar os valores do objeto, colocando o serializer dele, com os atributos many=True, read_only=True. Só precisamos colocar como o nome do atributo = serializer.
    - read_only=True, indica que os elementos serão apenas lidos e não serão sobrescritos.
    - Ao alinharmos serializers, nos os alinhamos, pois estamos acessando valores por ele.
    - É perigoso demais deixar uma view que tem serializers aninhados sem permissão alguma.