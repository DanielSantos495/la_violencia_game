import { Story } from 'inkjs';

/** Una línea de diálogo lista para mostrarse en un globo. */
export interface Linea {
  texto: string;
  /** Valor del tag `# hablante: X`, o null si la línea no lo trae. */
  hablante: string | null;
  tags: string[];
}

export interface Opcion {
  indice: number;
  texto: string;
}

const TAG_HABLANTE = /^hablante:\s*(.+)$/;

/** Envoltorio del runtime de Ink (doc 04 §4). Sin Phaser ni DOM. */
export class InkRunner {
  private readonly story: Story;

  constructor(json: string | Record<string, unknown>) {
    this.story = typeof json === 'string' ? new Story(json) : new Story(json);
  }

  get puedeContinuar(): boolean {
    return this.story.canContinue;
  }

  get terminado(): boolean {
    return !this.story.canContinue && this.story.currentChoices.length === 0;
  }

  /** Avanza una línea. Devuelve null si no hay más texto antes de una decisión o del final. */
  continuar(): Linea | null {
    if (!this.story.canContinue) return null;
    const texto = (this.story.Continue() ?? '').trim();
    const tags = this.story.currentTags ?? [];
    let hablante: string | null = null;
    for (const tag of tags) {
      const m = TAG_HABLANTE.exec(tag.trim());
      if (m?.[1]) hablante = m[1].trim();
    }
    return { texto, hablante, tags };
  }

  opciones(): Opcion[] {
    return this.story.currentChoices.map((c) => ({
      indice: c.index,
      texto: c.text,
    }));
  }

  elegir(indice: number): void {
    if (!this.story.currentChoices.some((c) => c.index === indice)) {
      throw new Error(`Opción inexistente: ${indice}`);
    }
    this.story.ChooseChoiceIndex(indice);
  }

  variable(nombre: string): unknown {
    return this.story.variablesState.$(nombre);
  }

  /** Estado completo de Ink serializado (incluye variables) para el guardado. */
  exportarEstado(): string {
    return this.story.state.ToJson();
  }

  importarEstado(json: string): void {
    this.story.state.LoadJson(json);
  }
}
