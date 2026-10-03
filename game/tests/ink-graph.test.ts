import { describe, expect, it } from 'vitest';
import paleta from '../art/paleta.json';
import {
  aDot,
  analizarInk,
  renderizarSvg,
  textoOpcion,
  tintaDePaleta,
  unirIncludes,
} from '../tools/ink-graph.ts';

const ink = `
VAR conciencia = 0
// comentario -> no_existe
-> mercado

=== mercado ===
Rosalba llega con la cuajada. # hablante: Rosalba
* [Saludar a Aurelio]
    ~ conciencia = 1
    -> casa
+ (quedarse) [Quedarse en la plaza] -> mercado.plaza
* {conciencia > 0} [Seguir a Efraín] -> casa
= plaza
Tiendas rojas y azules. # hablante: Custodia
-> DONE

=== casa ===
<- radio
- (reunion) La radio suena.
-> tunel_sermon ->
-> perdido

=== radio ===
La radio. -> DONE

=== tunel_sermon ===
Sermón. ->->

=== suelto ===
Nadie llega aquí. -> END

=== function doble(x) ===
~ return x * 2
`;

describe('analizarInk', () => {
  const g = analizarInk(ink);

  it('encuentra knots, stitches y nodos de fin; ignora funciones', () => {
    expect([...g.nodos.keys()]).toEqual(
      expect.arrayContaining([
        'mercado',
        'mercado.plaza',
        'casa',
        'radio',
        'DONE',
        'END',
      ]),
    );
    expect(g.nodos.has('doble')).toBe(false);
  });

  it('clasifica aristas: opción, condicional, persistente, hilo y túnel', () => {
    const a = (desde: string, hacia: string) =>
      g.aristas.find((x) => x.desde === desde && x.hacia === hacia);
    expect(a('mercado', 'casa')).toMatchObject({
      tipo: 'opcion',
      etiqueta: 'Saludar a Aurelio',
    });
    expect(a('mercado', 'mercado.plaza')).toMatchObject({
      tipo: 'opcion',
      persistente: true,
    });
    expect(
      g.aristas.filter(
        (x) => x.desde === 'mercado' && x.hacia === 'casa' && x.condicional,
      ),
    ).toHaveLength(1);
    expect(a('casa', 'radio')?.tipo).toBe('hilo');
    expect(a('casa', 'tunel_sermon')?.tipo).toBe('tunel');
  });

  it('registra escrituras de variables, hablantes y opciones', () => {
    const m = g.nodos.get('mercado');
    expect(m?.escribe.has('conciencia')).toBe(true);
    expect(m?.hablantes.has('Rosalba')).toBe(true);
    expect(m?.opciones).toBe(3);
    expect(g.nodos.get('mercado.plaza')?.hablantes.has('Custodia')).toBe(true);
  });

  it('ignora comentarios y avisa destinos inexistentes, inalcanzables y sin salida', () => {
    const tipos = g.avisos.map((a) => `${a.tipo}:${a.nodo}`);
    expect(tipos).toContain('destino-inexistente:casa');
    expect(tipos).toContain('inalcanzable:suelto');
    expect(tipos).toContain('sin-salida:tunel_sermon');
    expect(g.avisos.some((a) => a.detalle.includes('no_existe'))).toBe(false);
  });
});

describe('textoOpcion', () => {
  it('quita condición, etiqueta, divert y tags', () => {
    expect(textoOpcion('(x) {a} Mira[r] hacia atrás -> y # tag')).toBe('Mirar');
    expect(textoOpcion('[Callar] -> fin')).toBe('Callar');
  });
});

describe('unirIncludes', () => {
  it('inserta los INCLUDE una sola vez', () => {
    const archivos: Record<string, string> = {
      'a.ink': '=== a ===\nA -> END',
      'b.ink': 'INCLUDE a.ink',
    };
    const unido = unirIncludes(
      'INCLUDE a.ink\nINCLUDE b.ink',
      (r) => archivos[r] ?? '',
    );
    expect(unido.match(/=== a ===/g)).toHaveLength(1);
  });
});

describe('aDot y render', () => {
  it('genera un SVG con los colores de la paleta y sin rojo ni azul partidista', async () => {
    const tinta = tintaDePaleta(paleta);
    const dot = aDot(analizarInk(ink), 'prueba', tinta);
    expect(dot).toContain(tinta.papel);
    const rojo = paleta.colores.find((c) => c.id === 'rojo-liberal')?.hex ?? '';
    const azul =
      paleta.colores.find((c) => c.id === 'azul-conservador')?.hex ?? '';
    expect(dot.includes(rojo) || dot.includes(azul)).toBe(false);
    const svg = await renderizarSvg(dot);
    expect(svg).toContain('<svg');
    expect(svg).toContain('mercado');
  });
});
