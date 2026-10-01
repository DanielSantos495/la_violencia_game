import { Scene } from 'phaser';

export class Menu extends Scene {
  constructor() {
    super('Menu');
  }

  create(): void {
    // Sin menú todavía: pasa directo a la escena de prueba del setup.
    this.scene.start('Prueba');
  }
}
