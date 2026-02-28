# Stormer-Problem

Simulações numéricas do **Problema de Störmer** — movimento de partículas carregadas no campo de um dipolo magnético — usando o **método de Stormer-Verlet** (integração de segunda ordem). O projeto faz parte de um tema de pesquisa em iniciação científica.

---

## Contexto histórico e físico

Um tipo especial de espalhamento abordado neste trabalho é o **Problema de Störmer**, nome dado em homenagem ao cientista norueguês Carl Störmer. Com a descoberta do efeito que a latitude exerce sobre a intensidade dos raios cósmicos incidentes, o estudo do movimento de partículas carregadas em campos geomagnéticos ganhou notoriedade, em particular o movimento de partículas sob a influência do campo magnético da Terra.

Carl Störmer dedicou grande parte de sua vida, ao longo do século XX, ao estudo desses fenômenos. Störmer realizou análises qualitativas e quantitativas do campo magnético terrestre e produziu diversos trabalhos científicos sobre a possibilidade de partículas ficarem presas em um cinturão ao redor da Terra, além de estudar as equações de movimento para esse cenário. Mais tarde, essa região em que as partículas ficam confinadas foi observada pelos satélites Explorer 1 e Explorer 3, recebendo o nome de **cinturão de radiação de Van Allen** em homenagem a James Alfred Van Allen, que participou da construção dos satélites e da instrumentação utilizada na descoberta. Esse problema ficou conhecido como problema de Störmer, e os resultados de Carl Störmer ajudaram a esclarecer fenômenos como a aurora boreal.

*(Referências bibliográficas: Clay, Compton, Stormer, Stormer2, Stormer3 — ver relatório de iniciação científica.)*

---

## Método numérico

As equações de movimento são integradas com o **método de Stormer-Verlet**, um esquema symplectic de segunda ordem que preserva bem as constantes de movimento (energia, momento canônico azimutal etc.) em longos tempos de simulação.

---

## Estrutura do repositório e solvers em C

| Caminho | Descrição |
|--------|------------|
| **`stormer-verlet_method/constraint_case/sphere/`** | Partícula **confinada à superfície de uma esfera** (R fixo), com dipolo no centro. Baseado no problema restrito de Störmer (Cortés & Cortés Poza, *Eur. J. Phys.* 2015). Integração das equações de Hamilton em coordenadas esféricas (θ, φ) com momento canônico p_φ constante. |
| **`stormer-verlet_method/no_constraint_case/3d_case/`** | Caso **tridimensional completo**: movimento em (ρ, z, φ) no campo do dipolo (sem restrição a superfície). Solver em C (`sv_3d.c`) com Stormer-Verlet; scripts Python para trajetórias 3D, projeções 2D e espaço de fases. |
| **`stormer-verlet_method/no_constraint_case/equatorial_case/`** | Caso **equatorial** (órbita no plano z = 0): potencial efetivo e integração em (ρ, φ). Solver em C (`sv_equatorial.c`); scripts para potencial efetivo e gráficos. |
| **`Saletan_example/`** | Exemplo comparativo baseado em Saletan; implementação e visualização em Python. |

### Resumo dos solvers em C

- **`sv_sphere.c`** — Störmer restrito à esfera (θ, φ; momentos canônicos). Saída: trajetória (x, y, z) e espaço de fases. Parâmetros: tempo total, θ₀, p_θ0, φ₀, p_φ, arquivos de saída.
- **`sv_3d.c`** — Störmer 3D em coordenadas cilíndricas (ρ, z, φ). Constante de movimento c₂; saída em coordenadas e trajetórias.
- **`sv_equatorial.c`** — Movimento no plano equatorial; potencial efetivo e evolução de ρ, φ.

---

## Requisitos

- **Compilador C** (gcc ou clang) com suporte à biblioteca matemática (`-lm`).
- **Python 3** com NumPy, Matplotlib e Pandas (para os scripts de plot).

---

## Como rodar (exemplo: caso esfera)

```bash
cd stormer-verlet_method/constraint_case/sphere
./run.sh
```

O script `run.sh` compila `sv_sphere.c`, executa a simulação (parâmetros editáveis no próprio script, conforme figuras do artigo de referência) e gera o plot com `plotSphere.py`. O nome do arquivo de imagem pode ser passado pela linha de comando:

```bash
python3 plotSphere.py sphere_plot_fig6a.png
```

Os dados numéricos são gravados em `data/sphere.dat` e `data/phase_space.dat` (esses arquivos estão no `.gitignore`).

---

## Referências

- Cortés, E. & Cortés Poza, D., *Störmer problem restricted to a spherical surface*, Eur. J. Phys. **36**, 055009 (2015). *(PDF em `stormer-verlet_method/constraint_case/sphere/references/`.)*
- Störmer, C., *The Polar Aurora*, Oxford (1955).
- Relatório de iniciação científica (referências Clay, Compton, Stormer2, Stormer3, etc.).

---

## Licença

Uso acadêmico / projeto de iniciação científica.
