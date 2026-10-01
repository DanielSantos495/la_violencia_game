import { Scene } from 'phaser';
import { InkRunner } from '../../core/narrative/InkRunner.ts';
import { Globos } from '../../ui/Globos.ts';

/** Escena de prueba del setup: diálogo Ink en globos DOM. No es contenido del juego. */
export class Prueba extends Scene {
  private globos: Globos | null = null;

  constructor() {
    super('Prueba');
  }

  preload(): void {
    this.load.json('ink-prueba', 'generated/ink/prueba.json');
  }

  create(): void {
    const capaUi = document.getElementById('ui');
    if (!capaUi) throw new Error('Falta el contenedor #ui');
    const runner = new InkRunner(
      this.cache.json.get('ink-prueba') as Record<string, unknown>,
    );
    this.globos = new Globos(capaUi, runner);
    this.globos.avanzar();
    this.events.once('shutdown', () => this.globos?.destruir());
  }
}
