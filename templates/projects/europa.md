# Real-Time Strategy Game Engine

With a friend we wanted to make a clone of the famous RTS game <a href="https://en.wikipedia.org/wiki/Age_of_Empires">Age of Empires</a> from scratch.

![]({{rootImages}}projects/europa/ageofempire.jpg)

How hard can it be right?
No need to say that this project was a failure, but we've managed to implement some interesting stuff, still nowhere close to a complete game.

![]({{rootImages}}projects/europa/europa-scene.png)

## Features
- Entity-Components architecture
- Client/Server network architecture
- Resources manager
- Screens system (Splash screen, Pause, Game, ...)
- 2D isometric renderer
- UI system with dirty system
- Text box
- Check box
- Combo box
- Button
- Scroll bar
- Serializer
- Map loader
- Map editor
- Embedded debugging console
- Errors &amp; logging system
- Sound system
- Game entities
- Path finding using A*

I wrote the renderer, UI system and resources manager while my friend worked on the networking system and collisions handling. Our engine was able to handle quite a bit of entities...

![]({{rootImages}}projects/europa/europa-macdonald.png)

Here's the first entity we've sent through the internet!

![]({{rootImages}}projects/europa/europa-first-entity.png)

Code available on [GitHub](https://github.com/Nicolas82588/europa)
