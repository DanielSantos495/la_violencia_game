import { AUTO, Game, Scale, type Types } from 'phaser';
import { Boot } from './game/scenes/Boot.ts';
import { Menu } from './game/scenes/Menu.ts';
import { Prueba } from './game/scenes/Prueba.ts';
import './ui/ui.css';

// Resolución base 1920×1080 con escalado (doc 04 §8). AUTO = WebGL con respaldo Canvas.
const config: Types.Core.GameConfig = {
  type: AUTO,
  parent: 'game',
  width: 1920,
  height: 1080,
  backgroundColor: '#000000',
  scale: {
    mode: Scale.FIT,
    autoCenter: Scale.CENTER_BOTH,
  },
  scene: [Boot, Menu, Prueba],
};

export const game = new Game(config);
