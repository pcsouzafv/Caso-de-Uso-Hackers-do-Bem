Introdução
Neste estudo de caso, assumiremos o papel de um desenvolvedor individual encarregado de criar, implementar e assegurar a segurança de um sistema simples de gerenciamento de tarefas pessoais, aplicando conceitos de Introdução ao SDLC, Modelos e Metodologias SDLC, Introdução ao DevOps, Desenvolvimento Seguro de Software, Containers e Docker, e DevSecOps.

Etapa 1: Planejamento e Definição de Requisitos
Iniciar um projeto de desenvolvimento de software sem um entendimento claro dos requisitos é como iniciar uma viagem sem um destino em mente. Portanto, sua primeira tarefa é analisar e entender os requisitos do sistema de gerenciamento de tarefas pessoais.

Análise de Requisitos

Comece fazendo uma lista dos requisitos que você acredita serem necessários para o sistema de gerenciamento de tarefas pessoais. Por exemplo, o sistema deve ser capaz de autenticar os usuarios, permitir que os usuários criem, editem, excluam e visualizem suas tarefas, permitir que os usuários pesquisem tarefas por palavras-chave,etc.

Requisitos obrigatórios:

autenticação é obrigatoria antes de qualquer ação

aplicação deve gerar log de suas atividades via syslog, bem como sucesso ou fracasso nas autenticações

Requisitos Funcionais e Não Funcionais

Depois de identificar os requisitos, divida-os em requisitos funcionais e não funcionais.

Requisitos funcionais são características que o sistema deve ter para cumprir sua função (por exemplo, processar pedidos).

Requisitos não funcionais são características relacionadas ao desempenho do sistema, como velocidade, segurança e usabilidade.

Casos de Uso e Fluxos de Sistema

Em seguida, crie casos de uso para descrever como os usuários interagem com o sistema. Por exemplo, um caso de uso pode ser "Usuário faz um pedido".

Além disso, desenhe fluxos de sistema para mostrar como as diferentes partes do sistema interagem entre si.

Ameaças de Segurança e Medidas de Mitigação

Por último, mas não menos importante, pense nas possíveis ameaças de segurança que o sistema pode enfrentar e como mitigá-las. Por exemplo:

como você protegerá os dados dos usuários?

Como evitará ataques de negação de serviço?

o que será gerado nos logs como violação de segurança?

Esta etapa é crucial para garantir que o sistema seja seguro e confiável.

Arquitetura do Sistema

A arquitetura do sistema de pedidos de delivery deve ser dividida em duas partes principais:

Back-end (servidor): Esta parte do sistema lidará com o processamento de pedidos, a lógica de negócios e a interação com o banco de dados. Você deve desenvolver este componente usando a linguagem de programação Python e o framework Flask.

Front-end (cliente): Esta parte do sistema é a interface do usuário que interage com os clientes. É aqui que os usuários verão o menu, selecionarão seus itens e farão o pedido. Você deve desenvolver este componente usando HTML, CSS e JavaScript.

Etapa 2: Desenvolvimento do Sistema
Nesta etapa, você deve analisar o codigo-fonte base fornecido para o sistema e adaptá-lo ou modificá-lo de modo a atender os requisitos que foram especificados.

O sistema deve ser preparado de modo a que possa ser executado em um container Docker.

Certifique-se de que o Python e Flask estão instalados no seu ambiente de desenvolvimento.

Em seguida, adapte a aplicação base de gerenciamento de tarefas pessoais, usando python e flask, conforme os requisitos especificados na etapa 1.

git clone https://github.com/AdityaBagad/Task-Manager-using-Flask.git

pip3 install -r requirements.txt

python run.py

Etapa 3: Criação de um pipeline CI/CD
Após criada e testada inicialmente a aplicação, voce deve iniciar a criação um pipeline CI/CD usando o GitLab, como visto nas atividades práticas.

Obs: Caso sua máquina tenha 8Gb ou menos de memória, utilize o GitHub Action ao invés do Gitlab

O pipeline CI/CD deve contemplar inicialmente:

Controle de versão com Git: Todo o código-fonte deve estar armazenado em um repositório Gitlab, usando tags para marcar versões específicas do código, com ramificações dedicadas para produção, estágio e desenvolvimento.

Integração Contínua (CI):

Compilação: O código deve ser automaticamente compilado a cada commit para assegurar a consistência do ambiente.

Testes Automatizados: Realizar os Testes unitários, de integração e funcionais são executados.

Etapa 4: Análise Estática de Código
A análise estática de segurança (SAST, na sigla em inglês) é fundamentais para garantir a segurança da aplicação. A SAST envolve a análise estática e de dependencia do código fonte da aplicação em busca de vulnerabilidades.

Para a análise estática, utilize uma ferramenta chamada Bandit, que é uma ferramenta de análise de segurança Python.

Para uma análise de dependencias, utilize a ferramenta OWASP Dependency-Check para identificar bibliotecas desatualizadas ou com falhas de segurança.

Inclua no pipeline CI/CD essa etapa de SAST:

Análise Estática de Código

uso do Bandit para analisar o código em busca de vulnerabilidades.

Análise de Dependência

uso do Owasp Dependency-check

Etapa 5: Análise Dinâmica de Segurança (DAST)
Para a análise dinâmica, utilize o OAWSP ZAP na aplicação, que deve estar em execução em um container Docker.

Certifique-se de que a aplicação esteja em execução.

Inicie o Zed Attack Proxy (ZAP), uma ferramenta gratuita de testes de penetração que busca vulnerabilidades em aplicações web, a partir de uma imagem docker.

Configure o ZAP para usar o quick start, apontando para o endereço da aplicação (por exemplo, http://192.168.98.10:8080)

Inicie a verificação de segurança.

Após a verificação, o ZAP fornecerá um relatório detalhado de possíveis problemas de segurança.

Após essa etapa, você deve ter uma boa compreensão de como está a qualidade do código e a segurança da sua aplicação.

Lembre-se de corrigir os problemas encontrados e repetir os testes até que todos passem e a aplicação esteja segura.

Etapa 6: Entrega Contínua (CD)
Acrescente no pipeline CI/CD, a fase de Entrega Contínua (CD):

Review:

Para cada merge request, um ambiente temporário de revisão é criado automaticamente para avaliação manual.

Deploy em Estágio:

Para posterior aprovação, o código é implantado no ambiente de stage para simular a produção

Testes de Segurança de Aplicação Dinâmicos (DAST)

O OWASP ZAP é usado para realizar testes de segurança no ambiente de stage.

Etapa 7: Feedback e Monitoramento: (Revisar e analisar novas ferramentas)
Pesquise por ferramentas de monitoramento que possam analisar o log da aplicação e fornecer alertas imediatos de qualquer anomalia (por exemplo, tentativa de quebra de senha por força bruta)

Inclua no pipeline esse monitoramento Pós-Implantação:

Instalação de ferramentas que monitoram a aplicação em produção para detectar problemas.

Etapa 8: Documentação e Entrega Final (Considerar prints de etapas críticas do pipeline)
Por fim, documente o processo de desenvolvimento, implementação e segurança do sistema.

Prepare um relatório final, com no máximo 4 páginas, descrevendo o projeto, as etapas realizadas (com prints das telas mais importantes), as ferramentas utilizadas, os resultados alcançados e as lições aprendidas. Coloque também no relatório a versão final do pipeline ci/cd, com o conteúdo do arquivo .gitlab-ci.yml.

Tarefa a Entregar
Entregue o relatório final, em PDF.

Conclusão
Ao longo deste estudo de caso, tivemos a oportunidade de aplicar uma variedade de habilidades e conceitos importantes, desde o planejamento e design de um sistema até sua implementação e monitoramento contínuo. Este processo nos ajudou a entender melhor os desafios do desenvolvimento de software seguro e eficiente e nos preparou melhor para enfrentar esses desafios no futuro.