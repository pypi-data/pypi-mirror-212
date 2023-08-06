<h1>Pyrubi 2.1.0</h1>

> Pyrubi is a powerful and easy library for building self Bots in Rubika

<style>
    .image {
        border-radius: 12px
    }
    h1 {
        text-align: center;
        color: dodgerblue;
        font-size: 25px;
        border-radius: 3px
    }
    a{
        margin: 1px;
        color: white;
        background-image: linear-gradient(to right, rgb(0, 89, 255), rgb(0, 166, 255));
        font-size: 18px;
        border-radius: 3px
    }
</style>

<p align='center'>
    <img src='https://iili.io/HIjPRS9.jpg' alt='Pyrubi Library 2.1.0' width='356' class="image">
</p>
<p align='center'>
    <a href='https://github.com/AliGanji1/pyrubi'>GitHub</a>
    <a href='https://rubika.ir/pyrubika'>Documents</a>
</p>

<hr>

**Example:**
``` python
from pyrubi import Bot, Message

bot = Bot("TOKEN")

for update in bot.on_message():
    message = Message(update)
    if m.text() == 'Hello':
        bot.send_text(message.chat_id(), "``Hello`` **from** __Pyrubi__ ~~Library~~, --I'm Ali--.", message.message_id())
```

<hr>

### Features:
    
- **Fast** : *The requests are very fast.*

- **Easy** : *All methods and features are designed as easy and optimal as possible*

- **Powerful** : *While the library is simple, it has high speed and features that make your work easier and faster*


<hr>

## Rubika : @pyrubika

### Install or Update:

``` bash
pip install -U pyrubi
```
