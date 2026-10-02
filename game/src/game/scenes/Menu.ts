import { Scene } from 'phaser';

export class Menu extends Scene {
  constructor() {
    super('Menu');
  }

  create(): void {
    // Sin menú todavía: pasa directo a la escena de prueba del setup.
    // En desarrollo, ?escena=<clave> abre otra escena registrada (p. ej. PruebaEscenario).
    const pedida = import.meta.env.DEV
      ? new URLSearchParams(location.search).get('escena')
      : null;
    this.scene.start(
      pedida && pedida in this.game.scene.keys ? pedida : 'Prueba',
    );
  }
}
