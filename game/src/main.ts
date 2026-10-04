import { AUTO, Game, Scale, type Types } from 'phaser';
import { Boot } from './game/scenes/Boot.ts';
import { Menu } from './game/scenes/Menu.ts';
import { Prueba } from './game/scenes/Prueba.ts';
import { PruebaEscenario } from './game/scenes/PruebaEscenario.ts';
import './ui/ui.css';

// Resolución base 1920×1080 con escalado (doc 04 §8). AUTO = WebGL con respaldo Canvas.
const config: Types.Core.GameConfig = {
  type: AUTO,
  parent: 'game',
  width: 1920,
  height: 1080,
  backgroundColor: '#000000',
  // Detalle limpio en movimiento (doc 03 §1): lo que solo se desplaza (fondos, capas de paralaje)
  // se dibuja en píxeles enteros, sin hormigueo subpíxel; lo que se reduce (personajes) usa
  // mipmaps, que Phaser solo aplica a texturas potencia de dos como las páginas del atlas.
  render: {
    roundPixels: true,
    mipmapFilter: 'LINEAR_MIPMAP_LINEAR',
  },
  scale: {
    mode: Scale.FIT,
    autoCenter: Scale.CENTER_BOTH,
  },
  scene: [Boot, Menu, Prueba, PruebaEscenario],
};

export const game = new Game(config);
