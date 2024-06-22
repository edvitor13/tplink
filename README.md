# TPLink

Criado com o objetivo de abstrair a utilização da lib [python-kasa](https://github.com/python-kasa/python-kasa), facilitando a realização de ações simples (de forma síncrona) em Lâmpadas Inteligentes.

Por enquanto foi testado apenas em lâmpadas TAPO [modelo L530E](https://www.amazon.com.br/LAMPADA-INTELIGENTE-TP-LINK-L530E-AJUSTE/dp/B08GDC99PX/ref=sr_1_2?__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=21ET49R06NSWW&dib=eyJ2IjoiMSJ9.Jlxns5So4V3YyKLZu9tNy_wcLaaMxnfNIk0jtm7n18Jrelr8HQu122XV6YcOcftpIvR3CF-Ih7uTVWJPc_SzIlvgBgSveaYL4CjmKflrUX6ZYeqkfETHkk-GHpXN9AxejWS3b7tBUhWPj9zO6fm-gH4H0vFVOzb0dCG1GKcnPBbZWMafEwG9_1ezq2K6OiCfNjgzodSZ7h1cZQ5MP657N9uNVDpORBWL6glpFgCSDT4.qdSrm1l6dkiC2rCNf7cPlykTOJMzdITwK14LAeKOb6I&dib_tag=se&keywords=LAMPADA+WI-FI+INTELIGENTE+TP-LINK+TAPO+L530E&qid=1719080830&s=hi&sprefix=lampada+l530e%2Chi%2C177&sr=1-2), porém, deve oferecer suporte para [outros dispositivos](https://github.com/python-kasa/python-kasa/blob/master/SUPPORTED.md) das marcas **TAPO/KASA**.

## Instalando para desenvolvimento/testes:

* Utilize o python 3.11+
* Para instalar via poetry: (no diretório do projeto)
  * `poetry install`
  * `poetry shell`
* Para instalar via pip: (no diretório do projeto)
  * `python -m pip install--no-cache-dir-r requirements.txt`

## Instalando como lib

* PIP:

```shell
pip install git+https://github.com/edvitor13/tplink.git
```

* Poetry:

```shell
poetry add git+https://github.com/edvitor13/tplink.git
```

## Exemplos de uso:

Utilizando o modelo `L530E` como base.

1. Conecte e configure a lâmpada via aplicativo oficial TAPO.
2. Crie uma conta para gerenciar a Lâmpada via aplicativo.
3. Escolha um nome (label) para o dispositivo (Ex: Lâmpada Quarto)

Para testes, no arquivo main.py, importe a classe Lamp do módulo tplink:

```py
from tplink.lamp import Lamp
```

Crie uma nova instância de Lamp, informando as credenciais criadas no APP Oficial:

```py
lamp = Lamp(
    "emailtapoaccount@example.com", 
    "PasswordTapoAccount"
)
```

Ao instanciar Lamp, ela buscará na rede local todos os dispositivos inteligêntes que estão conectados e se conectará no primeiro que encontrar (do tipo lâmpada "is_bulb == True")

Por este motivo, é recomendado especificar o modelo e o label na lâmpada:

```py
lamp = Lamp(
    "emailtapoaccount@example.com", 
    "PasswordTapoAccount",
    label="Lâmpada Quarto", 
    model="L530"
)
```

**Agora** utilize as funcionalidades de `Lamp`, exemplos:

1. Verifica se a lâmpada está ligada, se estiver, desliga:

```py
if lamp.is_on:
    lamp.turn_off()
```

2. Liga a lâmpada na cor amarela, altera o brilho para 50%, espera 10 segundos e desliga:

```py
lamp.set_color_rgbhex(lamp.Colors.YELLOW)
lamp.turn_on()
lamp.set_brightness(50)
lamp.turn_off()
```

Também é possível realizar estas ações de forma encadeada:

```py
(
    lamp
        .set_color_rgbhex(lamp.Colors.YELLOW)
        .turn_on()
        .set_brightness(50)
        .turn_off()
)
```

3. Suporte para execução assíncrona, inicie com o método "begin_async_mode" e termine com "run_async_mode" para executar:

```py
(
    lamp
        .begin_async_mode()
        .set_color_rgb(255, 0, 255)
        .turn_on()
        .set_color_rgbhex(lamp.Colors.RED)
        .sleep(10)
        .turn_off()
        .run_async_mode()
)
```

Nesse formato a execução acontece em uma outra thread, assim, o fluxo não será travado.



## Cores

`Lamp` possui internamente a classe `Colors`, que possui alguns códigos hexadecimais de cores comuns:

1. Alterando para a cor vermelha **utilizando** `Colors`.

```py
lamp.set_color_rgbhex(lamp.Colors.RED)
```

2. Alterando para a cor vermelha **sem utilizar** `Colors`.

```py
lamp.set_color_rgbhex("#ff0000")
```

## Propriedades e Funcionalidades

### Propriedades

#### `username`

* **Recebe:** Nada
* **Retorna:** `str` - o nome de usuário associado à lâmpada.
* **Descrição:** Retorna o nome de usuário associado à lâmpada.

#### `brightness`

* **Recebe:** Nada
* **Retorna:** `int` - o nível de brilho atual da lâmpada.
* **Descrição:** Retorna o nível de brilho atual da lâmpada.

#### `hsv`

* **Recebe:** Nada
* **Retorna:** `tuple[int, int, int]` - o valor de cor HSV atual da lâmpada.
* **Descrição:** Retorna o valor de cor HSV atual da lâmpada.

#### `rgb`

* **Recebe:** Nada
* **Retorna:** `tuple[int, int, int]` - o valor de cor RGB atual da lâmpada.
* **Descrição:** Retorna o valor de cor RGB atual da lâmpada.

#### `is_on`

* **Recebe:** Nada
* **Retorna:** `bool` - `True` se a lâmpada estiver ligada, caso contrário `False`.
* **Descrição:** Retorna `True` se a lâmpada estiver ligada, caso contrário `False`.

#### `is_off`

* **Recebe:** Nada
* **Retorna:** `tuple[int, int, int]` - `True` se a lâmpada estiver desligada, caso contrário `False`.
* **Descrição:** Retorna `True` se a lâmpada estiver desligada, caso contrário `False`.

### Funcionalidades

#### `sleep`

* **Recebe:** `seconds: float`
* **Retorna:** `Lamp`
* **Descrição:** Pausa a execução por um número especificado de segundos.

#### `all_lamps`

* **Recebe:** Nada
* **Retorna:** `list[SmartBulb]` - lista de todas as lâmpadas inteligentes descobertas.
* **Descrição:** Retorna uma lista de todas as lâmpadas inteligentes descobertas.

#### `update`

* **Recebe:** Nada
* **Retorna:** `Lamp`
* **Descrição:** Atualiza as informações da lâmpada.

#### `turn_on`

* **Recebe:** Nada
* **Retorna:** `Lamp`
* **Descrição:** Liga a lâmpada.

#### `turn_off`

* **Recebe:** Nada
* **Retorna:** `Lamp`
* **Descrição:** Desliga a lâmpada.

#### `alternate_turn_on_off`

* **Recebe:** `times: int`, `sleep_ms: int = 100`
* **Retorna:** `Lamp`
* **Descrição:** Alterna ligando e desligando a lâmpada por um número especificado de vezes.

#### `blink`

* **Recebe:** `times: int`, `sleep_ms: int = 0`, `step: int = 15`, `min: int = 1`, `max: int = 100`, `end_with_start: bool = True`
* **Retorna:** `Lamp`
* **Descrição:** Faz a lâmpada piscar um número especificado de vezes com brilho ajustável.

#### `set_last_color`

* **Recebe:** `transition_ms: int | None = None`
* **Retorna:** `Lamp`
* **Descrição:** Define a lâmpada para a última cor usada.

#### `set_color_rgbhex`

* **Recebe:** `hex_color: str`, `transition_ms: int | None = None`
* **Retorna:** `Lamp`
* **Descrição:** Define a cor da lâmpada usando um valor RGB em hexadecimal.

#### `set_color_rgb`

* **Recebe:** `r: float`, `g: float`, `b: float`, `transition_ms: int | None = None`
* **Retorna:** `Lamp`
* **Descrição:** Define a cor da lâmpada usando valores RGB.

#### `set_color_hsv`

* **Recebe:** `h: int`, `s: int`, `v: int`, `transition_ms: int | None = None`
* **Retorna:** `Lamp`
* **Descrição:** Define a cor da lâmpada usando valores HSV.

#### `set_brightness`

* **Recebe:** `percentage: int = 100`, `sleep_ms: int | None = None`, `step: int = 1`
* **Retorna:** `Lamp`
* **Descrição:** Define o brilho da lâmpada para uma porcentagem especificada.
