# FISCO OPEN

Pague o imposto devido. Nem um centavo a mais.

Projeto independente e experimental. Não é produto da Receita Federal, não substitui contador e não calcula tributos para recolhimento.

## Executar

Requer Python 3.10+. Na raiz:

```sh
python -m fisco_open calculate examples/commerce.json
python -m fisco_open compare examples/scenarios.json
python -m fisco_open upstream
python -m unittest discover -s tests -v
```

Escopo: estimativa histórica para competências de 2025, anexos I a V do Simples, primeiras quatro faixas até R$ 1,8 milhão de RBT12. Apenas empresa estabelecida, elegível, com anexo confirmado e receita doméstica única, sem tratamentos especiais e abaixo dos limites aplicáveis. Não implementa segregação, regras de início de atividade, determinação automática do anexo por atividade, retenções, substituição tributária, monofasia, sublimites ou repartição de tributos. A confirmação dessas condições é responsabilidade externa. Fontes: [LC 123, art. 18 e anexos](https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp123.htm) e [Resolução CGSN 140](https://normas.receita.fazenda.gov.br/sijut2consulta/link.action?idAto=92278). Arredondamento apenas no total estimado; paridade PGDAS-D não verificada.

O comparador usa valores monetários hipotéticos fornecidos pelo usuário, para o mesmo período e sem duplicidade. Não determina elegibilidade nem recomenda troca de regime. O hash SHA-256 da evidência detecta alterações, não certifica a verdade das premissas.

Os adaptadores RTC somente encaminham JSON a serviços locais, sem validar o resultado fiscal. Ver [guia de integração](docs/upstream.md). Nenhum dado é enviado a servidores remotos pelo aplicativo; mantenha os serviços upstream em ambiente isolado e não publique relatórios com dados reais.

### Fator R histórico

`python -m fisco_open factor-r examples/factor-r.json` calcula o fator R para atividades previamente confirmadas e empresas com 12 meses completos de histórico. O resultado indica Anexo III ou V, sem inferir elegibilidade nem alterar automaticamente o comando `calculate`. A FS12 inclui folha paga e encargos elegíveis, e a RBT12r inclui receitas internas e exportações. O DAS do Anexo IV não inclui CPP patronal. Competências de 2026 permanecem fora do escopo. Base: Res. CGSN 140, art. 26, e LC 123, art. 18.
