# Official upstream references

Portaria Cotec 342/2026, art. 2: https://www.in.gov.br/web/dou/-/portaria-cotec-n-342-de-12-de-novembro-de-2026-744398356
Official announcement: https://www.gov.br/receitafederal/pt-br/assuntos/noticias/2026/novembro/receita-federal-publica-primeiro-codigo-fonte-aberto-no-github-e-amplia-transparencia-da-reforma-tributaria
The initial pinned references were checked by fetching LICENSE at each commit through GitHub; ZIP hashes and full dependency licenses have not been audited.

| Repo | Initial commit | Role |
|---|---|---|
| ReceitaFederal/calculadora-rtc-regime-regular | 150cccbe414d4a5edea703e4f7a424af5aa222c7 | JSON adapter |
| ReceitaFederal/calculadora-rtc-simples-nacional | c5b0f01c8351c3f0d0795cc617b29d233e9f98df | JSON adapter |
| ReceitaFederal/calculadora-rtc-gerador-danfse | 8d79e6b2f7fad6375340afcb51c85ed370c64a14 | inventory only |

The two pinned Java READMEs require Java 21+, Maven wrapper, SQLite and Flyway. Newer upstream main differs; follow pinned documentation. Obtain the source separately:

```sh
git clone https://github.com/ReceitaFederal/calculadora-rtc-regime-regular.git
cd calculadora-rtc-regime-regular
git checkout --detach 150cccbe414d4a5edea703e4f7a424af5aa222c7
git rev-parse HEAD
mkdir -p calculadora/db
./mvnw flyway:migrate -Dflyway.configFiles=./flyway/flyway-pro.conf --batch-mode --errors
./mvnw clean test
./mvnw spring-boot:run -Dspring-boot.run.profiles=offline
```

For Simples use its pinned README and verify the database migration dependency before starting. The pinned README contains an ambiguous self-reference for migration scripts; current main points to the regular repository. Do not mix revisions without testing. Prepare payloads using the running pinned service Swagger, not invented fixtures. From FISCO OPEN root:

```sh
python -m fisco_open rtc-regular request.json
python -m fisco_open rtc-simples request.json
```

These commands require a locally running service on port 8080 or 8082. The adapter does not verify the running commit, JSON schema or item-level errors. Do not use responses for filing or tax decisions until reviewed. Actual end-to-end integration, parity, security and dependency audits remain open.
